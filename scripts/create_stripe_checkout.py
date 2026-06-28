#!/usr/bin/env python3
"""Create a real Stripe test Checkout Session when STRIPE_SECRET_KEY is available.
Falls back to the signed local test event used by the public demo when no key is configured.
"""
import json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'
def main():
    audit=json.loads((DATA/'audit.json').read_text())
    fee_cents=int(round(audit['success_fee_amount']*100))
    key=os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('STRIPE_API_KEY')
    if not key:
        ledger=json.loads((DATA/'ledger.json').read_text())
        print(json.dumps({'mode':ledger['payment']['mode'],'reason':'No STRIPE_SECRET_KEY in runtime; using signed local test event.','amount_cents':fee_cents,'payment_link':ledger['payment'].get('payment_link')},indent=2))
        return
    if key.startswith('sk_live_'):
        raise SystemExit('Refusing live Stripe key without explicit approval.')
    cmd=['stripe','checkout','sessions','create','--api-key',key,'--mode','payment','--success-url','https://kcemate.github.io/otto-procurement-agent/?checkout=success','--cancel-url','https://kcemate.github.io/otto-procurement-agent/?checkout=cancel','--line-items[0][price_data][currency]','usd','--line-items[0][price_data][product_data][name]','Otto Procurement savings success fee','--line-items[0][price_data][unit_amount]',str(fee_cents),'--line-items[0][quantity]','1']
    out=subprocess.check_output(cmd,text=True)
    print(out)
if __name__=='__main__': main()
