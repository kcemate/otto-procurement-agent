# Submission form draft

## Project name
Otto Procurement Agent

## One-line summary
A replayable SaaS procurement micro-business that uses Hermes MoA to find verified software waste, block unsafe cuts, bill a success fee, record its own costs, and prepare approval-gated action manifests.

## What it does
Otto Procurement Agent ingests a 20-vendor SaaS stack with invoices, usage signals, owners, renewal context, and duplicate app categories. It runs an adversarial MoA council to identify waste, recompute the math, review provisioning risk, and block unsafe recommendations. The demo finds $62,880/year in approved savings, blocks a tempting Slack reduction because of legal hold and executive dependencies, records a $12,576 success-fee event, debits $34.20 of operating cost, reinvests $500 into the next scan, and signs dry-run action manifests for cancellations, migrations, seat true-ups, and checkout prep.

## Why Hermes Agent / MoA
The product depends on multi-agent disagreement, not a single model summary. The savings hunter proposes cuts; finance recomputes the fee basis; IT reviews provisioning safety; risk blocks unsafe changes; the aggregator promotes only actions that survive. The site exposes the replay log, council reasoning, evidence cards, blocked recommendation, P&L, and dry-run manifests so judges can see the agentic loop instead of trusting a static result.

## Stripe integration
For this public demo, the ledger uses a signed Stripe-style test event and includes a `scripts/create_stripe_checkout.py` path that creates a real Stripe test Checkout Session when a test key is available. Live keys are refused by default.

## NVIDIA / local AI lab angle
One MoA role (Risk Reviewer) routes to Nemotron 3 Ultra via Ollama Cloud. A `nvidia/safety_rack.py` instrumentation layer scaffolds NemoClaw-style policy checks (scope, rate limit, rollback verification, and human approval) before action manifests are signed. `scripts/gpu_probe.py` detects local NVIDIA hardware and records fallback timing; when no local GPU is present, the demo honestly records the cloud/CPU fallback. NVIDIA skills catalog access is recorded through `scripts/probe_nvidia_skills.py`.

## Demo URL
https://kcemate.github.io/otto-procurement-agent/

## Repository
https://github.com/kcemate/otto-procurement-agent

## X demo link
https://x.com/ai_aristocrat/status/2071323818313089500?s=46

## Data / safety disclosure
The demo uses public/synthetic data and test-mode economics. Live customer-facing changes stay behind human approval. Dry-run manifests include rollback paths and signatures but do not execute destructive actions.
