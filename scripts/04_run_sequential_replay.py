#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, pandas as pd, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from skna_framework.core import detect_time_column, detect_median_skna_column, infer_skna_scale_to_uv, sequential_replay, replay_metrics

def main():
 p=argparse.ArgumentParser(); p.add_argument('signals',type=Path); p.add_argument('--threshold',type=float,required=True); p.add_argument('--event-start',type=float,required=True); p.add_argument('--event-end',type=float,required=True); p.add_argument('--out',type=Path,required=True); p.add_argument('--window',type=float,default=30); p.add_argument('--hop',type=float,default=10); p.add_argument('--occupancy',type=float,default=5); p.add_argument('--persistence',type=int,default=2)
 a=p.parse_args(); df=pd.read_csv(a.signals); tc=detect_time_column(df); sc=detect_median_skna_column(df); t=pd.to_numeric(df[tc],errors='coerce').to_numpy(float); scale,_=infer_skna_scale_to_uv(df[sc],sc); y=pd.to_numeric(df[sc],errors='coerce').to_numpy(float)*scale
 rep=sequential_replay(t,y,a.threshold,a.window,a.hop,a.occupancy,a.persistence); a.out.parent.mkdir(parents=True,exist_ok=True); rep.to_csv(a.out,index=False); print(replay_metrics(rep,a.event_start,a.event_end))
if __name__=='__main__': main()
