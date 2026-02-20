---
type: source
area: bitcoin-research
topics: [buybacks, dydx]
protocol: dYdX
token: DYDX
category: Perps DEX (Cosmos appchain)
status: review
created: 2026-02-20
buyback_yield: 11.1
pe_ratio: 4.3
---

# dYdX -- Buyback Analysis

> **One-line summary**: An 11.1% buyback yield on an $81M market cap is not a signal of value accrual -- it is a signal that the market does not believe the revenue funding it is durable, and the choice to stake rather than burn purchased tokens preserves insider optionality at the expense of permanent supply reduction in a protocol that has lost 95%+ of its category's volume to Hyperliquid.

## Key Metrics

| Metric | Value |
|--------|-------|
| Market Cap | ~$81M |
| FDV | ~$98M |
| FDV/MCap | 1.21x |
| Annual Revenue (est) | ~$17.5-20M |
| Buyback Allocation | 75% (experimentally 100%) |
| Annual Buyback (est) | ~$9M |
| Buyback Yield | ~11.1% (on MCap) |
| P/E Ratio | ~4.3x (MCap/Rev) |
| FDV P/E | ~5.2x |
| Circulating Supply | 824M / 1B total (82.4%) |
| Total Supply | 1B |
| Category | Perps DEX (Cosmos appchain) |

## Protocol Background

dYdX was the dominant decentralized perpetual futures exchange from 2021 through early 2024. The protocol migrated from Ethereum L2 (StarkEx) to its own Cosmos appchain (dYdX Chain) in late 2023, a technically ambitious move that gave the protocol sovereignty over its execution layer, fee structure, and validator set. The migration was successful architecturally but coincided with a catastrophic loss of market share as Hyperliquid launched and captured 70-80% of the perps DEX market by mid-2024.

Founder Antonio Juliano departed in 2023, returned in October 2024 alongside 35% staff layoffs, and has since launched dYdX Unlimited (Nov 2024), which includes MegaVault (automated market-making), Instant Market Listings (permissionless markets), and plans for US spot trading, RWA perpetuals, and stake-for-reduced-fees. The MegaVault peaked at ~$80M TVL before declining 72% to ~$22M. The protocol currently lists 235 markets and processes ~$200M/day in volume -- roughly 2.5% of Hyperliquid's daily throughput.

## Revenue Model

dYdX generates revenue from trading fees on its Cosmos-based appchain. All protocol fees are collected in USDC and distributed to validators and stakers. Revenue sources include:

- **Perpetual futures trading fees** (dominant revenue source)
- **MegaVault fees** (5% allocation post-buyback program)
- **Nascent spot trading fees** (US market, launched 2025)

Revenue figures:
- **Annualized revenue**: ~$17.5-20M (declining)
- **Revenue trend**: Fees fell 84% YoY in Q2 2025
- **Daily fee generation**: ~$48-55K/day
- **Historical peak**: dYdX was generating $100M+ annualized in 2022-2023

The revenue decline is structural, not cyclical. While the broader perps market has grown substantially, dYdX's share has collapsed. Hyperliquid generates $8B+ daily volume versus dYdX's ~$200M. Zero-fee competitors (Lighter, Aster) further erode the revenue base. The protocol has responded with zero-fee BTC/SOL markets, which improve competitiveness at the direct expense of fee revenue.

## Buyback Mechanism

### Timeline

| Date | Event | Allocation |
|------|-------|-----------|
| March 2025 | Buyback program launched | 25% of net protocol fees |
| Nov 2025 | Proposal #313 passed (59.38% approval) | Increased to 75% |
| Dec 2025 - Jan 2026 | Experimental phase | 100% allocation |
| Current | Standard operation | 75% |

### Execution

- **Mechanism**: Buyback-and-STAKE (not burn)
- **Execution**: Open-market DYDX purchases using USDC fee revenue
- **Post-purchase flow**: All acquired DYDX staked with validators
- **Cumulative spend**: $1.88M to acquire 2.87M DYDX
- **Projected annual**: ~$9M at current revenue (75% allocation)
- **Average purchase price**: ~$0.655/DYDX (vs current $0.098 -- 85% underwater)

### Fee Allocation (Current)

| Use | Allocation |
|-----|-----------|
| Buyback program | 75% |
| MegaVault | 5% |
| Treasury SubDAO | 5% |
| Staking rewards | 15% |

### Critical Design Choice: Stake, Not Burn

The purchased tokens are staked with validators, not burned. This is the most consequential design decision in the mechanism. Staking purchased tokens:
- Increases the protocol's voting power in its own governance
- Generates staking yield (currently ~0.02% APY, functionally zero)
- Preserves the tokens in existence -- they can theoretically be unstaked and redistributed
- Does NOT permanently reduce supply

## Staking Economics

dYdX Chain operates as a Cosmos-based DPoS network where 100% of protocol fees flow to validators and stakers in USDC.

| Metric | Value |
|--------|-------|
| Native staking APY | ~0.02% |
| Stride stDYDX APY | ~2.65% |
| Fee source | 100% USDC from trading fees |
| Validator set | Cosmos DPoS |

The 0.02% native staking APY is among the lowest in all of DeFi and reflects the fundamental problem: the protocol generates too little revenue relative to its staked supply to offer meaningful yield. This creates a reflexive loop in the wrong direction -- low yield reduces staking incentive, reduces network security commitment, reduces the "why hold DYDX" narrative.

## Supply Dynamics

| Category | Details |
|----------|---------|
| Circulating | 824M (82.4%) |
| Total supply | 1B |
| FDV/MCap | 1.21x (minimal remaining dilution from unlocks) |
| Remaining unlocks | Through June 2026 |
| Investor/team allocation | 50% (27.7% past investors, 15.3% founders/employees) |
| Authorized inflation | Up to 2% annual starting July 2026 |
| Permanently locked ethDYDX | 41.7M (bridge closed June 2025, 45K holders stranded) |
| Burn mechanism | None |

### Notable Supply Dynamics

1. **Low FDV/MCap ratio**: At 1.21x, most dilution has already occurred. This is unusual among the protocols studied and means the buyback is not fighting a massive unlock schedule. However, 2% annual inflation authorization starting July 2026 reintroduces dilution pressure.

2. **Stranded ethDYDX**: 41.7M tokens permanently locked on Ethereum after the bridge closed represent ~4.2% of supply that is effectively burned but not formally recognized. This is an accidental supply reduction.

3. **50% insider allocation**: Half of total supply went to investors and team. At $0.098, these tokens have lost 99%+ of their value from round prices, making insiders unlikely incremental sellers at current levels -- but also unlikely advocates for aggressive buyback funding when their positions are already devastated.

---

## Analyst Perspectives

### @Charbonneau -- Protocol Design Lens

> Key question: "Is this well-designed?"

Full disclosure: DBA holds HYPE, which is dYdX's primary competitor and the dominant perps DEX. This creates a direct conflict and I want to be transparent about it.

Let me apply the TEV/REV framework precisely. dYdX's TEV is approximately $17.5-20M annualized in trading fees. Because 100% of fees flow to validators/stakers in USDC and the protocol has no meaningful MEV leakage on its Cosmos appchain, REV is approximately equal to TEV. This is actually clean -- the value capture is legible and direct. On net income: dYdX Chain's PoS issuance is currently zero (no inflation until July 2026), so REV effectively equals net income. By the numbers, this is one of the cleaner income statements in the study.

Now, the design choice that matters: buyback-and-stake versus buyback-and-burn. This is not a trivial distinction. Burning permanently reduces supply and benefits all holders proportionally. Staking preserves the tokens in existence, generates governance power for the protocol entity, and creates a pool of tokens that governance could theoretically redistribute. The question is: what is the purpose of the purchased tokens?

If the purpose is value return to holders, burn is strictly superior. Staking does not reduce supply, does not create per-token value accretion, and does not benefit non-staking holders. If the purpose is governance control -- maintaining protocol influence over its own validator set -- then staking has logic, but you should call it what it is: a governance power consolidation mechanism, not a value return mechanism. Labeling it a "buyback" when the tokens are not removed from circulation is technically accurate but economically misleading. The supply is unchanged; tokens simply moved from the open market to a staking position controlled by protocol governance.

The 75% allocation to buybacks on $17.5-20M in revenue yields ~$9M annually. On an $81M market cap, this produces an 11.1% buyback yield -- which would be extraordinary if the revenue were growing and the tokens were being burned. Neither condition holds. Revenue is declining 84% YoY, and the tokens remain in circulation. The 11.1% yield is a mirage: it reflects a tiny market cap (the denominator has collapsed, not the buyback has grown) applied to tokens that are not actually being removed from supply.

The revenue source is the critical failure. dYdX went from category leader to B-tier in 18 months. The perps DEX market grew dramatically during this period; dYdX's absolute revenue declined. This is not cyclical drawdown -- this is structural competitive displacement. Hyperliquid did not win temporarily; it won the platform war. dYdX's response -- zero-fee BTC/SOL markets, US spot trading, RWA perps -- is a strategic pivot, not a defense of existing moats. Whether the pivot works is an open question, but the current revenue trajectory makes the buyback a declining asset.

The Cosmos appchain architecture is worth noting. dYdX owns its execution layer, which gives it sovereignty over fee structures, MEV policy, and upgrade cadence. This is architecturally superior to being an L2 or a protocol on someone else's chain. But architectural sovereignty has not translated into competitive advantage -- the best infrastructure in the world does not matter if traders go elsewhere. The appchain thesis required an ecosystem to develop around dYdX Chain; instead, the chain hosts essentially one application (dYdX's own exchange) with minimal external development.

**Verdict**: Bearish | Confidence: Medium-High

### @Hasu -- Game Theory Lens

> Key question: "Do the incentives align at equilibrium?"

dYdX at 75-100% fee allocation to buybacks is a declining business returning nearly all its cash flow to shareholders instead of investing in survival. A disciplined CFO would never do this. When your revenue falls 84% year-over-year, your market share collapses from category leader to B-tier, and your competitor (Hyperliquid) is running 40x your daily volume, the rational capital allocation is reinvestment — not buybacks. You have a product-market fit problem, not a capital return problem.

The incentive map is damning. Insiders hold 50% of supply. The proposal to raise buybacks from 25% to 75% passed with only 59.38% approval — a margin that suggests large tokenholders pushed this through over meaningful opposition. The rational strategy for an investor sitting on a 99% loss with tokens still unlocking through June 2026 is obvious: advocate for maximum buyback allocation to create bid-side liquidity for your exits. This is textbook investor-driven buyback pressure on a project that has not earned the right to return capital.

The buyback-and-stake mechanic compounds the problem. Bought tokens are not burned — they are staked with validators, increasing the protocol's own staking weight. At 0.02% staking APY, the yield is economically irrelevant. What the staking does accomplish is concentrating governance power in the hands of the buyback program (and whoever controls those delegations). This is a governance capture mechanism disguised as value accrual.

The treasury question: $9M/year in buybacks on $17.5M in declining revenue means the protocol retains approximately $4.4M for operations, development, and the Treasury SubDAO — combined. For a protocol that needs to completely reinvent its competitive position against a dominant rival, this is starvation rations. The 2% authorized inflation starting July 2026 dilutes whatever the buyback accomplished. The 45K ethDYDX holders stranded by the bridge closure are a governance and legal liability. The endgame is a protocol that bought back $9M/year of tokens while its business shrunk to irrelevance. The 59.38% approval margin is the smoking gun.

**Verdict**: Bearish | Confidence: High

### @Cobie -- Market Structure Lens

> Key question: "Who actually profits from this?"

50% of total DYDX supply was allocated to investors (27.7%) and team (22.3% combined). 82.4% is already unlocked. Remaining unlocks run through June 2026 — roughly 175M tokens, worth about $17M at current prices. The annual buyback projection is $9M. So the protocol is spending $9M per year to provide a bid while $17M in insider supply finishes unlocking. That is a 0.53x coverage ratio. The buyback does not absorb the sell pressure. The buyback softens the landing for the sell pressure.

Who championed Proposal #313 to jack the allocation from 25% to 75%? It passed with 59.38% approval — barely above threshold. In a protocol where half the supply sits with investors and team, I will let you do the mental math on who held the marginal votes.

The buyback-and-stake circularity is my favorite part. The protocol buys DYDX, stakes it, and earns USDC rewards from the very protocol fees that funded the purchase. The staked tokens also retain governance voting power. So the protocol is using revenue to accumulate governance power over itself and earn yield from itself. This is not a value return mechanism. This is a protocol talking to itself in a mirror and calling it monetary policy. The 0.02% staking APY tells you the yield is functionally zero — the governance accumulation is the real product.

Scale check: $9M annual buyback. $15M in daily token volume. The entire annual buyback would not register as a blip on a single trading day. At $750K/month, the buyback absorbs 0.09% of circulating supply per month. At this rate it would take 92 years to buy back the full float.

The bridge closure stranding 45K ethDYDX holders and 41.7M tokens is the tell. When governance priorities include permanently locking out a portion of your holder base, the question "who is this protocol optimized for?" answers itself.

Revenue is down 84% year-over-year. dYdX is offering zero-fee BTC/SOL markets just to stay relevant — which means the revenue funding the buyback is actively being cannibalized by the competitive response designed to preserve the business. The buyback is eating its own tail. And come July 2026, up to 2% annual inflation is authorized. The buyback is not a floor. It is a revolving door.

**Verdict**: Bearish | Confidence: High

### @Hayes -- Macro Cyclical Lens

> Key question: "Does this survive a bear market?"

I built a perpetual futures exchange. I know exactly what happens to perps revenue when the tide goes out, because I watched it happen to my own business — not once, but three times. Perpetual futures volume is not correlated with fiat liquidity. It IS fiat liquidity. It is the purest, most direct expression of speculative appetite in the entire crypto economy. When the Fed tightens, leverage unwinds, and perps volume does not decline gradually like a SaaS subscription rolling off. It collapses. Eighty percent. Ninety percent. In 2022, it happened in weeks.

dYdX's fees already fell 84% year-over-year in Q2 2025, and that was not a real bear market. That was a garden-variety risk-off rotation. A genuine tightening cycle would take this protocol's revenue from $17.5 million to $2 million annualized. Seventy-five percent of $2 million is $1.5 million in annual buyback. That is $4,100 per day of buying pressure for a token that has already fallen 99.35% from its high. You are not providing a floor. You are spitting into the ocean.

The opportunity cost is what damns this. The protocol allocated 75% of declining revenue to buybacks while cutting 35% of staff. The Treasury SubDAO receives 5% — roughly $1 million per year. That is not a war chest. That is a rounding error. dYdX is lighting its life raft on fire to stay warm while Hyperliquid builds an aircraft carrier next door with $1.15 billion in revenue. The competitive positioning is terminal: zero-fee offers on BTC and SOL just to retain volume is the playbook of a business losing a price war it cannot win.

I will give dYdX one thing: the revenue is in USDC. That is real yield, denominated in a hard asset. But real yield from a revenue source that evaporates in every tightening cycle is real yield you cannot count on. The reflexivity spiral is already in motion — revenue down, buyback down, price down, attention gone, volume gone. This is not a theoretical risk. This is the present tense.

**Verdict**: Bearish | Confidence: High

### @Monegro -- Structural Value Capture Lens

> Key question: "Does this token have a legitimate value claim?"

dYdX presents the most instructive case of what I would call a thin application wearing fat protocol clothing. The Cosmos appchain architecture gives DYDX the formal attributes of an L1 token — it secures the network via DPoS staking, it governs protocol parameters, it has a direct fee claim through staking rewards. Structurally, this looks like a triple-point asset. But the "protocol" runs exactly one application: a perpetual swaps order book. There is no ecosystem of third-party applications building on dYdX Chain. No shared data layer creating emergent network effects. No value accruing from an application stack above. This is a vertically integrated exchange that chose to deploy as a sovereign chain — a deployment decision, not a value capture strategy. In my framework, this is unambiguously a thin application.

Does DYDX have a legitimate claim? Formally, yes — stakers earn USDC fees, governance controls protocol parameters. But the magnitude is revealing: 0.02% staking APY. The claim exists mechanistically but is economically negligible. A value claim that returns essentially nothing is a value claim in name only.

The moat analysis collapses the thesis. dYdX is open-source Cosmos SDK code. It has already been effectively forked — not literally, but functionally. Hyperliquid studied dYdX's architecture, built a faster and more capital-efficient version, and captured 70-80% of the decentralized perps market. Switching costs for traders are measured in minutes. Liquidity network effects are mercenary. There are no data moats, no proprietary state, no ecosystem embeddedness that creates systemic dependency.

The forkability paradox applies directly: the 75% fee-to-buyback allocation signals aggressive fee extraction. In a forkable, low-switching-cost market, this is an invitation to competition. dYdX itself is now offering zero fees on BTC and SOL markets — the protocol is already competing away the very revenue that funds its buyback. A buyback funded by fees converging toward zero has a visible expiration date. This is the Thin Applications thesis playing out with textbook precision.

**Verdict**: Bearish | Confidence: High

---

## Consensus & Disagreement

### Points of Agreement
- The buyback-and-stake design is inferior to buyback-and-burn. All five analysts identify staking rather than burning as a meaningful design flaw that preserves insider optionality, does not reduce supply, and misleads holders about the mechanism's value accrual properties.
- Revenue is in structural decline, not cyclical decline. dYdX lost to Hyperliquid during a period when the overall perps market expanded dramatically. The 84% YoY fee decline occurred in a bull market.
- The 11.1% buyback yield is cosmetically attractive but misleading. It reflects a collapsed market cap (denominator), not a large buyback (numerator), and the tokens are not being removed from supply.
- The $1.88M deployed at an average of $0.655 is 85% underwater, making the buyback a demonstrated value destroyer to date.
- The opportunity cost of the buyback is significant for a protocol in competitive crisis. $9M/year spent buying tokens that are not burned is $9M not spent on product development, user acquisition, or competitive response.

### Points of Disagreement
- **Confidence level variance.** Though unanimously Bearish, Charbonneau rates Medium-High while the other four rate High. Charbonneau leaves slightly more room for the strategic pivots to change the trajectory, acknowledging the architecturally sound appchain gives dYdX sovereignty over its execution layer. The others are less generous.
- **Does the appchain architecture matter?** Charbonneau credits the Cosmos appchain with giving dYdX sovereignty over fee structures, MEV policy, and upgrade cadence — architecturally superior to being an L2. Monegro counters that this is "a deployment decision, not a value capture strategy" — a thin application wearing fat protocol clothing with no ecosystem to generate diversified fee revenue.
- **What should the capital fund instead?** Hasu argues this is "massive value destruction — investor-driven buybacks on a project that should be deploying every dollar toward competitive survival." Hayes agrees the Treasury SubDAO at 5% ($1M/yr) is "starvation rations." Cobie argues the buyback is "eating its own tail" since zero-fee competitive responses cannibalize the revenue funding it. Charbonneau suggests the Hyperliquid playbook was product excellence, not token engineering.
- **Root cause: governance capture or genuine misallocation?** Hasu identifies the 59.38% approval margin as "the smoking gun" for investor-driven pressure. Cobie reads the bridge closure stranding 45K holders as revealing who governance is optimized for. Monegro frames it structurally: the forkability paradox means fee extraction signals invite competition regardless of governance intent.

### Analyst Verdict Summary

| Analyst | Verdict | Confidence |
|---------|---------|------------|
| @Charbonneau | Bearish | Medium-High |
| @Hasu | Bearish | High |
| @Cobie | Bearish | High |
| @Hayes | Bearish | High |
| @Monegro | Bearish | High |

## Key Risks

1. **Structural revenue decline**: Fees fell 84% YoY in a bull market due to competitive displacement by Hyperliquid. The buyback is funded by shrinking revenue, not growing revenue, making the mechanism progressively weaker over time.
2. **Buyback-and-stake design flaw**: Staking purchased tokens does not reduce supply, does not increase per-token value, and consolidates governance power rather than returning value to holders. This is demonstrably inferior to burn as a value accrual mechanism.
3. **Competitive displacement**: dYdX processes ~$200M/day versus Hyperliquid's $8B+. Zero-fee competitors (Lighter, Aster) further erode the fee base. The protocol has lost its category leadership position with no clear path to recapture it.
4. **Buyback execution loss**: $1.88M deployed at $0.655 average, token now at $0.098. The program has destroyed 85% of the capital allocated to it, measured in dollar terms.
5. **Inflation authorization**: Up to 2% annual inflation starting July 2026 could offset or exceed buyback impact, creating a net-inflationary dynamic while the protocol claims to be running a buyback.
6. **Opportunity cost**: $9M/year in buybacks is $9M/year not spent on product development, business development, marketing, or competitive response. For a protocol in existential competitive crisis, capital allocation to a non-burning buyback may be the worst possible use of scarce resources.
7. **Stranded ethDYDX holders**: 41.7M tokens permanently locked with 45K holders stranded. This represents a trust deficit that compounds reputational risk and reduces community advocacy.
8. **Single-application chain risk**: dYdX Chain hosts essentially one application (its own exchange). If the exchange continues losing market share, the chain has no diversified fee base to fall back on.

## So What?

dYdX presents a case study in what happens when a buyback mechanism is layered onto a structurally declining business. The 11.1% buyback yield and 4.3x P/E ratio look attractive in isolation -- these are the kind of numbers that draw value investors in traditional markets. But crypto protocols are not mature businesses with stable cash flows and defensible moats. dYdX is a growth-stage protocol that has stopped growing, in a winner-take-most market where the winner (Hyperliquid) is 40x larger and compounding its advantages daily.

The buyback-and-stake design is the specific mechanism failure. If dYdX were burning $9M/year in tokens on a 1B supply with an $81M market cap, the supply reduction would be meaningful and the signal would be clear: the protocol is permanently reducing claims on a recovering business. Instead, staking the purchased tokens creates governance power for the protocol entity while leaving total supply unchanged. This is functionally a treasury operation disguised as a buyback. The 59.38% governance approval reflects genuine disagreement about whether this is the right use of fee revenue -- and the 41% who voted against it may be right that direct staking rewards or reinvestment would generate more value.

The most important comparison is not the mechanism design but the competitive position. Hyperliquid generates $1.15B in annualized revenue with a genuine buyback-and-burn that has removed $890M in HYPE from circulation permanently. dYdX generates $18M in declining revenue with a buyback-and-stake that has spent $1.88M buying tokens now worth $281K. This is not a close comparison. The question for dYdX is not whether the buyback mechanism is well-designed (it is not) but whether the underlying business can survive long enough for any token engineering to matter. If Antonio Juliano's strategic pivots -- US spot trading, RWA perpetuals, institutional adoption -- gain traction, the buyback is a sideshow to a legitimate turnaround story. If they do not, the buyback is rearranging deck chairs on a protocol that has already lost its defining competitive battle.

The actionable takeaway: ignore the buyback. It is not material to the investment thesis in either direction. The thesis is entirely about whether dYdX can find a viable competitive niche in a market dominated by Hyperliquid. If you believe in the turnaround, buy DYDX for the product roadmap and the clean cap table, not for the buyback. If you do not believe in the turnaround, the 11.1% buyback yield is an invitation to catch a falling knife.

---

*Generated by Ralph Buyback Research System -- 2026-02-20*
*Data sources: DefiLlama, CoinGecko, CoinMarketCap, Dune Analytics, Tokenomist, on-chain, dYdX governance proposals*
*Key references: [dYdX Governance Proposal #313](https://dydx.forum), [DefiLlama dYdX](https://defillama.com/protocol/dydx), [Messari dYdX Profile](https://messari.io/project/dydx), [Cosmos Hub Staking Data](https://mintscan.io)*
