#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SITE = ROOT / "site"
DOCS = ROOT / "docs"


def money(n: float | int) -> str:
    if n is None:
        return "n/a"
    return "$" + format(float(n), ",.0f")


def cents(c: int | float | None) -> str:
    if c is None:
        return "n/a"
    sign = "-" if c < 0 else ""
    return sign + "$" + format(abs(c) / 100, ",.2f")


def read_json(name: str, fallback=None):
    p = DATA / name
    if not p.exists():
        return fallback if fallback is not None else {}
    return json.loads(p.read_text())


def main() -> None:
    SITE.mkdir(exist_ok=True)
    DOCS.mkdir(exist_ok=True)

    audit = read_json("audit.json")
    ledger = read_json("ledger.json")
    evidence = read_json("evidence_pack.json")
    nvidia = read_json("nvidia_integrations.json")
    proof = read_json("proof.json")
    safety_log = read_json("safety_log.json")
    treasury = read_json("treasury.json")

    site_data = {
        "audit": audit,
        "ledger": ledger,
        "evidence": evidence,
        "nvidia": nvidia,
        "proof": proof,
        "safety_log": safety_log,
        "treasury": treasury,
        "format": {
            "spend": money(audit.get("before_annual_spend")),
            "savings": money(audit.get("annual_savings")),
            "fee": money(audit.get("success_fee_amount")),
            "run_cost": money((evidence.get("agent_pnl") or {}).get("agent_operating_cost")),
            "balance": cents(ledger.get("balance_cents")),
        },
    }

    (SITE / "data.json").write_text(json.dumps(site_data, indent=2))
    (SITE / "index.html").write_text(INDEX)
    (SITE / "styles.css").write_text(STYLES)
    (SITE / "app.js").write_text(APP)

    for asset in ("index.html", "styles.css", "app.js", "data.json"):
        shutil.copy2(SITE / asset, DOCS / asset)
    (DOCS / ".nojekyll").write_text("")

    print(json.dumps({"ok": True, "site": str(SITE / "index.html"), "docs": str(DOCS / "index.html"), "data": str(SITE / "data.json")}, indent=2))


INDEX = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Otto Procurement Profit Agent</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">Nous × NVIDIA × Stripe Hermes Agent Hackathon</p>
      <h1>Otto Procurement Profit Agent</h1>
    </div>
    <div class="badge">synthetic replay · test/local treasury</div>
  </header>

  <main>
    <section class="hero card">
      <div>
        <p class="eyebrow">Nemotron-governed procurement twin</p>
        <h2>Agent-run business loop: find waste → review risk → gate actions → book a success fee.</h2>
        <p class="lede">Otto is not just a SaaS audit dashboard. It is a replayable Hermes business agent that earns through synthetic savings, spends under policy, and makes unsafe procurement actions visible before they can execute.</p>
        <div class="cta-row">
          <button id="replayBtn">Replay the proof trail</button>
          <span>Human approval required before live customer-facing changes.</span>
        </div>
      </div>
      <div class="metric-grid">
        <article><span>Synthetic spend audited</span><b id="spend">--</b></article>
        <article><span>Synthetic savings found</span><b id="savings">--</b></article>
        <article><span>Stripe test/local success fee</span><b id="fee">--</b></article>
        <article><span>Modeled agent run cost</span><b id="runCost">--</b></article>
      </div>
    </section>

    <section class="proof-strip">
      <article><b>Hermes MoA</b><p>GPT-5.5 + GLM + Nemotron roles challenge savings, finance, IT, and risk.</p></article>
      <article><b>Nemotron 3 Ultra</b><p id="nemotronCard">Risk reviewer loading…</p></article>
      <article><b>NemoClaw-compatible gate</b><p id="clawCard">Safety disclosure loading…</p></article>
      <article><b>Stripe loop</b><p id="stripeCard">Treasury loading…</p></article>
    </section>

    <section class="grid2">
      <article class="card" id="policyGate">
        <p class="eyebrow">Visible safety layer</p>
        <h2>Approve/block policy gate</h2>
        <p class="small">This demo does not claim NVIDIA NemoClaw runtime is installed. It shows a NemoClaw-compatible scaffold: scope checks, rollback checks, rate limits, dry-run signatures, and human approval gates.</p>
        <div id="safetyEvents" class="timeline"></div>
      </article>

      <article class="card">
        <p class="eyebrow">Treasury / P&L</p>
        <h2>Earns, spends, reconciles</h2>
        <p class="small">Stripe remains test/local in this public demo. No real revenue or real customer payment is claimed.</p>
        <div id="treasuryEntries" class="ledger"></div>
      </article>
    </section>

    <section class="card" id="evidenceSection">
      <div class="section-head">
        <div>
          <p class="eyebrow">Evidence cards</p>
          <h2>Every dollar has a fingerprint</h2>
        </div>
        <span id="generated">loading</span>
      </div>
      <div id="evidenceCards" class="cards"></div>
    </section>

    <section class="card replay">
      <p class="eyebrow">Replay mode</p>
      <h2>Deterministic audit trail</h2>
      <div id="runLog" class="timeline"></div>
    </section>

    <section class="card honest">
      <p class="eyebrow">Honest scope</p>
      <h2>Aggressive demo, clean claims</h2>
      <ul>
        <li>Synthetic SaaS spend and usage evidence.</li>
        <li>Stripe success-fee loop is local/test-mode unless a test key is configured.</li>
        <li>Nemotron 3 Ultra via Ollama Cloud is real and recorded.</li>
        <li>NVIDIA skills catalog discovery is real and recorded.</li>
        <li>NemoClaw-compatible policy instrumentation is scaffolded; production NemoClaw runtime is not claimed as installed.</li>
      </ul>
    </section>
  </main>

  <footer>Built with Hermes Agent, Nemotron 3 Ultra, NVIDIA skills catalog proof, and Stripe test/local economics.</footer>
  <script src="app.js"></script>
</body>
</html>
"""

STYLES = """
:root{--bg:#070b17;--panel:#0f172a;--panel2:#111827;--line:#334155;--text:#f8fafc;--muted:#cbd5e1;--gold:#ffd166;--green:#86efac;--blue:#93c5fd;--red:#fca5a5}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#172554 0,#070b17 38%,#05070f 100%);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main,.topbar,footer{max-width:1220px;margin:auto}.topbar{display:flex;justify-content:space-between;gap:24px;align-items:center;padding:34px 20px 18px}.eyebrow{text-transform:uppercase;letter-spacing:.15em;font-size:12px;font-weight:900;color:var(--gold);margin:0 0 10px}h1{font-size:48px;line-height:.94;letter-spacing:-.05em;margin:0}h2{font-size:34px;letter-spacing:-.04em;line-height:1.08;margin:0 0 14px}h3{margin:0 0 8px}.badge{border:1px solid var(--green);background:#052e1a;border-radius:999px;padding:10px 14px;font-weight:900;color:#dcfce7}.card,.proof-strip article{background:linear-gradient(180deg,rgba(17,24,39,.96),rgba(15,23,42,.96));border:1px solid rgba(148,163,184,.35);border-radius:26px;box-shadow:0 24px 80px rgba(0,0,0,.35)}.hero{display:grid;grid-template-columns:1.35fr .9fr;gap:26px;margin:10px 20px 20px;padding:34px}.lede{font-size:19px;line-height:1.55;color:#e5e7eb;max-width:820px}.cta-row{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:24px}.cta-row button{border:0;background:var(--gold);color:#111827;border-radius:999px;padding:14px 20px;font-weight:950}.cta-row span,.small{color:var(--muted);line-height:1.5}.metric-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.metric-grid article{border:1px solid var(--line);border-radius:18px;padding:18px;background:#0b1224}.metric-grid span{display:block;color:var(--muted);font-size:13px;font-weight:800}.metric-grid b{display:block;color:var(--green);font-size:34px;margin-top:8px}.proof-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:20px}.proof-strip article{padding:20px}.proof-strip b{color:var(--blue)}.proof-strip p{color:#e5e7eb;line-height:1.42}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:20px}.grid2 .card,.card.replay,.card.honest,#evidenceSection{padding:26px;margin:20px}.section-head{display:flex;justify-content:space-between;gap:16px;align-items:end}.section-head span{color:var(--muted);font-weight:800}.timeline{display:grid;gap:10px;margin-top:16px}.event,.runitem,.line{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:start;border:1px solid var(--line);background:#0b1224;border-radius:14px;padding:12px}.event b,.runitem b{color:var(--blue)}.ok{color:var(--green)}.block,.neg{color:var(--red)}.warn{color:var(--gold)}.ledger{display:grid;gap:10px;margin-top:16px}.line{grid-template-columns:1fr auto}.line small{display:block;color:var(--muted);margin-top:3px}.cards{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:18px}.evidence{border:1px solid var(--line);background:#0b1224;border-radius:18px;padding:18px}.evidence-top{display:flex;justify-content:space-between;gap:14px}.saving{font-size:26px;color:var(--green);font-weight:950}.tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.tags span{border:1px solid #475569;border-radius:999px;padding:5px 8px;color:#e2e8f0;font-size:12px;font-weight:800}.honest ul{margin:0;padding-left:20px;color:#e5e7eb;line-height:1.7}footer{padding:28px 20px 50px;color:var(--muted);text-align:center}@media(max-width:900px){.hero,.grid2,.proof-strip,.cards{grid-template-columns:1fr}.topbar{display:block}.metric-grid{grid-template-columns:1fr}h1{font-size:38px}h2{font-size:28px}}
"""

APP = r"""
// Safe in this static demo: data.json is generated from repo-local synthetic artifacts,
// not from user-submitted browser input. innerHTML is used only to render fixed proof data.
function money(n){return '$'+Number(n||0).toLocaleString(undefined,{maximumFractionDigits:0})}
function cents(c){var n=Number(c||0);var sign=n<0?'-':'';return sign+'$'+(Math.abs(n)/100).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2})}
function clsForDecision(d){d=(d||'').toLowerCase();if(d.includes('block'))return 'block';if(d.includes('escalate'))return 'warn';return 'ok'}
function el(id){return document.getElementById(id)}
function tagList(items){return '<div class="tags">'+items.map(x=>'<span>'+x+'</span>').join('')+'</div>'}
function boot(){fetch('data.json?ts='+Date.now()).then(r=>r.json()).then(data=>{
  const a=data.audit||{}, e=data.evidence||{}, n=data.nvidia||{}, proof=data.proof||{}, safety=data.safety_log||{}, treasury=data.treasury||{}, f=data.format||{};
  el('spend').textContent=f.spend; el('savings').textContent=f.savings; el('fee').textContent=f.fee; el('runCost').textContent=f.run_cost;
  const nem=(n.nemotron_3_ultra||{}), claw=(n.nemoclaw||{}), skills=(n.nvidia_skills||{});
  el('nemotronCard').innerHTML=(nem.model||'Nemotron 3 Ultra')+' returned <b class="'+clsForDecision(nem.verdict)+'">'+(nem.verdict||'n/a')+'</b>'+(nem.latency_seconds?' in '+nem.latency_seconds+'s':'')+'.';
  el('clawCard').textContent=(claw.status||'scaffold only')+'. '+(claw.runtime_installed?'Runtime installed.':'Runtime not installed/claimed.');
  el('stripeCard').textContent=(treasury.mode||((data.ledger||{}).payment||{}).mode||'test/local')+'; ending balance '+f.balance+'.';
  el('generated').textContent='Generated '+(proof.generated_at||a.generated_at||'');
  const events=(safety.events||[]).slice(0,8);
  el('safetyEvents').innerHTML=events.map((x,i)=>'<div class="event"><b>#'+(i+1)+'</b><span>'+(x.step||x.action||x.kind)+'<br><small>'+(x.reason||x.model||x.kind||'policy checks recorded')+'</small></span><b class="'+clsForDecision(x.decision||x.nemotron_verdict)+'">'+(x.decision||x.nemotron_verdict||'checked')+'</b></div>').join('');
  const entries=(treasury.entries||((data.ledger||{}).entries)||[]);
  el('treasuryEntries').innerHTML=entries.map(x=>'<div class="line"><span>'+x.label+'<small>'+(x.timestamp||x.approved_by||'')+'</small></span><b class="'+(Number(x.amount_cents)>=0?'ok':'neg')+'">'+cents(x.amount_cents)+'</b></div>').join('')+'<div class="line"><span><b>Ending treasury</b></span><b class="ok">'+f.balance+'</b></div>';
  el('evidenceCards').innerHTML=(e.evidence_cards||[]).map(r=>'<article class="evidence"><div class="evidence-top"><h3>'+r.action+'</h3><div class="saving">'+money(r.annual_savings)+'</div></div><p class="small">'+r.math+'</p><p class="small">'+(r.evidence||[]).map(ev=>'<b>'+ev.kind+':</b> '+ev.finding).join('<br>')+'</p>'+tagList(['fee if verified '+money(r.success_fee_if_verified),'risk '+r.risk,'approval required'])+'</article>').join('');
  el('runLog').innerHTML=(e.run_log||[]).map(x=>'<div class="runitem"><b>+'+x.t_plus_sec+'s</b><span>'+x.event+'</span><b class="ok">'+x.status+'</b></div>').join('');
  el('replayBtn').onclick=()=>{document.querySelector('.replay').scrollIntoView({behavior:'smooth'});document.querySelectorAll('.runitem').forEach((n,i)=>{n.style.opacity=.35;setTimeout(()=>{n.style.opacity=1;n.style.borderColor='#86efac'},i*170)})};
})}
boot();setInterval(boot,30000);
"""

if __name__ == "__main__":
    main()
