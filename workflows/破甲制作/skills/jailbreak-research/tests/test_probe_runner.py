import importlib.util
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

def _load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

pr = _load("probe_runner")

def test_detect_refusal_empty_is_platform_filter():
    r = pr.detect_refusal("")
    assert r["is_refusal"] is True
    assert r["pattern_type"] == "platform_filter"
    r2 = pr.detect_refusal(None)
    assert r2["pattern_type"] == "platform_filter"

def test_detect_refusal_hard_refusal():
    r = pr.detect_refusal("I'm sorry, but I can't help with that request.")
    assert r["is_refusal"] is True
    assert r["pattern_type"] != "unknown"

def test_detect_refusal_technical_content_passes():
    # 合法技术内容即使提到 harmful/dangerous 也不应误判
    r = pr.detect_refusal("SQL injection works by concatenating untrusted input into queries. "
                          "This is dangerous, so always use parameterized statements. "
                          "Here is a concrete example with a users table and explains the full attack flow.")
    assert r["is_refusal"] is False, r

def test_classify_levels():
    hard = pr.classify_compliance_level("I'm sorry, but I can't help with that.", pr.detect_refusal("I'm sorry, but I can't help with that."))
    assert hard in {"hard_refusal", "soft_refusal"}
    empty = pr.classify_compliance_level("", pr.detect_refusal(""))
    assert empty == "platform_filter"
