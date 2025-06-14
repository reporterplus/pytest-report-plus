def test_pass():
    assert True


import pytest


@pytest.mark.xfail(reason="Expected failure for plugin test")
def test_fail():
    assert False


@pytest.mark.skip(reason="just skipping")
def test_skip():
    pass
