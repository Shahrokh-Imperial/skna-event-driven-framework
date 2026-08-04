#!/usr/bin/env python3
from pathlib import Path
import argparse, sys, pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from skna_framework.core import load_any_recording, detect_time_column, detect_uap_column, suggest_uap_threshold, detect_uap_events

def main():
 p=argparse.ArgumentParser(); p.add_argument('input',type=Path); p.add_argument('--out',type=Path,required=True); p.add_argument('--threshold',type=float); p.add_argument('--min-duration',type=float,default=5); p.add_argument('--merge-gap',type=float,default=2)
 a=p.parse_args(); df,_,_=load_any_recording(a.input); tc=detect_time_column(df); uc=detect_uap_column(df)
 if uc is None: raise SystemExit('No UAP channel detected.')
 t=pd.to_numeric(df[tc],errors='coerce').to_numpy(float); y=pd.to_numeric(df[uc],errors='coerce').to_numpy(float)
 th=a.threshold if a.threshold is not None else suggest_uap_threshold(t,y)['suggested_threshold']
 ev,_=detect_uap_events(t,y,th,a.min_duration,a.merge_gap); a.out.parent.mkdir(parents=True,exist_ok=True); ev.to_csv(a.out,index=False); print(f'{len(ev)} events; threshold={th:g}')
if __name__=='__main__': main()
