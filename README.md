# Otto Procurement Agent

Otto Procurement Agent is an autonomous SaaS-spend micro-business built for the Nous Research x NVIDIA x Stripe Hermes Agent Accelerated Business Hackathon.

It ingests a SaaS stack, uses Hermes MoA to identify wasted spend, packages the result as a paid savings audit, creates a Stripe-style success-fee checkout event, records revenue and agent operating costs, and prepares buyer delivery/provisioning actions.

## Winning hook

"This agent audited a startup's SaaS stack, found tens of thousands in waste, and billed only when it saved money."

## MoA roles

- Reference 1: `openai-codex:gpt-5.5`
- Reference 2: `ollama-launch:glm-5.2:cloud`
- Aggregator: `openai-codex:gpt-5.5`

## Run locally

```bash
python3 scripts/run_full_cycle.py
cd site && python3 -m http.server 8791 --bind 127.0.0.1
```

## Safety

No proprietary company data. The dataset is synthetic but realistic. No live spend without explicit human approval. If a Stripe test key is present, the code can create a Stripe test Checkout session; otherwise it generates a signed local Stripe-style test event and labels it honestly.
