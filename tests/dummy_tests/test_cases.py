import sys

import pytest


@pytest.mark.flaky(reruns=1)
@pytest.mark.link("https://example.com/fail-trace")
@pytest.mark.xfail(reason="Expected failure for plugin test")
def test_fail():
    print("stdout from fail")
    print("stderr from fail", file=sys.stderr)
    pytest.logs = "log from fail"
    assert False


@pytest.mark.link("https://example.com/pass-trace")
@pytest.mark.flaky(reruns=1)
def test_pass():
    print("stdout from pass")
    print("stderr from pass", file=sys.stderr)
    pytest.logs = "log from pass"
    assert True


@pytest.mark.skip(reason="just skipping")
def test_skip():
    pass
