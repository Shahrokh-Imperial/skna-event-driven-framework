import json
from pathlib import Path
from skna_framework.core import persistence_gate

def test_defaults_match_manuscript():
    cfg=json.loads((Path(__file__).parents[1]/"config/defaults.json").read_text())
    assert cfg["baseline"]["duration_before_onset_s"]==60
    assert cfg["replay"]=={"window_s":30.0,"update_s":10.0,"occupancy_threshold_pct":5.0,"persistence_updates":2}

def test_two_update_persistence():
    out=persistence_gate([False,True,True,False],2)
    assert list(out)==[False,False,True,False]
