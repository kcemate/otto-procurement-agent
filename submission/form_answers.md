# Submission form draft

## Project name
Otto Procurement Profit Agent

## One-line summary
A Nemotron-governed Hermes agent that runs a replayable procurement business with Stripe test/local success fees and NemoClaw-compatible safety gates.

## What it does
Otto audits a synthetic 20-vendor SaaS stack with invoices, usage signals, owners, renewal context, and duplicate app categories. It runs an adversarial Hermes MoA council to identify waste, recompute the math, review provisioning risk, and block unsafe recommendations. The demo finds $62,880/year in synthetic approved savings on $235,416/year of synthetic spend, blocks a tempting Slack reduction because of legal hold and executive dependencies, records a capped $12,576 local/test success-fee event, debits $34.20 of modeled operating cost, and signs approval-gated dry-run action manifests.

## Why Hermes Agent / MoA
The product depends on multi-agent disagreement, not a single model summary. The savings hunter proposes cuts; finance recomputes the fee basis; IT reviews provisioning safety; Nemotron 3 Ultra performs risk review; the aggregator promotes only actions that survive. The site exposes the replay log, council reasoning, evidence cards, blocked recommendation, P&L, safety-gate checks, and dry-run manifests.

## NVIDIA integration
The demo uses Nemotron 3 Ultra via Ollama Cloud for the Risk Reviewer role. It also includes NVIDIA skills catalog discovery with a verified count of 225. The safety layer is framed honestly as NemoClaw-compatible scaffolding/policy logic; it does not claim the NVIDIA NemoClaw runtime is installed or running. `scripts/gpu_probe.py` detects local NVIDIA hardware and records fallback status; this Mac does not have local NVIDIA GPU inference.

## Stripe integration
The public demo uses a signed Stripe-style local/test success-fee event and treasury ledger with hard limits and audit logging. `scripts/create_stripe_checkout.py` can create a real Stripe test Checkout Session when a Stripe test key is available. Live keys are refused by default. The demo does not claim real customer revenue or production payments.

## Demo URL
https://kcemate.github.io/otto-procurement-agent/

## Repository
https://github.com/kcemate/otto-procurement-agent

## X demo link
https://x.com/ai_aristocrat/status/2071323818313089500?s=46

## Honest scope
Synthetic replay only. No real customer data. No real revenue claim. No production Stripe payment claim. No claim that NemoClaw runtime is running. No local NVIDIA GPU required.
