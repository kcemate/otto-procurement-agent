# Rules Grounding — Nous x NVIDIA x Stripe Hermes Agent Hackathon

Generated: 2026-06-28

## Source-backed facts

Primary source surfaced by X Search: `@NousResearch` post `2066921443548348436`.

Known contest frame:

- Event: Nous Research x NVIDIA x Stripe Hermes Agent Accelerated Business Hackathon.
- Theme: build agents that can **earn, spend, and run real business operations at scale**.
- Entry mechanics:
  - Post a **1–3 minute demo video** on X.
  - Tag `@NousResearch`.
  - Include a short write-up.
  - Drop the X link in the Discord submissions channel.
  - Fill out the submission form.
- Deadline: EOD Tuesday, June 30, 2026.
- Judging criteria from source summary: **usefulness, viability, presentation**.
- Prize stack includes NVIDIA DGX Spark and Stripe credits.

## Sponsor integration implications

### Hermes / Nous

A competitive submission must show actual agent behavior, not just a static app:

- Multi-step workflow.
- Tool use / operations.
- Memory or replayability if relevant.
- MoA/adversarial reasoning where it improves judgment.
- Visible run log or evidence chain.

### Stripe

A competitive submission must make the earn/spend loop central:

- Agent earns money or records a realistic test-mode revenue event.
- Agent spends or allocates operating costs under safety limits.
- Test-mode or synthetic economics must be labeled clearly.
- Live spend must not be claimed without real execution and user approval.

### NVIDIA

The official positioning emphasizes:

- **NemoClaw**: safe/runtime layer for agents.
- **Nemotron 3 Ultra**: fast agentic inference.
- **NVIDIA agent skills**: extensive skills catalog.

Implication: merely saying “NVIDIA/local AI lab” is weak. The repo/demo should show proof artifacts for at least one real NVIDIA path and should be explicit where the runtime is scaffolded rather than installed.

## Current hard constraints

- No proprietary CFA data.
- Synthetic/public demo data only.
- Stripe test/local economics only unless explicitly approved.
- No false claim that NemoClaw/OpenShell runtime is installed.
- No claim of local NVIDIA GPU inference on this Mac: `nvidia-smi` is not present on the runner.
- Nemotron 3 Ultra may be claimed because the model path has been smoke-tested and called via Ollama Cloud.
- NVIDIA skills catalog may be claimed because `npx skills add nvidia/skills --list --full-depth` found 225 skills.

## Winning bar

The product must answer three judge questions in under 10 seconds:

1. **What business does this agent run?**
2. **Where is the money loop?**
3. **Why did NVIDIA/Stripe/Hermes matter, instead of being name-dropped?**

Any product that cannot answer all three visually and verifiably is below the bar.
