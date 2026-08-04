import numpy as np, pandas as pd
from skna_framework.core import adaptive_threshold, sequential_replay, detect_uap_events

def test_threshold_is_maximum_candidate():
 rng=np.random.default_rng(1); x=np.r_[rng.normal(1,.08,5000),rng.normal(1.8,.12,100)]
 r=adaptive_threshold(x,95,6)
 assert np.isclose(r['adaptive_threshold_uV'],max(r['gmm_threshold_uV'],r['q95_threshold_uV'],r['median_plus_6mad_uV']))

def test_replay_no_future_access_shape():
 t=np.arange(0,200,.1); y=np.ones_like(t); y[(t>=80)&(t<130)]=3
 r=sequential_replay(t,y,2,30,10,5,2)
 assert {'window_end_relative_s','burst_occupancy_pct','candidate_on','trigger_on'} <= set(r.columns)
 assert r.window_end_relative_s.is_monotonic_increasing

def test_multiple_uap_events():
 t=np.arange(0,300,.1); y=np.zeros_like(t); y[(t>50)&(t<100)]=-30; y[(t>180)&(t<240)]=-25
 ev,_=detect_uap_events(t,y,-10,5,2)
 assert len(ev)==2
