#!/usr/bin/env python3
from pathlib import Path
import argparse, json, sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from skna_framework.core import load_any_recording, preprocess_raw_recording, detect_ecg_columns

def main():
 p=argparse.ArgumentParser(description='Convert a raw LabChart TXT/ZIP recording to processed ECG/SKNA CSV.')
 p.add_argument('input',type=Path); p.add_argument('--out',type=Path,required=True)
 p.add_argument('--fs-out',type=float,default=100); p.add_argument('--hp',type=float,default=500)
 p.add_argument('--envelope',type=float,default=1.0); p.add_argument('--mad-clip-k',type=float,default=None)
 a=p.parse_args(); df,meta,kind=load_any_recording(a.input)
 if kind=='processed': out=df; proc={'note':'Input already contained processed SKNA; no preprocessing repeated.'}
 else:
  fs=float(meta.get('source_fs_hz',0));
  if fs<=0: raise SystemExit('Sampling rate could not be inferred from the raw file.')
  out,proc=preprocess_raw_recording(df,fs,detect_ecg_columns(df),a.fs_out,a.hp,a.envelope,mad_clip_k=a.mad_clip_k)
 a.out.parent.mkdir(parents=True,exist_ok=True); out.to_csv(a.out,index=False)
 (a.out.with_suffix('.manifest.json')).write_text(json.dumps({'input':str(a.input),'loader':meta,'processing':proc},indent=2,default=str))
 print(a.out)
if __name__=='__main__': main()
