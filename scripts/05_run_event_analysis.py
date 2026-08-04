#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, json, pandas as pd, numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from skna_framework.core import *

def main():
 p=argparse.ArgumentParser(description='End-to-end analysis for one processed recording and one or more events.')
 p.add_argument('signals',type=Path); p.add_argument('events',type=Path); p.add_argument('--out-dir',type=Path,required=True); p.add_argument('--baseline-duration',type=float,default=60,help='Seconds immediately before each event onset used for threshold calibration.'); p.add_argument('--window',type=float,default=30); p.add_argument('--hop',type=float,default=10); p.add_argument('--occupancy',type=float,default=5); p.add_argument('--persistence',type=int,default=2)
 a=p.parse_args(); a.out_dir.mkdir(parents=True,exist_ok=True); df=pd.read_csv(a.signals); ev=pd.read_csv(a.events); tc=detect_time_column(df); sc=detect_median_skna_column(df); t=pd.to_numeric(df[tc],errors='coerce').to_numpy(float); scale,note=infer_skna_scale_to_uv(df[sc],sc); y=pd.to_numeric(df[sc],errors='coerce').to_numpy(float)*scale
 sc_start=next(c for c in ev if 'start' in c.lower()); sc_end=next(c for c in ev if 'end' in c.lower()); rows=[]
 for i,r in ev.iterrows():
  onset=float(r[sc_start]); offset=float(r[sc_end]); baseline_start=max(float(np.nanmin(t)),onset-a.baseline_duration); bm=(t>=baseline_start)&(t<onset); th=adaptive_threshold(y[bm],95,6); rep=sequential_replay(t,y,th['adaptive_threshold_uV'],a.window,a.hop,a.occupancy,a.persistence); met=replay_metrics(rep,onset,offset); rep.to_csv(a.out_dir/f'event_{i+1}_replay.csv',index=False); rows.append({'event':i+1,'start_s':onset,'end_s':offset,'baseline_start_s':baseline_start,'baseline_end_s':onset,'baseline_samples':int(bm.sum()),**th,**met})
 pd.DataFrame(rows).to_csv(a.out_dir/'event_summary.csv',index=False); (a.out_dir/'run_config.json').write_text(json.dumps(vars(a)|{'unit_note':note},indent=2,default=str))
 print(a.out_dir)
if __name__=='__main__': main()
