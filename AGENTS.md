# Project Conventions

## Python
- Python 3.11+, use venv at ./venv
- Run: python -m pytest src/ (validation)
- All collectors return JSON to data/

## Reports
- Obsidian frontmatter required (type, area, topics, status)
- One protocol per report, one report per loop iteration
- Reports go to output/, not scattered through the vault

## Git
- Commit after each completed report
- Message format: "research({protocol}): add buyback analysis report"
- Keep commits atomic — one protocol per commit

## Subagents
- Use parallel subagents for the 5 analyst personas
- Use 1 subagent for data collection (backpressure)
- Use 1 subagent for discovery (backpressure)

## Data Sources
- DefiLlama (free API): revenue, fees, TVL, holders revenue
- CoinGecko (free API): price, mcap, supply
- Snapshot.org (free GraphQL): governance proposals
- Direct RPC (free): protocol-specific queries
