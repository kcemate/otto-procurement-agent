# Submission form draft

## Project name
Otto Procurement Agent

## One-line summary
An autonomous SaaS procurement micro-business that uses Hermes MoA to find wasted software spend, bill a success fee through Stripe, record operating costs, and prepare provisioning actions.

## What it does
Otto Procurement Agent ingests a company's SaaS stack, normalizes spend and utilization, identifies duplicate systems and low-use licenses, synthesizes a paid savings audit through Hermes MoA, creates a success-fee checkout for 20% of first-year savings, records revenue/spend/reinvestment in a treasury ledger, and prepares buyer delivery plus provisioning actions.

## Why it is useful
SaaS bloat is universal and measurable. Buyers do not need another dashboard; they need a concrete savings plan with actions, risk, effort, and a business model aligned to outcomes.

## Why it is viable
The demo uses durable primitives: Hermes Agent, MoA, synthetic-but-realistic spend ingestion, Stripe test/local checkout events, treasury accounting, static publishing, and prepared provisioning delivery. The architecture can swap in real SaaS APIs and Stripe test/live keys with the same operating loop.

## How it uses MoA
The corrected council uses GPT-5.5 as Reference 1, GLM 5.2 Cloud as Reference 2, and GPT-5.5 as Aggregator. The references challenge spend assumptions and implementation risk; the aggregator produces the final buyer-facing audit and action queue.

## Safety controls
No proprietary data. No live spend without human approval. Per-cycle spend caps. If a live Stripe key is detected, object creation is blocked. If no test key is present, the demo uses a signed local Stripe-style test event and labels it honestly.

## Repository / demo URL
[paste durable site URL]

## X post URL
[paste final X post URL]
