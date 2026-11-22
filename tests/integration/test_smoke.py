"""Integration smoke test. Real pipeline tests (load -> split -> fit -> evaluate on
tests/fixtures/) are added by I-04 and I-08 to I-12, written before the code they test."""

import importlib


def test_src_modules_import_together():
    for name in ("src.data", "src.metrics", "src.models"):
        assert importlib.import_module(name)
