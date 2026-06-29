#!/usr/bin/env python3
"""Probe NVIDIA/Nemotron integration evidence for the public demo."""
from __future__ import annotations

import json
import platform
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def now() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def gpu_status() -> dict:
    if not shutil.which("nvidia-smi"):
        return {"available": False, "reason": "nvidia-smi not found on this runner"}
    try:
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], text=True, timeout=5)
        return {"available": True, "devices": [line.strip() for line in out.splitlines() if line.strip()]}
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}


def ollama_models() -> dict:
    if not shutil.which("ollama"):
        return {"available": False, "reason": "ollama CLI not found"}
    try:
        out = subprocess.check_output(["ollama", "list"], text=True, timeout=20)
        models = [line.split()[0] for line in out.splitlines()[1:] if line.strip()]
        return {
            "available": True,
            "nemotron_3_ultra_available": "nemotron-3-ultra:cloud" in models,
            "models": [m for m in models if "nemotron" in m.lower() or "glm" in m.lower()][:20],
        }
    except Exception as exc:
        return {"available": False, "reason": repr(exc)}


def cpu_micro_benchmark() -> dict:
    start = time.perf_counter()
    total = 0
    for i in range(160_000):
        total = (total + (i * i) % 97) % 1_000_000
    elapsed = max(time.perf_counter() - start, 1e-9)
    return {"elapsed_seconds": round(elapsed, 4), "checksum": total, "ops_per_second": round(160_000 / elapsed, 1)}


def read_json(name: str) -> dict:
    p = DATA / name
    return json.loads(p.read_text()) if p.exists() else {}


def main() -> None:
    DATA.mkdir(exist_ok=True)
    nemotron = read_json("nemotron_risk_review.json")
    safety = read_json("nemoclaw_safety_rack.json")
    report = {
        "generated_at": now(),
        "host": platform.platform(),
        "nvidia_gpu": gpu_status(),
        "ollama": ollama_models(),
        "nemotron_3_ultra": {
            "model": nemotron.get("model", "ollama-launch:nemotron-3-ultra:cloud"),
            "role": "Risk Reviewer in Hermes MoA",
            "status": nemotron.get("status", "missing"),
            "verdict": nemotron.get("verdict"),
            "latency_seconds": nemotron.get("latency_seconds"),
        },
        "nemoclaw": {
            "runtime_installed": safety.get("runtime_installed", False),
            "status": safety.get("runtime_status", "scaffold_only_not_production_nemoclaw"),
            "policy_checks": safety.get("policy_checks", []),
            "disclosure": safety.get("disclosure", "NemoClaw runtime not installed in this public demo."),
        },
        "nvidia_skills": read_json("nvidia_skills_access.json"),
        "cpu_fallback_benchmark": cpu_micro_benchmark(),
        "deployment_story": (
            "Risk review routes through Nemotron 3 Ultra via Ollama Cloud. "
            "The demo records local NVIDIA GPU detection and CPU fallback. "
            "NemoClaw is represented as an honest compatibility scaffold, not a claimed production runtime."
        ),
    }
    (DATA / "nvidia_integrations.json").write_text(json.dumps(report, indent=2))
    print(json.dumps({"ok": True, "nemotron_status": report["nemotron_3_ultra"]["status"], "gpu_available": report["nvidia_gpu"].get("available"), "output": str(DATA / "nvidia_integrations.json")}, indent=2))


if __name__ == "__main__":
    main()
