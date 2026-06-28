#!/usr/bin/env python3
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
steps=[['python3','scripts/fetch_saas_spend.py'],['python3','scripts/run_moa_saas_audit.py'],['python3','scripts/run_business_ops.py'],['python3','scripts/render_site.py']]
for step in steps:
    print('$',' '.join(step)); r=subprocess.run(step,cwd=str(ROOT),text=True,capture_output=True,timeout=600); print(r.stdout);
    if r.stderr: print(r.stderr,file=sys.stderr)
    if r.returncode: sys.exit(r.returncode)
print('Otto Procurement cycle complete.')
