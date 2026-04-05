# OpenClaw Self-Improve

Evidence-based and approval-gated self-improvement workflow for OpenClaw.

## When to Use

- User asks to make OpenClaw more powerful or optimize behavior
- Measurable before/after outcomes are required
- Structure, approval, and rollback are needed

## When NOT to Use

- Casual "fix this thing" requests
- Cosmetic changes
- Hot patches

## How It Works

1. **Baseline** — Capture current state and metrics
2. **Hypotheses** — 1-3 testable improvement ideas
3. **Proposal** — Review plan + get explicit approval
4. **Implement** — Apply only approved changes
5. **Validate** — Compare before/after with evidence
6. **Outcome** — Document results, residual risk

## Scripts

- `init-improvement-run.sh` — Create run directory + templates
- `validate-improvement-run.sh` — Check required artifacts
- `export-improvement-run-json.py` — Generate machine-readable output

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
