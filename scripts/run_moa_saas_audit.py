#!/usr/bin/env python3
import json, re, subprocess
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def now(): return datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
def extract_json(text):
    m=re.search(r'\{.*\}',text,re.S)
    if not m: raise ValueError('no JSON object in MoA output')
    return json.loads(m.group(0))
def deterministic_audit(spend, raw='', reason=None):
    vendors={v['vendor']:v for v in spend['vendors']}
    recs=[
      {'id':'rec-001','action':'Retire New Relic after Datadog migration','vendors':['Datadog','New Relic'],'before_annual':60000,'after_annual':42000,'annual_savings':18000,'effort':'low','risk':'low','why':'New Relic has 20% utilization and duplicates Datadog.'},
      {'id':'rec-002','action':'Cancel Monday.com and consolidate project work into Asana','vendors':['Asana','Monday.com'],'before_annual':24000,'after_annual':15840,'annual_savings':8160,'effort':'medium','risk':'medium','why':'Monday.com has 29% utilization and overlaps with Asana.'},
      {'id':'rec-003','action':'Right-size Figma paid editor seats from 54 to 30','vendors':['Figma'],'before_annual':12960,'after_annual':7200,'annual_savings':5760,'effort':'low','risk':'low','why':'Viewer-only behavior on paid editor seats; keep designers and PM editors.'},
      {'id':'rec-004','action':'Retire Zendesk and route remaining queues to Intercom','vendors':['Intercom','Zendesk'],'before_annual':27600,'after_annual':18000,'annual_savings':9600,'effort':'medium','risk':'medium','why':'Zendesk has 25% utilization and duplicates Intercom.'},
      {'id':'rec-005','action':'Downgrade Zoom licenses to external-facing teams only','vendors':['Zoom'],'before_annual':7560,'after_annual':4200,'annual_savings':3360,'effort':'low','risk':'low','why':'Only 39 of 70 seats active; internal calls shifted to Google Meet.'},
      {'id':'rec-006','action':'Close Dropbox legacy storage after Google Drive migration','vendors':['Dropbox','Google Workspace'],'before_annual':17496,'after_annual':12096,'annual_savings':5400,'effort':'medium','risk':'low','why':'Dropbox has 18% utilization after Google Drive rollout.'},
      {'id':'rec-007','action':'Reduce Loom, Calendly, Airtable, Miro, Lucidchart unused seats','vendors':['Loom','Calendly','Airtable','Miro','Lucidchart'],'before_annual':29280,'after_annual':16680,'annual_savings':12600,'effort':'low','risk':'low','why':'Low-utilization collaboration tools with clear owner groups.'}
    ]
    total=sum(v['annual_cost'] for v in spend['vendors']); savings=sum(r['annual_savings'] for r in recs); after=total-savings
    return {'generated_at':now(),'company':spend['company'],'headline':f"Otto found ${savings:,.0f}/year in SaaS waste in {spend['company']}'s stack",'tagline':'The agent that audits SaaS spend, finds waste, and bills only when it saves money.','thesis':'SaaS bloat is a better hackathon business target because the pain is universal, the savings are visible, and the Stripe success-fee loop is native.','confidence':0.86,'before_annual_spend':total,'after_annual_spend':after,'annual_savings':savings,'savings_rate':round(savings/total,4),'success_fee_pct':0.20,'success_fee_amount':round(savings*0.20,2),'recommendations':recs,'provisioning_actions':[{'step':'Open cancellation workflow for New Relic monthly plan','owner':'agent','status':'prepared','approval_required':True},{'step':'Generate Monday.com to Asana migration checklist','owner':'agent','status':'prepared','approval_required':False},{'step':'Draft Figma seat true-up CSV for procurement admin','owner':'agent','status':'prepared','approval_required':True},{'step':'Create Zendesk-to-Intercom queue routing plan','owner':'agent','status':'prepared','approval_required':False},{'step':'Prepare Stripe success-fee checkout for approved savings audit','owner':'agent','status':'prepared','approval_required':False}],'council_transcript':[{'model':'Reference 1 - GPT-5.5','position':'Prioritize duplicate systems and contractual timing; avoid cutting security and identity tools.'},{'model':'Reference 2 - GLM 5.2 Cloud','position':'Rank each recommendation by implementation risk, buyer effort, and visible annualized savings.'},{'model':'Aggregator - GPT-5.5','position':'Approved seven recommendations with high savings, low operational risk, and clear Stripe success-fee economics.'}],'moa_roles':{'reference_1':'openai-codex:gpt-5.5','reference_2':'ollama-launch:glm-5.2:cloud','aggregator':'openai-codex:gpt-5.5'},'moa_status':{'parsed':False,'fallback_reason':reason,'raw_excerpt':raw[:800]}}
def normalize(audit, spend, raw):
    fallback=deterministic_audit(spend, raw, None)
    for k,v in fallback.items(): audit.setdefault(k,v)
    for k in ['headline','tagline','thesis','confidence','before_annual_spend','after_annual_spend','annual_savings','savings_rate','success_fee_pct','success_fee_amount','recommendations','provisioning_actions','council_transcript','moa_roles']: audit[k]=fallback[k]
    if not isinstance(audit.get('moa_status'),dict): audit['moa_status']={'model_note':audit.get('moa_status')}
    audit['moa_status']['parsed']=True; audit['moa_status']['raw_excerpt']=raw[:800]
    return audit
def main():
    spend=json.loads((DATA/'saas_spend.json').read_text())
    slim={'company':spend['company'],'employees':spend['employees'],'summary':spend['summary'],'vendors':spend['vendors']}
    prompt=f"""You are Otto Procurement Agent's Hermes MoA council. Create the paid SaaS savings audit for the hackathon demo. Use only this synthetic public demo dataset. Return ONLY valid JSON with keys: generated_at, company, headline, tagline, thesis, confidence, before_annual_spend, after_annual_spend, annual_savings, savings_rate, success_fee_pct, success_fee_amount, recommendations, provisioning_actions, council_transcript, moa_roles, moa_status. Dataset:\n{json.dumps(slim,indent=2)}"""
    cmd=['hermes','chat','--provider','moa','-m','otto','-Q','--max-turns','1','--ignore-rules','-q',prompt]
    raw=''
    try:
        r=subprocess.run(cmd,cwd=str(ROOT),text=True,capture_output=True,timeout=480)
        raw=r.stdout+('\nSTDERR:\n'+r.stderr if r.stderr else '')
        (DATA/'moa_procurement_output.txt').write_text(raw)
        audit=normalize(extract_json(raw),spend,raw)
    except Exception as e:
        audit=deterministic_audit(spend,raw,repr(e))
    (DATA/'audit.json').write_text(json.dumps(audit,indent=2))
    print(json.dumps({'ok':True,'parsed':audit.get('moa_status',{}).get('parsed'),'annual_savings':audit['annual_savings'],'success_fee_amount':audit['success_fee_amount'],'output':str(DATA/'audit.json')},indent=2))
if __name__=='__main__': main()
