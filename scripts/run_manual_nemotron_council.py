#!/usr/bin/env python3
"""Manual MoA fallback for product strategy when provider=moa times out.

Runs three independent council lanes (Nemotron 3 Ultra, GPT-5.5, GLM 5.2)
and then has GPT-5.5 aggregate. This preserves the MoA pattern while keeping
artifacts explicit and auditable.
"""
from __future__ import annotations

import concurrent.futures as cf
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRATEGY = ROOT / "strategy"

RULES = """Contest: Nous x NVIDIA x Stripe Hermes Agent hackathon. Criteria: usefulness, viability, presentation. Theme: agents earn, spend, run business operations. NVIDIA emphasis: NemoClaw safety, Nemotron 3 Ultra speed, NVIDIA skills. Stripe emphasis: earn/spend with safety limits.

Incumbent: Otto Procurement Agent. Synthetic replayable SaaS procurement business. Verified artifacts: $235,416 synthetic annual SaaS spend; $62,880 synthetic annual savings; $12,576 local/test success fee; $34.20 modeled run cost; real Nemotron 3 Ultra via Ollama Cloud risk review; NVIDIA skills catalog count 225; NemoClaw-compatible scaffold only, not installed runtime; no local NVIDIA GPU on Mac.

Rules: no invented numbers, no real customer/revenue claims, no claiming NemoClaw runtime is running, penalize concepts requiring hardware/data/credentials we do not have. Optimize to win, not preserve incumbent.
"""

LANES = [
    (
        "nemotron-risk-strategist",
        "ollama-launch",
        "nemotron-3-ultra:cloud",
        "You are Nemotron 3 Ultra. Focus on NVIDIA centrality, agent safety, proof burden, and judge skepticism. Generate and score 10 product concepts. Include whether each beats the incumbent. Be concise but brutal.",
    ),
    (
        "gpt-business-judge",
        "openai-codex",
        "gpt-5.5",
        "You are the business/judging strategist. Focus on usefulness, viability, presentation, and what can win the hackathon. Generate and score 10 product concepts. Include whether each beats the incumbent. Be concise but brutal.",
    ),
    (
        "glm-builder-feasibility",
        "ollama-launch",
        "glm-5.2:cloud",
        "You are the builder/feasibility judge. Focus on what can be built and verified before deadline without fake claims. Generate and score 10 product concepts. Include whether each beats the incumbent. Be concise but brutal.",
    ),
]


def call_lane(lane: tuple[str, str, str, str]) -> tuple[str, str]:
    name, provider, model, role = lane
    prompt = f"""{RULES}

{role}

Required format:
- Ranked list of 10 concepts
- For each: name, one-line hook, sponsor fit /10, usefulness /10, viability /10, presentation /10, proof fit /10, novelty /10, time fit /10, fabrication risk /10, EV score = positives - fabrication risk
- Top 3 recommendation
- Direct verdict: keep, reframe, or pivot from incumbent
"""
    cmd = ["hermes", "chat", "--provider", provider, "-m", model, "-Q", "--max-turns", "1", "--ignore-rules", "-q", prompt]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=420)
    out = proc.stdout + ("\n\nSTDERR:\n" + proc.stderr if proc.stderr else "")
    artifact = f"<!-- lane={name} provider={provider} model={model} exit={proc.returncode} generated={datetime.utcnow().isoformat()}Z -->\n\n{out}"
    (STRATEGY / f"manual-moa-{name}.md").write_text(artifact)
    return name, artifact


def aggregate(outputs: dict[str, str]) -> str:
    joined = "\n\n".join(f"## {name}\n{txt[-18000:]}" for name, txt in outputs.items())
    prompt = f"""You are the aggregator for a manual MoA council. Make the final hackathon product decision.

{RULES}

Council outputs:
{joined}

Produce:
1. Final decision: KEEP, REFRAME, or PIVOT.
2. Chosen product and one-line hook.
3. Scorecard comparing top 5 candidates.
4. Why rejected alternatives lose.
5. Exact product/story changes required.
6. Exact repo/demo/submission files to modify.
7. Discord copy under 1800 chars.
8. X reply under 600 chars.
9. Form patch language.
10. Verification checklist.

Be aggressive but honest. Do not invent numbers. If incumbent survives, prefer REFRAME unless no changes are required.
"""
    cmd = ["hermes", "chat", "--provider", "openai-codex", "-m", "gpt-5.5", "-Q", "--max-turns", "1", "--ignore-rules", "-q", prompt]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=420)
    out = proc.stdout + ("\n\nSTDERR:\n" + proc.stderr if proc.stderr else "")
    artifact = f"<!-- aggregator=gpt-5.5 exit={proc.returncode} generated={datetime.utcnow().isoformat()}Z -->\n\n{out}"
    (STRATEGY / "final-product-decision.md").write_text(artifact)
    return artifact


def main() -> None:
    STRATEGY.mkdir(exist_ok=True)
    outputs = {}
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(call_lane, lane) for lane in LANES]
        for fut in cf.as_completed(futures):
            name, artifact = fut.result()
            outputs[name] = artifact
            print(f"lane_done {name} chars={len(artifact)}")
    combined = "\n\n---\n\n".join(outputs[name] for name in sorted(outputs))
    (STRATEGY / "nemotron-product-divergence.md").write_text(combined)
    decision = aggregate(outputs)
    print("decision_chars", len(decision))
    print(decision[-5000:])


if __name__ == "__main__":
    main()
