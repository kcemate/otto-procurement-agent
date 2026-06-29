# Claim Ledger — Otto Procurement Agent

Generated: 2026-06-28

## Verified by tool output / repo artifacts

| Claim | Status | Evidence |
|---|---:|---|
| Demo URL resolves | Verified | HTTP 200 for `https://kcemate.github.io/otto-procurement-agent/` |
| Repo resolves | Verified | HTTP 200 for `https://github.com/kcemate/otto-procurement-agent` |
| X post resolves | Verified | HTTP 200 for `https://x.com/ai_aristocrat/status/2071323818313089500?s=46` |
| Current repo commit includes NVIDIA proof | Verified locally | `git rev-parse --short HEAD` returned `4942f5e` before latest local changes |
| MoA preset includes Nemotron 3 Ultra | Verified | `hermes moa list` showed `nvidia-hackathon` with `ollama-launch:nemotron-3-ultra:cloud`, `openai-codex:gpt-5.5`, `ollama-launch:glm-5.2:cloud`, GPT-5.5 aggregator |
| Direct Nemotron works | Verified | `hermes chat --provider ollama-launch -m nemotron-3-ultra:cloud ...` returned `nemotron-ready` |
| Nemotron MoA works | Verified | `hermes chat --provider moa -m nvidia-hackathon ...` returned `moa-nemotron-ready` |
| Nemotron risk review call succeeded | Verified | `data/nemotron_risk_review.json`: model `ollama-launch:nemotron-3-ultra:cloud`, status `ok`, verdict `escalate`, latency `5.181s` from previous run |
| NVIDIA skills catalog discovered | Verified | `data/nvidia_skills_access.json`: status `ok`, `found_count: 225` |
| Local NVIDIA GPU not present | Verified | `data/nvidia_integrations.json`: `nvidia_gpu.available: false`, reason `nvidia-smi not found on this runner` |
| NemoClaw runtime not installed/running | Verified limitation | `data/nemoclaw_safety_rack.json`: `runtime_installed: false`, status `scaffold_only_not_production_nemoclaw` |
| Procurement demo stack annual spend | Synthetic/test-mode artifact | `data/audit.json`: `$235,416` before annual spend |
| Approved savings | Synthetic/test-mode artifact | `data/audit.json`: `$62,880` annual savings |
| Success fee | Synthetic/test-mode artifact | `data/audit.json`: `$12,576` / 20% |
| Agent run cost | Modeled demo artifact | `data/evidence_pack.json`: `$34.20` operating cost |
| Blocked Slack reduction | Synthetic safety scenario | `data/evidence_pack.json`: legal hold + executive workspace dependencies |
| Stripe revenue event | Test/local only | `data/ledger.json`: `local_stripe_style_test_event`; no live Stripe payment claimed |

## Claims allowed in public copy

- “Nemotron 3 Ultra via Ollama Cloud powers the Risk Reviewer MoA role.”
- “NVIDIA skills catalog discovery found 225 skills.”
- “NemoClaw-compatible safety instrumentation scaffolds policy checks.”
- “NemoClaw runtime is not claimed as production-installed.”
- “The demo uses synthetic/test-mode data and approval-gated dry-run manifests.”
- “Stripe-style success-fee event is local/test-mode unless a Stripe test key is configured.”

## Claims not allowed

- “NemoClaw is running.”
- “NemoClaw secured this agent in production.”
- “Local NVIDIA GPU inference ran on this Mac.”
- “The agent collected real revenue.”
- “The agent processed real customer spend.”
- “The agent autonomously cancelled vendor subscriptions.”
- Any unqualified dollar claim that omits synthetic/test-mode framing.

## Current weakness flags

1. **NemoClaw is scaffolded, not installed.** This is honest but less compelling than a real NemoClaw runtime.
2. **Stripe is local/test-mode.** The business loop is plausible but not real money.
3. **Dataset is synthetic.** The demo is replayable and safe, but less market-proven.
4. **The public X post omitted the strongest NVIDIA proof.** This can be corrected with a reply and Discord/form copy, not necessarily by reposting.
5. **Current story risks reading as “SaaS audit dashboard.”** It must be reframed as a policy-gated autonomous procurement business.

## Immediate product-copy implication

The safest high-EV framing is not “we built a SaaS savings tool.” It is:

> A Hermes agent business that earns a success fee by finding SaaS waste, while Nemotron 3 Ultra risk-reviews unsafe actions and a NemoClaw-compatible safety rack keeps procurement changes approval-gated.
