"""Baselines and models with a shared fit/predict interface (I-08 to I-10).

Interface every model follows (I-09 and I-10 subclass `Model`):

    model = SomeModel().fit(train)         # train: DataFrame from src.data.split(), returns self
    proba = model.predict_proba(df)        # DataFrame, columns = CLASSES, same index as df, rows sum to 1
    labels = model.predict(df)             # Series of class names, same index as df

Only `fit` and `predict_proba` need writing: `predict` is the argmax of `predict_proba`.
`predict_proba` must not read the `fit` label column of `df`. Fit on train only, never on valid or test.
Score with src.metrics: `average_auc(df["fit"], proba)` and `macro_f1(df["fit"], labels)`.
"""

import warnings

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.optimize import minimize
from scipy.special import softmax
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression as _SkLogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

from src.data import CATEGORICAL, NUMERIC
from src.metrics import CLASSES


def _feature_columns() -> ColumnTransformer:
    """Feature matrix shared by LogisticRegression and LatentFactorFit (fit on train only)."""
    flags = [f"{c}_missing" for c in NUMERIC]
    return ColumnTransformer(
        [
            ("num", StandardScaler(), ["size", *NUMERIC]),
            ("cat", OneHotEncoder(handle_unknown="ignore"), list(CATEGORICAL)),
            ("flags", "passthrough", flags),
        ]
    )


class Model:
    """Base class: subclasses implement `fit` and `predict_proba`."""

    def fit(self, train: pd.DataFrame) -> "Model":
        raise NotImplementedError

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def predict(self, df: pd.DataFrame) -> pd.Series:
        return self.predict_proba(df).idxmax(axis=1)


class MajorityClass(Model):
    """Trivial baseline: every row gets the class frequencies of train, so it always predicts "fit"."""

    def fit(self, train: pd.DataFrame) -> "MajorityClass":
        self.freq_ = train["fit"].value_counts(normalize=True).reindex(CLASSES, fill_value=0.0)
        return self

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.DataFrame([self.freq_.to_numpy()] * len(df), columns=list(CLASSES), index=df.index)


class LogisticRegression(Model):
    """Course model: multinomial logistic regression on size, measurements and categories (I-09).

    Input: rows from `src.data.preprocess()`. Features: `size`, the NUMERIC columns and their
    `_missing` flags, and one-hot CATEGORICAL columns. Numbers are standardised, unseen categories
    get all zeros. Everything is fitted on train only. `C` and `class_weight` are for I-11 to tune.
    """

    def __init__(self, C: float = 1.0, class_weight: str | dict | None = None):
        self.C, self.class_weight = C, class_weight

    def fit(self, train: pd.DataFrame) -> "LogisticRegression":
        clf = _SkLogisticRegression(C=self.C, class_weight=self.class_weight, max_iter=1000)
        self.pipeline_ = make_pipeline(_feature_columns(), clf).fit(train, train["fit"])
        return self

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        proba = self.pipeline_.predict_proba(df)  # columns follow classes_ (alphabetical), so name them
        classes = self.pipeline_.classes_
        return pd.DataFrame(proba, columns=classes, index=df.index).reindex(
            columns=list(CLASSES), fill_value=0.0
        )


class LatentFactorFit(Model):
    """Main model (I-10): features plus user and item latent factors with biases, class weighted.

    Input: rows from `src.data.preprocess()` (they carry `user_id` and `item_id`). For class k:

        z_k = w_k . x + b_k + bu[user, k] + bi[item, k] + gamma[user] . delta[item, k]

    `x` is the LogisticRegression feature matrix, `bu` and `bi` are per-class biases, `gamma` is a
    K-dim user vector shared by the classes and `delta` a K-dim item vector per class. `K=0` drops
    the interaction and leaves features plus user and item biases. The softmax of z gives the class
    probabilities. Minimised by L-BFGS (full batch, exact gradients): the loss is smooth, a fit
    takes seconds, and it needs no learning rate. Objective, with sample weight s_i from
    `class_weight` (as in scikit-learn):

        sum_i s_i * CE_i + 0.5 * |W|^2 + 0.5 * lam * (|bu|^2 + |bi|^2 + |gamma|^2 + |delta|^2)

    A user or item not seen in train gets zero bias and zero factors (an all-zero indicator row).
    """

    def __init__(
        self, K: int = 4, lam: float = 5.0, class_weight: str | dict | None = None, max_iter: int = 200
    ):
        self.K, self.lam, self.class_weight, self.max_iter = K, lam, class_weight, max_iter

    def _design(self, df: pd.DataFrame):
        """Sparse X, user indicators U, item indicators It; unseen ids give all-zero rows."""
        X = sparse.csr_matrix(self.columns_.transform(df))
        rows = np.arange(len(df))

        def indicator(ids, index):
            code = index.get_indexer(ids)
            keep = code >= 0
            return sparse.csr_matrix(
                (np.ones(keep.sum()), (rows[keep], code[keep])), shape=(len(df), len(index))
            )

        return X, indicator(df["user_id"], self.users_), indicator(df["item_id"], self.items_)

    def _unpack(self, theta, d):
        sizes = [
            d * 3,
            3,
            len(self.users_) * 3,
            len(self.items_) * 3,
            len(self.users_) * self.K,
            len(self.items_) * self.K * 3,
        ]
        parts = np.split(theta, np.cumsum(sizes)[:-1])
        W, b, Bu, Bi, Gam, Del = parts
        return (
            W.reshape(d, 3),
            b,
            Bu.reshape(-1, 3),
            Bi.reshape(-1, 3),
            Gam.reshape(len(self.users_), self.K),
            Del.reshape(len(self.items_), self.K * 3),
        )

    def _logits(self, params, X, U, It):
        W, b, Bu, Bi, Gam, Del = params
        gam, dl = U @ Gam, (It @ Del).reshape(X.shape[0], self.K, 3)
        return X @ W + b + U @ Bu + It @ Bi + np.einsum("nk,nkc->nc", gam, dl), gam, dl

    def fit(self, train: pd.DataFrame) -> "LatentFactorFit":
        self.columns_ = _feature_columns().fit(train)
        self.users_, self.items_ = pd.Index(train["user_id"].unique()), pd.Index(train["item_id"].unique())
        X, U, It = self._design(train)
        d = X.shape[1]
        y = pd.Index(CLASSES).get_indexer(train["fit"])
        Y = np.eye(3)[y]
        s = compute_sample_weight(self.class_weight, train["fit"])[:, None]
        rng = np.random.default_rng(0)  # random start: all-zero factors are a saddle with zero gradient
        n_theta = (
            d * 3
            + 3
            + (len(self.users_) + len(self.items_)) * 3
            + len(self.users_) * self.K
            + len(self.items_) * self.K * 3
        )
        theta0 = np.zeros(n_theta)
        factors = slice(n_theta - len(self.users_) * self.K - len(self.items_) * self.K * 3, n_theta)
        theta0[factors] = rng.normal(0, 0.1, factors.stop - factors.start)

        def objective(theta):
            params = self._unpack(theta, d)
            W, b, Bu, Bi, Gam, Del = params
            z, gam, dl = self._logits(params, X, U, It)
            logp = np.log(softmax(z, axis=1) + 1e-12)
            loss = (
                -(s * Y * logp).sum()
                + 0.5 * (W**2).sum()
                + 0.5 * self.lam * sum((a**2).sum() for a in (Bu, Bi, Gam, Del))
            )
            G = s * (np.exp(logp) - Y)  # d loss / d z
            gW = X.T @ G + W
            gBu, gBi = U.T @ G + self.lam * Bu, It.T @ G + self.lam * Bi
            gGam = U.T @ np.einsum("nc,nkc->nk", G, dl) + self.lam * Gam
            gDel = It.T @ (gam[:, :, None] * G[:, None, :]).reshape(len(G), -1) + self.lam * Del
            return loss, np.concatenate(
                [
                    gW.ravel(),
                    G.sum(0),
                    gBu.ravel(),
                    gBi.ravel(),
                    np.asarray(gGam).ravel(),
                    np.asarray(gDel).ravel(),
                ]
            )

        res = minimize(objective, theta0, jac=True, method="L-BFGS-B", options={"maxiter": self.max_iter})
        self.params_, self.n_iter_ = self._unpack(res.x, d), res.nit
        self.converged_ = bool(res.success)
        if not self.converged_:
            warnings.warn(
                f"LatentFactorFit did not converge in {res.nit} iterations: {res.message}", stacklevel=2
            )
        return self

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        X, U, It = self._design(df)
        z, _, _ = self._logits(self.params_, X, U, It)
        return pd.DataFrame(softmax(z, axis=1), columns=list(CLASSES), index=df.index)


# Tuned on validation in notebooks/03_models.ipynb (I-11). Build a model: getattr(models, name)(**params).
BEST_PARAMS = {
    "LogisticRegression": {"C": 0.01, "class_weight": "balanced"},
    "LatentFactorFit": {"K": 0, "lam": 2.0, "class_weight": "balanced"},
}
