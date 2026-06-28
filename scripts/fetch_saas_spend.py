#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; SEED=DATA/'saas_spend_seed.json'; OUT=DATA/'saas_spend.json'
def main():
    DATA.mkdir(parents=True,exist_ok=True); snap=json.loads(SEED.read_text()); vendors=snap['vendors']; total=sum(v['annual_cost'] for v in vendors); low=[v for v in vendors if v['utilization_pct']<50]; dup={}
    for v in vendors: dup.setdefault(v['category'],[]).append(v['vendor'])
    dup={k:v for k,v in dup.items() if len(v)>1}; snap['generated_at']=datetime.utcnow().replace(microsecond=0).isoformat()+'Z'; snap['summary']={'vendor_count':len(vendors),'annual_spend':total,'low_utilization_count':len(low),'duplicate_categories':dup}
    OUT.write_text(json.dumps(snap,indent=2)); print(json.dumps({'ok':True,'vendors':len(vendors),'annual_spend':total,'low_utilization_count':len(low),'output':str(OUT)},indent=2))
if __name__=='__main__': main()
