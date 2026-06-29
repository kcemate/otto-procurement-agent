# Otto Procurement Profit Agent

A Nemotron-governed Hermes agent business built for the Nous Research x NVIDIA x Stripe Hermes Agent Accelerated Business Hackathon.

**Live demo:** https://kcemate.github.io/otto-procurement-agent/

## One-line hook

Otto runs a replayable procurement business: it audits a synthetic SaaS stack, finds waste, sends risky cuts through Nemotron 3 Ultra, applies NemoClaw-compatible approve/block gates, and books a capped Stripe test/local success fee.

## What it proves

This is not positioned as a generic SaaS audit dashboard. The demo is an agent-run business loop:

1. Ingest synthetic SaaS spend and usage evidence.
2. Propose savings actions through an adversarial Hermes MoA council.
3. Route risky actions to Nemotron 3 Ultra via Ollama Cloud.
4. Apply NemoClaw-compatible policy checks before action manifests.
5. Record a Stripe-style test/local success-fee event.
6. Debit modeled operating costs and show agent P&L.
7. Produce approval-gated dry-run manifests and an audit trail.

## Verified proof spine

| Proof item | Value | Scope |
|---|---:|---|
| Synthetic annual SaaS spend | **$235,416** | demo dataset |
| Synthetic annual savings found | **$62,880** | deterministic replay |
| Stripe-style success fee | **$12,576** | local/test event, 20% |
| Modeled agent run cost | **$34.20** | demo P&L |
| Customer net first-year value | **$50,304** | synthetic savings minus fee |
| Nemotron 3 Ultra | **called via Ollama Cloud** | Risk Reviewer role |
| NVIDIA skills catalog | **225 skills discovered** | catalog proof |
| NemoClaw | **compatible scaffold only** | runtime not claimed installed |
| Local NVIDIA GPU on this Mac | **not present** | `nvidia-smi` not found |

## Sponsor fit

### Hermes / MoA

The product depends on disagreement. Savings, finance, IT, risk, and aggregation roles challenge each other before a recommendation is promoted.

### NVIDIA

- Nemotron 3 Ultra via Ollama Cloud is wired to the Risk Reviewer lane.
- NVIDIA skills catalog discovery is recorded in `data/nvidia_skills_access.json`.
- NemoClaw-style scope, rollback, rate-limit, signature, and human-approval checks are scaffolded in `nvidia/safety_rack.py`.
- The demo does **not** claim the production NVIDIA NemoClaw runtime is installed or running.

### Stripe

- The public demo records a signed Stripe-style local/test success-fee event.
- `scripts/create_stripe_checkout.py` can create a real Stripe test Checkout Session when a Stripe test key is configured.
- Live Stripe keys are refused by default.

## Run locally

```bash
make demo
make verify
make serve
```

Open http://127.0.0.1:8791.

## NVIDIA verification

```bash
make nvidia-verify
```

This runs:

- `nvidia/nemotron_client.py`
- `nvidia/safety_rack.py`
- `scripts/probe_nvidia_skills.py`
- `scripts/gpu_probe.py`

## Honest scope

The demo uses synthetic data and test/local economics. It does not claim real customer data, real revenue, live vendor cancellations, production Stripe payments, local NVIDIA GPU inference, or a running NemoClaw production runtime. Live customer-facing changes remain behind human approval.
