#!/usr/bin/env python3
"""Instrument the acceleration path honestly: detect NVIDIA if present, otherwise record CPU fallback.
The business point is deployment readiness for private/local inference over procurement data.
"""
import json, platform, shutil, subprocess, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def nvidia():
    if not shutil.which('nvidia-smi'):
        return {'available':False,'reason':'nvidia-smi not found on this runner'}
    try:
        out=subprocess.check_output(['nvidia-smi','--query-gpu=name,memory.total','--format=csv,noheader'],text=True,timeout=5)
        return {'available':True,'devices':[x.strip() for x in out.splitlines() if x.strip()]}
    except Exception as e:
        return {'available':False,'reason':type(e).__name__}
def cpu_work():
    # Deterministic light workload approximating local embedding/vector reconciliation bookkeeping.
    start=time.perf_counter(); total=0
    for i in range(1,120000): total=(total+(i*i)%9973)%1000000007
    elapsed=time.perf_counter()-start
    return {'elapsed_seconds':round(elapsed,4),'checksum':total,'ops_per_second':round(120000/elapsed,1)}
def main():
    report={'generated_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'host':platform.platform(),'nvidia':nvidia(),'cpu_fallback_benchmark':cpu_work(),'deployment_story':'Procurement evidence contains contracts, pricing and vendor terms. The production path is local/private inference on NVIDIA-class hardware; this runner records CPU fallback when no NVIDIA GPU is attached.'}
    (DATA/'lab_readiness.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
if __name__=='__main__': main()
