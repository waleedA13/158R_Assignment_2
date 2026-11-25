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
