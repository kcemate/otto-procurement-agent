#!/usr/bin/env python3
"""Build canonical proof artifacts for the reframed Procurement Profit Agent."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def read_json(name: str) -> dict:
    return json.loads((DATA / name).read_text())


def main() -> None:
    audit = read_json("audit.json")
    ledger = read_json("ledger.json")
    evidence = read_json("evidence_pack.json")
    nemotron = read_json("nemotron_risk_review.json")
    safety = read_json("nemoclaw_safety_rack.json")
    nvidia = read_json("nvidia_integrations.json")
    skills = read_json("nvidia_skills_access.json")

    proof = {
        "generated_at": now(),
        "product_name": "Otto Procurement Profit Agent",
        "hook": "A Nemotron-governed Hermes agent business that finds SaaS waste, gates risky actions, and books a capped Stripe test/local success fee.",
        "scope": {
            "data_mode": "synthetic replay",
            "stripe_mode": ledger["payment"]["mode"],
            "real_customer_data": False,
            "real_revenue_claimed": False,
            "nemoclaw_runtime_installed": safety.get("runtime_installed", False),
            "local_nvidia_gpu": nvidia.get("nvidia_gpu", {}).get("available", False),
        },
        "verified_numbers": {
            "synthetic_annual_spend": audit["before_annual_spend"],
            "synthetic_annual_savings": audit["annual_savings"],
            "local_test_success_fee": audit["success_fee_amount"],
            "modeled_run_cost": evidence["agent_pnl"]["agent_operating_cost"],
            "customer_net_first_year_value": evidence["agent_pnl"]["customer_net_first_year_value"],
            "contribution_margin": evidence["agent_pnl"]["contribution_margin"],
            "nvidia_skills_discovered": skills.get("found_count"),
            "nemotron_latency_seconds": nemotron.get("latency_seconds"),
        },
        "nvidia": {
            "nemotron_model": nemotron.get("model"),
            "nemotron_role": "Risk Reviewer",
            "nemotron_status": nemotron.get("status"),
            "nemotron_verdict": nemotron.get("verdict"),
            "nvidia_skills_count": skills.get("found_count"),
            "nvidia_gpu_status": nvidia.get("nvidia_gpu"),
            "nemoclaw_status": safety.get("runtime_status"),
            "nemoclaw_disclosure": safety.get("disclosure"),
        },
    }

    safety_events = []
    for event in safety.get("manifest_evaluations", []):
        safety_events.append({
            "kind": "manifest_gate",
            "action_id": event.get("action_id"),
            "step": event.get("step"),
            "decision": event.get("decision"),
            "checks": event.get("checks", {}),
        })
    for blocked in evidence.get("blocked_recommendations", []):
        safety_events.append({
            "kind": "nemotron_risk_block",
            "action": blocked.get("action"),
            "decision": blocked.get("decision"),
            "reason": blocked.get("why"),
            "nemotron_verdict": nemotron.get("verdict"),
            "model": nemotron.get("model"),
        })
    safety_log = {
        "generated_at": now(),
        "runtime": safety.get("runtime"),
        "runtime_installed": safety.get("runtime_installed"),
        "disclosure": safety.get("disclosure"),
        "events": safety_events,
    }

    treasury = {
        "generated_at": now(),
        "mode": ledger["payment"]["mode"],
        "disclosure": "Stripe is test/local in this public demo; no real revenue is claimed.",
        "success_fee_event": ledger.get("stripe_event"),
        "safety_limits": ledger.get("safety_limits"),
        "entries": ledger.get("entries"),
        "ending_balance_cents": ledger.get("balance_cents"),
        "payment": ledger.get("payment"),
    }

    (DATA / "proof.json").write_text(json.dumps(proof, indent=2))
    (DATA / "safety_log.json").write_text(json.dumps(safety_log, indent=2))
    (DATA / "treasury.json").write_text(json.dumps(treasury, indent=2))
    print(json.dumps({"ok": True, "proof": str(DATA / "proof.json"), "safety_events": len(safety_events), "treasury_mode": treasury["mode"]}, indent=2))


if __name__ == "__main__":
    main()
