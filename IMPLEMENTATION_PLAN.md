---
type: plan
area: bitcoin-research
status: active
created: 2026-02-19
---

# Implementation Plan — Ralph Buyback Research

## Status

- **Current iteration**: 5
- **Reports completed**: 5
- **Last updated**: 2026-02-19
- **Last discovery scan**: Iteration 3 (2026-02-19)

## Research Queue

Priority order for analysis. Project Lead works top-to-bottom.

### High Priority (Primary Targets)

| # | Protocol | Token | Status | Date | Notes |
|---|----------|-------|--------|------|-------|
| 1 | Hyperliquid | HYPE | Done | 2026-02-19 | Benchmark protocol, 54% fee buyback-burn. Consensus: mechanism best-in-class, unlock overhang dominant risk. |
| 2 | Jupiter | JUP | Done | 2026-02-19 | 50% fee buyback HALTED. Litterbox Trust spent $70M at avg $0.74, token at $0.16. Unanimous Bearish from all 5 analysts. Pivoting to Net-Zero Emissions. |
| 3 | Ethena | ENA | Done | 2026-02-19 | $890M SPAC buyback (held, not burned). Token -92% from ATH, -83% during buyback. Fee switch is superior mechanism. 4 Bearish, 1 Neutral. |
| 4 | Jito | JTO | Done | 2026-02-19 | 100% DAO rev to buyback via CSD. $2.5M deployed at $1.91 avg (now $0.29). 0.49x buyback-to-unlock ratio. 3 Neutral, 2 Bearish. Infrastructure strong, token value accrual nascent. |
| 5 | Ether.fi | ETHFI | Done | 2026-02-19 | 3-layer buyback (withdrawal weekly, revenue monthly, $50M treasury conditional). $13.18M deployed at $0.46 (-94.6% ATH). Revenue $65-96M real. Unlock pressure 8.5x buyback capacity. 3 Neutral, 1 Neutral/Bearish, 1 Bearish. Cash Card is thesis-changing variable. |
| 6 | Pump.fun | PUMP | Queued | | 100% revenue to buyback |
| 7 | Pyth Network | PYTH | Queued | | 33% DAO treasury |
| 8 | Aster | ASTER | Queued | | Up to 80% fees |
| 9 | Chainlink | LINK | Queued | | Reserve mechanism |
| 10 | dYdX | DYDX | Queued | | 25-75% net fees |
| 11 | Maple Finance | SYRUP | Queued | | Staking → buyback transition |
| 12 | Clanker | CLANKER | Queued | | Auto buyback-burn |
| 13 | Raydium | RAY | Queued | | 12% fee buyback & burn |

### Discovered in Iteration 3 — Promote to Primary Targets

| # | Protocol | Token | Status | Date | Notes |
|---|----------|-------|--------|------|-------|
| 14 | Aave | AAVE | Queued | | $50M/yr permanent buyback, weekly adaptive purchases. Largest lending protocol. |
| 15 | Sky (MakerDAO) | SKY | Queued | | ~$97M buyback-and-burn in 2025, 5.4% supply burned. $338M annual revenue. |
| 16 | Gains Network | GNS | Queued | | 100% revenue to burn, 25.7% supply burned. "Road to 1 GNS." |
| 17 | GMX | GMX | Queued | | Buyback & Distribute model, 12.9% supply repurchased. Governance debate on 90% allocation. |

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
| LayerZero | ZRO | $160M buyback from investors + Stargate revenue | Watch |
| Linea | LINEA | Dual-burn mechanism (80/20 LINEA/ETH) | Watch |
| PancakeSwap | CAKE | 29-month deflationary streak, buy-and-burn | Watch |
| Lido | LDO | Conditional automated buyback (NEST program, 2026) | Watch |

## Completed Reports

| Protocol | Date | Report Path | Analyst Consensus |
|----------|------|-------------|-------------------|
| Hyperliquid | 2026-02-19 | output/hyperliquid-report.md | 2 Bullish, 2 Neutral, 1 Bearish |
| Jupiter | 2026-02-19 | output/jupiter-report.md | 0 Bullish, 0 Neutral, 5 Bearish (unanimous) |
| Ethena | 2026-02-19 | output/ethena-report.md | 0 Bullish, 1 Neutral, 4 Bearish |
| Jito | 2026-02-19 | output/jito-report.md | 0 Bullish, 3 Neutral, 2 Bearish |
| Ether.fi | 2026-02-19 | output/etherfi-report.md | 0 Bullish, 3 Neutral, 1 Neutral/Bearish, 1 Bearish |

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
- Python collectors require outbound internet — if running offline, data must be collected via web search subagents
- DefiLlama API DNS resolution failed during Jito iteration (fees.llama.fi) — web research subagents used as fallback. Consider adding cached responses or alternative API endpoints.

## Research Questions (Accumulated)

- How do buyback yields compare to traditional equity buyback yields?
- Is there a relationship between buyback announcement and token price action?
- Do protocols with higher FDV/MCap ratios have less effective buybacks (dilution overwhelms)?
- What is the optimal buyback frequency — continuous vs. periodic?
- How do bear market conditions affect buyback program sustainability?
- (From HYPE analysis) Does the unlock-to-buyback ratio provide a generalizable metric for buyback effectiveness?
- (From HYPE analysis) Should protocols retain treasury reserves before initiating buybacks? What is the optimal reserve-to-buyback allocation?
- (From HYPE analysis) How does "vertically integrated app with own L1" differ from "true fat protocol" for buyback sustainability?
- (From HYPE analysis) Can team wallet behavior be monitored systematically as a signal for buyback quality?
- (From JUP analysis) How should buyback programs handle concurrent insider unlock schedules? Is there a minimum buyback/unlock coverage ratio below which buybacks are counterproductive?
- (From JUP analysis) Lock vs burn: are there any scenarios where locking purchased tokens is preferable to burning? Or is this always a design error?
- (From JUP analysis) The Mercurial offset pattern — how common are near-perfect buyback/vesting offsets across protocols? Is this a systematic feature of buyback programs with concurrent vesting?
- (From JUP analysis) Application-layer vs infrastructure-layer buybacks: does Monegro's forkability thesis hold empirically? Need to compare Jupiter (app) vs Hyperliquid (L1) outcomes.
- (From JUP analysis) Pro-cyclical buyback failure: can countercyclical buyback designs (accumulate treasury in bull, deploy in bear) be implemented programmatically?
- (From JUP analysis) Does the pivot from buyback to emission control (Net-Zero) represent a generalizable pattern for protocols that discover buybacks are insufficient?
- (From ENA analysis) Can revenue models that cross zero (go negative) ever sustain buyback programs? Is there a minimum revenue floor requirement?
- (From ENA analysis) SPAC-as-buyback-vehicle: is StablecoinX a one-off experiment or a template? What are the regulatory implications of Nasdaq-listed entities accumulating DeFi governance tokens?
- (From ENA analysis) Hold vs burn: does holding purchased tokens in a treasury vehicle create worse outcomes than Jupiter's Litterbox Trust lock model? Both failed — is "not burning" always a design error?
- (From ENA analysis) Fee switch vs buyback: when both mechanisms are available, does running them in parallel create capital allocation incoherence? Is there evidence that fee switches alone outperform fee switch + buyback combinations?
- (From ENA analysis) Buyback & Distribute (GMX model) vs Buyback & Burn vs Buyback & Hold: systematic comparison needed across all three token flow models.
- (From ENA analysis) Conditional/adaptive buybacks (Lido NEST, Aave adaptive weekly) vs flat-rate buybacks: do triggers and conditions improve outcomes?
- (From Discovery) Supply compression leaders — Gains Network (25.7%) and GMX (12.9%) are dramatically ahead. Is there an inflection point where supply compression becomes reflexively positive?
- (From Discovery) MakerDAO/Sky buyback scaling ($370K → $97M in one year, 262x increase) — what drove this and is it replicable?
- (From JTO analysis) Infrastructure-layer moat vs token value accrual: can a protocol have a dominant infrastructure position (95%+ penetration) while the governance token still fails to capture value? What additional mechanisms (veToken, fee distribution, burns) are necessary?
- (From JTO analysis) The CSD "treasury as insider bid" dynamic: when buybacks run against live vesting schedules, does the DAO systematically subsidize insider exit? Is there a minimum vesting-completion threshold before buybacks become value-accretive?
- (From JTO analysis) Forkability at the infrastructure layer: Paladin forked Jito-Solana and eroded MEV share from 75% to 60% in 6 months. Does the JitoSOL flywheel (DeFi composability, TVL gravity) create a sufficient second moat, or will MEV infrastructure commoditize?
- (From JTO analysis) Revenue denomination matters: Jito earns in SOL (hard asset) but converts to JTO (governance token) via buyback. Is this trade-down from hard asset to soft asset always value-destructive, or can it compound if the governance token appreciates?
- (From JTO analysis) The "buyback and barter" model (inter-DAO token swaps): does distributing purchased tokens to partner DAOs create more durable demand than burning? Soft lock-up through relationships vs hard lock-up through code.
- (From ETHFI analysis) Buyback-to-unlock ratio as a universal metric: Ether.fi's buyback absorbs 12-30% of unlock pressure (8.5x sell pressure vs buy pressure). Is there a minimum ratio below which buybacks are net-negative (providing exit liquidity for insiders while consuming treasury)?
- (From ETHFI analysis) Nominal-price triggers vs valuation-based triggers: the $3 trigger is permanently active at $0.46. Should buyback triggers be P/E-based or revenue-multiple-based rather than nominal-price-based? Would this produce better capital allocation outcomes?
- (From ETHFI analysis) Counter-cyclical withdrawal fee buybacks: Ether.fi's withdrawal fees fund buybacks during panic exits — a rare counter-cyclical element. How material is this in practice? Does it represent a generalizable design pattern for staking protocols?
- (From ETHFI analysis) The "neobank escape hatch" — when DeFi middleware protocols pivot to consumer fintech (Cash cards, hotel bookings), does this create sufficient non-crypto-correlated revenue to sustain buybacks through crypto winters? Or does crypto card spending collapse in bear markets too?
- (From ETHFI analysis) Distribute-to-stakers vs burn for application-layer tokens: all 5 analysts agreed distribute is correct for non-monetary tokens. Is there empirical evidence that distribution creates more sustainable demand than burns at the application layer?
- (From ETHFI analysis) Capital allocation at the inflection point: Hasu argues buyback capital should be redirected to Cash Card growth. When should protocols shift from "return capital" to "reinvest for growth"? Is there a revenue-to-FDV ratio that determines the optimal switch?
- (From ETHFI analysis) Ecosystem embeddedness as a moat against forkability: weETH's 400+ DeFi integrations create switching friction at the ecosystem level (not user level). How durable is this moat compared to L1 network effects? Historical precedents?
