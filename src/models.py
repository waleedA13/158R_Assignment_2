"""Baselines and models with a shared fit/predict interface (I-08 to I-10).

Interface every model follows (I-09 and I-10 subclass `Model`):

    model = SomeModel().fit(train)         # train: DataFrame from src.data.split(), returns self
    proba = model.predict_proba(df)        # DataFrame, columns = CLASSES, same index as df, rows sum to 1
    labels = model.predict(df)             # Series of class names, same index as df

Only `fit` and `predict_proba` need writing: `predict` is the argmax of `predict_proba`.
`predict_proba` must not read the `fit` label column of `df`. Fit on train only, never on valid or test.
Score with src.metrics: `average_auc(df["fit"], proba)` and `macro_f1(df["fit"], labels)`.
"""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression as _SkLogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.data import CATEGORICAL, NUMERIC
from src.metrics import CLASSES


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
        self.numeric_ = ["size", *NUMERIC]
        self.flags_ = [f"{c}_missing" for c in NUMERIC]
        columns = ColumnTransformer(
            [
                ("num", StandardScaler(), self.numeric_),
                ("cat", OneHotEncoder(handle_unknown="ignore"), list(CATEGORICAL)),
                ("flags", "passthrough", self.flags_),
            ]
        )
        clf = _SkLogisticRegression(C=self.C, class_weight=self.class_weight, max_iter=1000)
        self.pipeline_ = make_pipeline(columns, clf).fit(train, train["fit"])
        return self

    def predict_proba(self, df: pd.DataFrame) -> pd.DataFrame:
        proba = self.pipeline_.predict_proba(df)  # columns follow classes_ (alphabetical), so name them
        classes = self.pipeline_.classes_
        return pd.DataFrame(proba, columns=classes, index=df.index).reindex(
            columns=list(CLASSES), fill_value=0.0
        )
