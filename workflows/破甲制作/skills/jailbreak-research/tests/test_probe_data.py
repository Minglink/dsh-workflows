import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "probes.json"
KNOWN_FRAMES = {"direct","academic","fiction","prefill","technical","technical_precise","authority","gradual","ctf","disguised","meta","casual","polite","imperative","question"}

def _load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def test_counts():
    d = _load()
    assert len(d["probes"]) == 208
    assert len(d["meta_awareness"]) == 13

def test_unique_ids():
    d = _load()
    ids = [p["id"] for p in d["probes"]] + [p["id"] for p in d["meta_awareness"]]
    assert len(ids) == len(set(ids)), "duplicate probe id"

def test_schema():
    d = _load()
    for p in d["probes"] + d["meta_awareness"]:
        assert p["id"] and p["category"] and p["msg"], p
        assert p["frame"] in KNOWN_FRAMES, (p["id"], p["frame"])
        assert p.get("tier", 0) in (0,1,2,3,4,5)

def test_tiers_bounded():
    d = _load()
    tiers = {p["tier"] for p in d["probes"]}
    assert tiers <= {0,1,2,3,4,5}, tiers
