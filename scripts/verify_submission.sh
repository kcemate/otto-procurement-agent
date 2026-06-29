#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1] if '__file__' in globals() else Path.cwd()
# When run as bash script, cwd should be repo root.
root=Path.cwd()

def j(path):
    return json.loads((root/path).read_text())

audit=j(Path('data/audit.json'))
ledger=j(Path('data/ledger.json'))
evidence=j(Path('data/evidence_pack.json'))
nemotron=j(Path('data/nemotron_risk_review.json'))
safety=j(Path('data/nemoclaw_safety_rack.json'))
skills=j(Path('data/nvidia_skills_access.json'))
proof=j(Path('data/proof.json'))
assert audit['before_annual_spend'] == 235416, audit['before_annual_spend']
assert audit['annual_savings'] == 62880, audit['annual_savings']
assert int(audit['success_fee_amount']) == 12576, audit['success_fee_amount']
assert abs(evidence['agent_pnl']['agent_operating_cost'] - 34.2) < 0.001
assert nemotron['model'] == 'ollama-launch:nemotron-3-ultra:cloud'
assert nemotron['status'] == 'ok'
assert skills['found_count'] == 225
assert safety['runtime_installed'] is False
assert proof['scope']['real_customer_data'] is False
assert proof['scope']['real_revenue_claimed'] is False
assert ledger['payment']['mode'] in {'local_stripe_style_test_event', 'stripe_test_payment_link'}
print('json_claims_ok')
PY

node --check site/app.js >/dev/null
python3 -m json.tool site/data.json >/dev/null
python3 -m json.tool docs/data.json >/dev/null

if grep -RInE --exclude='verify_submission.sh' 'NemoClaw is running|NemoClaw protected this in production|real customer payment collected|real revenue generated|local NVIDIA GPU inference ran' README.md submission site docs data scripts nvidia 2>/tmp/otto_forbidden_hits; then
  echo 'Forbidden positive claim found:' >&2
  cat /tmp/otto_forbidden_hits >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
for p, limit in [('submission/discord_submission.md',1800), ('submission/x_reply.md',600)]:
    txt=Path(p).read_text()
    assert len(txt) <= limit, (p, len(txt), limit)
    print(f'{p}_chars={len(txt)}')
PY

echo 'submission_verify_ok'
