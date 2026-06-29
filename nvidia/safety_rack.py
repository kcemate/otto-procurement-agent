#!/usr/bin/env python3
"""NemoClaw-compatible safety instrumentation for Otto Procurement Agent.

NemoClaw/OpenShell is not installed in this public demo runtime. This module is
an honest, repo-visible compatibility scaffold: it records the checks a
production NemoClaw policy would enforce before any procurement action executes.
The demo remains dry-run and approval-gated.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def evaluate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    has_rollback = bool(manifest.get("rollback"))
    is_dry_run = manifest.get("mode") == "dry_run"
    approval_required = bool(manifest.get("approval_required"))
    signature_present = str(manifest.get("signature", "")).startswith("dryrun_")
    allowed = has_rollback and is_dry_run and approval_required and signature_present
    return {
        "action_id": manifest.get("action_id"),
        "step": manifest.get("step"),
        "decision": "prepared_for_human_approval" if allowed else "blocked_until_controls_pass",
        "checks": {
            "scope_check": is_dry_run,
            "rollback_present": has_rollback,
            "human_approval_required": approval_required,
            "dry_run_signature_present": signature_present,
            "rate_limit_policy": "max_autonomous_ops_spend_5000c",
        },
    }


def main() -> None:
    evidence = json.loads((DATA / "evidence_pack.json").read_text())
    nemotron = json.loads((DATA / "nemotron_risk_review.json").read_text()) if (DATA / "nemotron_risk_review.json").exists() else {}
    manifests = evidence.get("dry_run_manifests", [])
    evaluations = [evaluate_manifest(m) for m in manifests]
    blocked = [
        {
            "action": b.get("action"),
            "decision": b.get("decision", "blocked"),
            "risk_reason": b.get("why"),
            "nemotron_verdict": nemotron.get("verdict"),
            "nemotron_model": nemotron.get("model"),
        }
        for b in evidence.get("blocked_recommendations", [])
    ]
    report = {
        "generated_at": now(),
        "runtime": "NemoClaw-compatible safety instrumentation scaffold",
        "runtime_installed": False,
        "runtime_status": "scaffold_only_not_production_nemoclaw",
        "disclosure": "NemoClaw/OpenShell is not installed in this demo runtime; live customer-facing changes remain blocked behind human approval.",
        "policy_checks": [
            "scope_check",
            "rate_limit_policy",
            "rollback_present",
            "human_approval_required",
            "dry_run_signature_present",
        ],
        "manifest_evaluations": evaluations,
        "blocked_recommendations": blocked,
        "summary": {
            "manifests_checked": len(evaluations),
            "prepared_for_human_approval": sum(1 for e in evaluations if e["decision"] == "prepared_for_human_approval"),
            "blocked_recommendations": len(blocked),
        },
    }
    (DATA / "nemoclaw_safety_rack.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"ok": True, "runtime_installed": False, "manifests_checked": len(evaluations), "output": str(DATA / "nemoclaw_safety_rack.json")}, indent=2))


if __name__ == "__main__":
    main()
