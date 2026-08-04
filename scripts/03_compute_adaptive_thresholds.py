#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, pandas as pd, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from skna_framework.core import detect_time_column, detect_median_skna_column, infer_skna_scale_to_uv, adaptive_threshold

def main():
 p=argparse.ArgumentParser(); p.add_argument('signals',type=Path); p.add_argument('--event-start',type=float,required=True); p.add_argument('--baseline-duration',type=float,default=60,help='Seconds immediately before event onset used for calibration.'); p.add_argument('--out',type=Path,required=True); p.add_argument('--k-mad',type=float,default=6); p.add_argument('--percentile',type=float,default=95)
 a=p.parse_args(); df=pd.read_csv(a.signals); tc=detect_time_column(df); sc=detect_median_skna_column(df); t=pd.to_numeric(df[tc],errors='coerce').to_numpy(float); scale,note=infer_skna_scale_to_uv(df[sc],sc); y=pd.to_numeric(df[sc],errors='coerce').to_numpy(float)*scale
 baseline_start=max(float(np.nanmin(t)),a.event_start-a.baseline_duration); m=(t>=baseline_start)&(t<a.event_start); result=adaptive_threshold(y[m],a.percentile,a.k_mad); result.update({'baseline_start_s':baseline_start,'baseline_end_s':a.event_start,'baseline_duration_requested_s':a.baseline_duration,'baseline_samples':int(m.sum()),'unit_note':note,'k_mad':a.k_mad})
 a.out.parent.mkdir(parents=True,exist_ok=True); pd.DataFrame([result]).to_csv(a.out,index=False); print(a.out)
if __name__=='__main__': main()
