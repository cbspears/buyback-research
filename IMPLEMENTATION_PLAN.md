---
type: plan
area: bitcoin-research
status: active
created: 2026-02-19
---

# Implementation Plan — Ralph Buyback Research

## Status

- **Current iteration**: 0
- **Reports completed**: 0
- **Last updated**: 2026-02-19 (initial setup)

## Research Queue

Priority order for analysis. Project Lead works top-to-bottom.

### High Priority (Primary Targets)

| # | Protocol | Token | Status | Date | Notes |
|---|----------|-------|--------|------|-------|
| 1 | Hyperliquid | HYPE | Queued | | Benchmark protocol, 97% fee buyback |
| 2 | Jupiter | JUP | Queued | | 50% fees, 3yr lock mechanism |
| 3 | Ethena | ENA | Queued | | $890M committed, fee switch |
| 4 | Jito | JTO | Queued | | Auction-based buyback |
| 5 | Ether.fi | ETHFI | Queued | | $50M approved, auto-trigger |
| 6 | Pump.fun | PUMP | Queued | | 100% revenue to buyback |
| 7 | Pyth Network | PYTH | Queued | | 33% DAO treasury |
| 8 | Aster | ASTER | Queued | | Up to 80% fees |
| 9 | Chainlink | LINK | Queued | | Reserve mechanism |
| 10 | dYdX | DYDX | Queued | | 25-75% net fees |
| 11 | Maple Finance | SYRUP | Queued | | Staking → buyback transition |
| 12 | Clanker | CLANKER | Queued | | Auto buyback-burn |
| 13 | Raydium | RAY | Queued | | 12% fee buyback & burn |

### Discovery Candidates (Need Verification)

| Protocol | Token | Signal | Status |
|----------|-------|--------|--------|
| Berachain | BERA | Novel PoL mechanism | Watch |
| EigenLayer | EIGEN | AVS fee distribution | Watch |
| Arbitrum | ARB | Sequencer revenue discussions | Watch |
| Banana Gun | BANANA | Revenue share/buyback | Watch |
| Rollbit | RLB | Revenue-based buyback-burn | Watch |
| Metaplex | MPLX | Protocol fee burn | Watch |
| WOO | WOO | Buyback and burn program | Watch |
| Uniswap | UNI | Fee switch debate | Watch |

## Completed Reports

| Protocol | Date | Report Path | Analyst Consensus |
|----------|------|-------------|-------------------|
| (none yet) | | | |

## Methodology Notes

- Discovery scan runs every 3rd iteration
- Each iteration targets one protocol
- 5 analyst personas run in parallel per protocol
- Reports follow specs/report-template.md format
- Data collected: DefiLlama (revenue/fees), CoinGecko (market data), Snapshot (governance)

## Known Issues / Gaps

- Some protocols may not have DefiLlama slugs configured — check src/collectors/defillama.py
- CoinGecko free tier has rate limits — be patient
- Snapshot spaces not configured for all protocols — some use custom governance
- On-chain collector is minimal — expand per-protocol as needed

## Research Questions (Accumulated)

- How do buyback yields compare to traditional equity buyback yields?
- Is there a relationship between buyback announcement and token price action?
- Do protocols with higher FDV/MCap ratios have less effective buybacks (dilution overwhelms)?
- What is the optimal buyback frequency — continuous vs. periodic?
- How do bear market conditions affect buyback program sustainability?
