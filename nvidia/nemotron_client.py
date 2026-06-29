#!/usr/bin/env python3
"""Nemotron 3 Ultra risk-review lane for Otto Procurement Agent.

This calls the Ollama OpenAI-compatible endpoint using the configured
`nemotron-3-ultra:cloud` model. It is intentionally scoped to the Risk Reviewer
role: determine whether a proposed procurement action should be allowed,
blocked, or escalated.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
MODEL = "nemotron-3-ultra:cloud"
OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def extract_json(text: str) -> dict[str, Any]:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("Nemotron response did not contain JSON")
    return json.loads(match.group(0))


def call_nemotron(prompt: str, timeout: int = 180) -> tuple[str, float]:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are the NVIDIA Nemotron 3 Ultra risk reviewer inside a Hermes MoA. "
                    "Return only compact JSON. Do not approve destructive actions without evidence, "
                    "rollback, owner, and human approval."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
        "max_tokens": 900,
    }
    started = time.perf_counter()
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode(),
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = json.loads(response.read().decode())
    elapsed = time.perf_counter() - started
    content = raw["choices"][0]["message"]["content"]
    return content, elapsed


def fallback_review(reason: str) -> dict[str, Any]:
    return {
        "generated_at": now(),
        "role": "risk_reviewer",
        "model": f"ollama-launch:{MODEL}",
        "provider": "ollama_openai_compatible",
        "status": "fallback",
        "verdict": "block",
        "reason": (
            "Fallback risk posture: block unsafe Slack reduction and require human approval "
            f"because Nemotron call failed: {reason}"
        ),
        "blocked_action": "Cancel Slack Enterprise add-ons",
        "required_controls": [
            "legal_hold_check",
            "owner_approval",
            "rollback_plan",
            "human_approval_before_live_change",
        ],
        "latency_seconds": None,
        "raw_excerpt": "",
    }


def main() -> None:
    DATA.mkdir(exist_ok=True)
    audit = json.loads((DATA / "audit.json").read_text())
    blocked = {
        "candidate_action": "Cancel Slack Enterprise add-ons",
        "tempting_savings": 9360,
        "known_risks": [
            "12 channels under active legal hold",
            "executive workspace automation depends on enterprise workflow add-ons",
            "security retention requirements are unresolved",
        ],
        "available_controls": [
            "dry-run only",
            "signed rollback path",
            "human approval required before live change",
        ],
    }
    prompt = (
        "Review this procurement action as the Risk Reviewer in a SaaS savings MoA. "
        "Return JSON with keys generated_at, role, model, status, verdict, reason, "
        "blocked_action, required_controls. Use verdict=block/allow/escalate.\n\n"
        f"Audit headline: {audit['headline']}\n"
        f"Candidate action: {json.dumps(blocked, indent=2)}"
    )
    try:
        text, elapsed = call_nemotron(prompt)
        parsed = extract_json(text)
        parsed.update(
            {
                "generated_at": parsed.get("generated_at") or now(),
                "role": "risk_reviewer",
                "model": f"ollama-launch:{MODEL}",
                "provider": "ollama_openai_compatible",
                "status": "ok",
                "latency_seconds": round(elapsed, 3),
                "raw_excerpt": text[:1000],
            }
        )
    except Exception as exc:  # honest fallback for network/model errors
        parsed = fallback_review(repr(exc))
    (DATA / "nemotron_risk_review.json").write_text(json.dumps(parsed, indent=2))
    print(json.dumps({"ok": parsed["status"] == "ok", "model": parsed["model"], "verdict": parsed["verdict"], "latency_seconds": parsed.get("latency_seconds"), "output": str(DATA / "nemotron_risk_review.json")}, indent=2))


if __name__ == "__main__":
    main()
