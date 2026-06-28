#!/usr/bin/env python3
import hashlib,hmac,json,os,time,urllib.parse,urllib.request
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; LOCAL_DEMO_SIGNING_SALT='not-a-real-secret-demo-salt'
def now(): return datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
def stripe_api(path,payload,key):
    req=urllib.request.Request('https://api.stripe.com'+path,data=urllib.parse.urlencode(payload).encode(),method='POST'); req.add_header('Authorization','Bearer '+key); req.add_header('Content-Type','application/x-www-form-urlencoded'); return json.loads(urllib.request.urlopen(req,timeout=30).read().decode())
def payment_link(audit):
    key=os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_API_KEY') or ''; fee_cents=round(audit['success_fee_amount']*100)
    if key.startswith('sk_test_'):
        product=stripe_api('/v1/products',{'name':'Otto Procurement SaaS Savings Audit','description':audit['headline']},key); price=stripe_api('/v1/prices',{'unit_amount':fee_cents,'currency':'usd','product':product['id']},key); link=stripe_api('/v1/payment_links',{'line_items[0][price]':price['id'],'line_items[0][quantity]':1,'metadata[annual_savings]':str(audit['annual_savings']),'metadata[success_fee_pct]':str(audit['success_fee_pct'])},key); return {'mode':'stripe_test_payment_link','payment_link':link.get('url'),'product_id':product['id'],'price_id':price['id'],'amount_cents':fee_cents}
    if key.startswith('sk_live_'): return {'mode':'blocked_live_key','payment_link':None,'reason':'Live Stripe key detected; creation blocked without explicit approval.','amount_cents':fee_cents}
    return {'mode':'local_stripe_style_test_event','payment_link':None,'reason':'No Stripe test secret in runtime; using signed local checkout.session.completed event.','amount_cents':fee_cents}
def main():
    audit=json.loads((DATA/'audit.json').read_text()); pay=payment_link(audit); fee_cents=pay['amount_cents']
    event={'id':'evt_otto_procurement_'+str(int(time.time())),'type':'checkout.session.completed','created':int(time.time()),'livemode':False,'data':{'object':{'id':'cs_test_otto_procurement','amount_total':fee_cents,'currency':'usd','customer_email':'buyer@example.com','metadata':{'annual_savings':str(audit['annual_savings']),'success_fee_pct':str(audit['success_fee_pct']),'company':audit['company']}}}}
    event['local_signature']=hmac.new(LOCAL_DEMO_SIGNING_SALT.encode(),json.dumps(event,sort_keys=True).encode(),hashlib.sha256).hexdigest()
    costs=[('MoA council SaaS audit',-1850),('Spend ingestion and normalization',-420),('Provisioning plan generation',-960),('Static hosting allocation',-190)]; reserve=-50000
    entries=[{'type':'revenue','label':'Success-fee checkout: 20% of first-year savings','amount_cents':fee_cents,'source':event['id'],'timestamp':now()}]+[{'type':'spend','label':l,'amount_cents':a,'approved_by':'policy:max_autonomous_ops_spend_5000c','timestamp':now()} for l,a in costs]+[{'type':'reserve','label':'Reinvested into next SaaS audit cycle','amount_cents':reserve,'approved_by':'policy:retain_positive_balance','timestamp':now()}]
    ledger={'generated_at':now(),'business':'Otto Procurement Agent','currency':'usd','payment':pay,'safety_limits':{'max_autonomous_ops_spend_cents':5000,'live_spend_requires_human_approval':True,'public_demo_dataset':True},'stripe_event':event,'entries':entries,'balance_cents':sum(e['amount_cents'] for e in entries),'gross_margin_cents_before_reinvestment':fee_cents+sum(a for _,a in costs),'delivery_status':'audit_and_provisioning_plan_prepared'}
    (DATA/'ledger.json').write_text(json.dumps(ledger,indent=2))
    delivery=f"# Buyer delivery payload\n\n**{audit['headline']}**\n\nAnnual SaaS spend before: ${audit['before_annual_spend']:,.0f}\nAnnual SaaS spend after: ${audit['after_annual_spend']:,.0f}\nIdentified savings: ${audit['annual_savings']:,.0f}\nSuccess fee: ${audit['success_fee_amount']:,.2f}\n\n## Recommended actions\n"+''.join(f"- **{r['action']}** — saves ${r['annual_savings']:,.0f}/yr. Effort: {r['effort']}. Risk: {r['risk']}. {r['why']}\n" for r in audit['recommendations'])+"\n## Provisioning queue\n"+''.join(f"- {a['status']}: {a['step']} (approval_required={a['approval_required']})\n" for a in audit['provisioning_actions'])+f"\nDelivered by Otto Procurement Agent. Payment/event: `{event['id']}`.\n"
    (DATA/'delivery_payload.md').write_text(delivery)
    print(json.dumps({'ok':True,'payment_mode':pay['mode'],'success_fee_cents':fee_cents,'balance_cents':ledger['balance_cents'],'ledger':str(DATA/'ledger.json')},indent=2))
if __name__=='__main__': main()
