# org/governance (Starter)

Reusable governance for multiple repos:
- Policies (constitution, Rego, schemas, lint)
- Reusable **immune** workflow for PR gates

## How to use (in a project repo)
```yaml
jobs:
  immune:
    uses: <org>/governance/.github/workflows/immune.yml@v1
    with:
      style_pack: book
```
Then protect the `main` branch to require the status **immune / gate**.


## Inputs
- `style_pack` (default: `book`)
- `strict` (default: `false`) — if `true`, any violation **fails** the check; if `false`, violations are warnings.
- `allow_override_label` (default: `gov-override`) — if the PR has this label, the gate runs but **never blocks**.

## Performance
The gate only runs when files under `docs/`, `generated/`, or `ledger/` change.
