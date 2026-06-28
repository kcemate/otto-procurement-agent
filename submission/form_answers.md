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
Procurement evidence contains sensitive contracts, pricing, and vendor terms. The production deployment path is private/local inference on NVIDIA-class hardware. The dashboard includes an instrumentation lane that detects NVIDIA availability and records a CPU fallback benchmark when no NVIDIA GPU is attached to the runner.

## Demo URL
https://kcemate.github.io/otto-procurement-agent/

## Repository
https://github.com/kcemate/otto-procurement-agent

## X demo link
[paste final X post URL]

## Data / safety disclosure
The demo uses public/synthetic data and test-mode economics. Live customer-facing changes stay behind human approval. Dry-run manifests include rollback paths and signatures but do not execute destructive actions.
