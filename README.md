# Otto Procurement Agent

A replayable SaaS procurement micro-business built for the Nous Research x NVIDIA x Stripe Hermes Agent Accelerated Business Hackathon.

**Live demo:** https://kcemate.github.io/otto-procurement-agent/

## What it proves

Otto audits a synthetic-but-realistic 20-vendor SaaS stack, finds approved waste, blocks unsafe cuts, records an outcome-based success fee, debits its own operating costs, reinvests into the next scan, and signs dry-run action manifests for buyer approval.

## Verified demo economics

- Full SaaS stack: **$235,416/year**
- Approved savings: **$62,880/year**
- Success fee: **$12,576** / 20% of approved savings
- Agent run cost: **$34.20**
- Contribution margin: **$12,541.80**
- Reinvestment: **$500** into next scan
- Ending treasury: **$12,041.80**

## 10x proof points

- **Replay mode:** deterministic run log from raw evidence to fee event.
- **Evidence cards:** every approved dollar ties to invoice, usage, owner, migration, or policy evidence.
- **Adversarial MoA council:** GPT-5.5, GLM 5.2 Cloud, and Nemotron 3 Ultra risk review.
- **Safety refusal:** a tempting Slack reduction is blocked due to legal hold and executive workspace dependencies.
- **NVIDIA integration proof:** Nemotron 3 Ultra runs through Ollama Cloud; NVIDIA skills catalog discovery is recorded; NemoClaw-compatible policy checks are scaffolded honestly without claiming the runtime is installed.
- **Dry-run manifests:** signed action packets with rollback paths; no destructive action executes without approval.
- **Treasury/P&L:** revenue, operating costs, reinvestment, and ending balance.
- **Public source checks:** benchmark vendor pricing endpoints are checked and rendered.
- **Private inference lane:** NVIDIA/local-lab deployment path is instrumented; CPU fallback benchmark is recorded when no NVIDIA GPU is attached.
- **One-command demo:** `make demo && make verify`.
- **Autonomy loop:** GitHub Actions hourly cycle refreshes public artifacts.

## Run locally

```bash
make demo
make verify
make serve
```

Open http://127.0.0.1:8791.

## Stripe

The public demo uses a signed Stripe-style test event. If a Stripe test key is configured, the checkout helper creates a real Checkout Session:

```bash
STRIPE_SECRET_KEY=sk_test_... python3 scripts/create_stripe_checkout.py
```

Live keys are refused by default.

## Safety / disclosure

The demo uses public/synthetic data and test-mode economics. Live customer-facing changes remain behind human approval. Dry-run manifests include signatures and rollback paths but do not execute destructive actions.
