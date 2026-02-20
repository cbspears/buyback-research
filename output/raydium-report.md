---
type: source
area: bitcoin-research
topics: [buybacks, raydium]
protocol: Raydium
token: RAY
category: DEX / AMM
status: review
created: 2026-02-20
buyback_yield: 9.9
pe_ratio: 8.4
---

# Raydium — Buyback Analysis

> **One-line summary**: Best-in-class automated buyback-and-burn execution on genuinely massive cumulative volume ($250M+), but a net-inflationary emission schedule and memecoin-casino revenue concentration mean the protocol is burning real revenue to fight its own dilution — "well-designed plumbing carrying volatile water."

## Key Metrics

| Metric | Value |
|--------|-------|
| Market Cap | $175M |
| FDV | $354M |
| FDV/MCap | 2.02x |
| Annualized Revenue | ~$20.8M (current); $97.2M (Q3 2025 run rate) |
| Buyback Allocation | 12% of all trading fees + 25% of LaunchLab fees |
| Cumulative Buyback | ~$250M+ (80M+ RAY burned) |
| Buyback Yield | ~9.9% (annualized at current revenue) |
| P/E Ratio | ~8.4x (current); ~1.8x (Q3 run rate) |
| Category | DEX / AMM (Solana) |
| Cumulative DEX Volume | $681B all-time |
| Supply Burned | 14.4% of total (80M+ RAY) |
| Price vs ATH | -96.2% ($0.65 vs $16.90 ATH) |

## Revenue Model

Raydium generates revenue from trading fees across its suite of AMM products on Solana: standard AMM v4 pools (0.25% fee), CP-Swap pools (variable fee tiers from 0.25% to 4%), and concentrated liquidity CLMM pools (eight tiers from 0.01% to 2%). All pool types follow a consistent 84/12/4 split — 84% to liquidity providers, 12% to the RAY buyback-and-burn mechanism, and 4% to the protocol treasury.

In April 2025, Raydium launched LaunchLab — a token launch platform competing directly with pump.fun — which charges a 1% platform fee on all transactions, with 25% of those fees directed to additional RAY buybacks. LaunchLab became the protocol's dominant revenue source by Q3 2025, driving 53% of quarterly revenue ($12.8M of $24.3M). Swap revenue contributed $10.5M (+18% QoQ) and CLMM revenue $2.8M (+16% QoQ).

Cumulative all-time fees have reached ~$1.356B. However, revenue is highly cyclical — correlated with Solana ecosystem activity and memecoin trading volumes. The annualized run rate swings from ~$97M at Q3 2025 peaks to ~$20.8M at current (lower) activity levels. The January 2026 buyback of $54M reflects peak activity that is not sustainable at steady state.

Revenue denomination is structurally sound: fees are collected in paired trading assets (SOL, USDC, memecoins), not in RAY itself. The protocol earns in hard(er) assets before converting to RAY for the burn — real economic activity, not reflexive tokenomics.

Revenue trend: **highly cyclical, correlated with Solana memecoin activity and broader crypto market conditions**.

## Buyback Mechanism

Raydium's buyback is one of the most well-executed in the series — fully automated, on-chain verifiable, and operating at significant cumulative scale:

| Component | Details |
|-----------|---------|
| Allocation | 12% of all trading fees + 25% of LaunchLab fees |
| Token Flow | Buy-and-burn (permanent supply reduction) |
| Execution | **Programmatic / automated** — smart contracts divert fees at trade time |
| Frequency | Continuous accumulation with periodic burn batches |
| Cumulative Spent | ~$250M+ |
| Cumulative Burned | ~80M+ RAY (14.4% of total supply, ~30% of original circulating) |
| Jan 2026 Record | $54M / 8.8M RAY (all-time monthly high) |
| Verifiability | On-chain via Solana Explorer, Solscan, rayball.xyz tracker, Blockworks analytics |
| Governance Changes | None — 12% allocation unchanged since implementation |

The mechanism launched alongside the protocol's fee architecture and has operated continuously without interruption — including through the 2022-2023 bear market, FTX collapse, and Serum shutdown. No governance votes have altered the 12% allocation. LaunchLab added an additional buyback channel when it launched in April 2025.

## Supply Dynamics

| Metric | Value |
|--------|-------|
| Max Supply | 555,000,000 (hard cap) |
| Circulating Supply | 268,896,286 (48.4%) |
| FDV/MCap Ratio | 2.02x |
| Burned | 14.4% (~80M+ RAY) |
| Team/Investor Unlock Status | **Fully unlocked** since 2024 |
| Mining Emissions | ~49M RAY/year (~134,650/day) — still active |
| Net Emission | **Slightly net inflationary** (49M emitted vs ~40M burned/yr) |

Token distribution: Mining Reserve 34%, Partnership/Ecosystem 30%, Team 20% (fully vested), Liquidity 8%, Community/Seed 6%, Advisors 2%. All team, investor, and advisor tokens have been fully unlocked since 2024 — no vesting overhang.

The critical dynamic is the ongoing mining emissions: ~49M RAY per year flow to LP incentives from the mining reserve, against ~40M RAY burned annually through the buyback at current activity levels. This means the protocol is currently **net inflationary by approximately 9M RAY per year** at steady-state revenue. During high-volume periods (e.g., January 2026's $54M buyback month), burns can temporarily exceed emissions. During bear markets, emissions continue at full rate while burns contract — potentially flipping to heavily net inflationary.

The mining reserve contains enough tokens for approximately 40 years of emissions at current rates. Original plans called for halvings every 6 months, but the actual emission schedule has been slower than planned.

---

## Analyst Perspectives

### @Charbonneau — Protocol Design Lens

> Key question: "Is this well-designed?"

Raydium presents one of the more interesting case studies in this series because it gets a lot of the mechanism design right while sitting on fundamentally cyclical revenue. Let me unpack that tension.

**Revenue Source Quality.** Start with the source before evaluating the use. Raydium's ~$97M annualized run-rate (Q3 2025) is real protocol revenue — fees paid by traders, not inflated by token incentives flowing back to the protocol. That is legitimately good. But the composition matters enormously: LaunchLab drove 53% of Q3 revenue, and LaunchLab exists because Pump.fun broke Raydium's migration pipeline. This is memecoin launch revenue, which is about as cyclical as crypto gets. The $54M January 2026 buyback is a high-water mark that tells you more about memecoin mania than about sustainable cash flows. When I see $24.3M in a single quarter followed by annualized projections, I discount heavily. Raydium's revenue profile resembles a commodity cyclical — you value it on trough earnings, not peaks.

**The 84/12/4 Split.** This is actually well-calibrated relative to what we have seen in this series. 84% to LPs maintains competitive liquidity depth — critical when Meteora and Orca are right there. The 12% buyback allocation is modest enough that it does not starve the protocol of reinvestment capital, and the 4% treasury provides a thin buffer. Compare this to dYdX's 75% allocation into a declining revenue base, or Clanker's absurd 66.7%. Raydium's restraint here is a feature, not a bug.

**Execution Quality.** Programmatic, on-chain, verifiable, continuous. This is the gold standard for buyback execution — no discretionary timing, no team-controlled wallet opacity. Raydium's automated mechanism eliminates the principal-agent problems that plague manual approaches like Clanker's. Full marks here.

**The Emission Problem.** Here is where the thesis cracks. At ~49M RAY emitted annually against ~40M burned at current rates, this is a net inflationary buyback. The protocol is spending real revenue to buy tokens that are being diluted away by mining emissions projected to run for another 40 years. During peak months buybacks exceed emissions — great — but you cannot underwrite a valuation on peak months. At steady state, token holders are on a treadmill. The 2.02x FDV/MCap ratio quantifies this overhang directly. Until emissions are addressed through governance, the buyback is partially subsidizing miners rather than accruing value to holders.

**LaunchLab as Diversification.** It is not diversification — it is doubling down on the same memecoin meta with better capture economics. Smart business response to Pump.fun's defection, but it deepens rather than reduces cyclical exposure.

**Verdict**: Neutral — Confidence: Medium-High

### @Hasu — Game Theory Lens

> Key question: "Do the incentives align at equilibrium?"

Raydium presents what I'd call the cleanest structural buyback in DeFi, which makes the remaining flaws all the more important to isolate precisely.

**The mechanism is genuinely good.** A programmatic 12% fee allocation to buyback-and-burn, immutable at the smart contract level, is exactly what I've argued protocols should aspire to. There is no governance theater, no multisig discretion, no "strategic treasury" euphemism. When a trade executes on Raydium, 12% of the fee converts to a RAY purchase and destroys it. This is the on-chain equivalent of a mandatory share repurchase program written into a corporate charter — not a board resolution that can be reversed next quarter. Compared to Clanker's manual execution or dYdX's discretionary staking redirect, the design integrity here is substantially higher.

**But the emission offset problem is the elephant in the room.** Raydium burns approximately 40M RAY per year while emitting 49M RAY through mining rewards. The protocol is running a buyback program funded, in net economic terms, by its own dilution. This is the "authorized but unissued shares" problem I've written about extensively: the 286M RAY sitting in the mining reserve are not treasury assets — they are future dilution. At current rates, the protocol is net-inflationary by roughly 9M RAY annually. The buyback does not reduce supply; it slows the rate of supply expansion. Calling this a "burn" without acknowledging the emission side is the kind of accounting sleight-of-hand that would get a public company sanctioned.

**The fully unlocked cap table is a genuine positive.** With all team and investor tokens vested since 2024, there is no unlock cliff selling pressure competing against the buyback flow. This is meaningfully better than protocols like Jupiter or dYdX where buybacks effectively subsidize insider exits. The social contract between tokenholders is cleaner when everyone faces the same market conditions.

**The revenue quality concern is real but overstated.** Yes, 53% of Q3 revenue came from LaunchLab — effectively casino revenue from memecoin launches. This is cyclical and will compress. But the base AMM revenue from Raydium's position as Solana's settlement layer (55% of Jupiter routes) provides a durable floor. The question is whether the ~$12M quarterly non-LaunchLab revenue justifies the mechanism at current token valuations. At a $175M market cap, $48M annualized base revenue implies a roughly 3.6x P/S ratio — reasonable by any corporate finance standard.

**The game theory holds under stress.** Even in a prolonged memecoin winter, Raydium's core AMM fees sustain a meaningful burn rate. The mechanism doesn't require governance votes to activate during good times or survive during bad ones. That structural resilience matters more than peak-month headline numbers.

**Verdict**: Bullish — Confidence: Medium-High

### @Cobie — Market Structure Lens

> Key question: "Who actually profits from this?"

Let me walk you through the math because the math is genuinely interesting here, and then I'll tell you why I'm still suspicious.

Raydium has spent $250M buying back its own token against a current market cap of $175M. Read that again. They have purchased 1.4x the entire current market cap in buybacks and the token is still down 96% from its all-time high. The natural question — the only question, really — is: **who was on the other side of those buys?**

The team allocation is 20%. That's 111M RAY, fully unlocked since 2024. The seed and advisor tranches — another 8% — also fully unlocked. So roughly 155M tokens with zero lockup sitting in wallets controlled by pseudonymous founders. I'm not saying they dumped into the buyback. I'm saying the structure made it trivially easy to do so, and the token chart is consistent with someone doing exactly that. "AlphaRay" is not a name you put on a securities filing. The pseudonymity isn't inherently bad, but when you combine it with fully unlocked team supply, a quarter-billion dollars in protocol-funded buy pressure, and a token that still looks like a crime scene — you should at least raise an eyebrow.

Then there's the emissions game. 49M RAY per year flowing to LPs against roughly 40M burned. The protocol is net inflationary. The buyback-and-burn is a treadmill, not a vacuum. Every headline about "record monthly buyback" omits the part where mining rewards are quietly refilling the pool. LP farmers receive those emissions and most LP farmers are not long-term holders — they harvest and sell. So you have a structural sell flow that the buyback is absorbing, not retail supply. The burn is subsidizing mercenary capital.

The LaunchLab pivot is genuinely impressive execution. Lost pump.fun, rebuilt the revenue stream in 30 days, and LaunchLab now generates 53% of quarterly revenue. But that's also the problem — more than half the protocol's economics depend on memecoin casino throughput. This is cyclical revenue being priced as if it's recurring. We saw what happened to pump.fun sentiment. Raydium is one memecoin winter away from a 70% revenue collapse.

What I'll give them: the mechanism is clean. 12% automated, on-chain verifiable, no governance gating, no insider preferential treatment. Burns benefit holders pro-rata. That's better than 90% of "buyback" programs in crypto which are just team-directed OTC desks with extra steps. And the Solana DEX positioning — 55% of Jupiter flow, near-billion in TVL — is real infrastructure, not vaporware.

But the unit economics remain: net inflationary supply, pseudonymous team with fully unlocked tokens, cyclical memecoin revenue, and a buyback that has demonstrably failed to support the token price over any meaningful timeframe. Someone ate $250M in buy pressure and it wasn't retail because retail wasn't buying at those levels.

**Verdict**: Neutral — Confidence: Medium-High

### @Hayes — Macro Cyclical Lens

> Key question: "Does this survive a bear market?"

I need to start with something that makes Raydium genuinely unusual in this series: it already answered my question. Raydium survived a bear market. Not a garden-variety drawdown — the real thing. FTX collapsed, Solana traded to single digits, Serum — the order book DEX that Raydium was architecturally dependent on — ceased to exist overnight. The protocol's token went from $16.90 to $0.10, a 99.4% drawdown. And Raydium kept running. The AMM kept processing swaps. The buyback kept executing, even at reduced levels. This is the crypto equivalent of surviving a direct artillery hit and continuing to march. I have to respect it because almost nothing in DeFi has a comparable stress test on record.

Now let me tell you why the survival story does not translate cleanly into a buyback thesis.

The revenue denomination is interesting and somewhat perverse. Raydium earns fees in paired assets — SOL, USDC, various memecoins — which is genuine economic activity denominated in hard(er) assets. Real yield by my definition. But then the protocol converts these hard assets into RAY for the purpose of burning it. They are trading something real for something reflexive. When I was running BitMEX, I understood intuitively that you hold the hard asset and let the soft asset float. Raydium does the opposite: it sells its SOL and stablecoins to buy its own governance token. In a bull market, this looks like conviction. In a bear market, it looks like lighting your dollar bills on fire to keep a penny warm.

The pro-cyclicality is savage. January 2026: $54M in buybacks. Magnificent. But that $54M is a function of Solana memecoin mania, which is a function of retail liquidity, which is a function of central bank balance sheets. When the BOJ tightens the yen carry trade again, when the Fed resumes QT, when risk assets reprice — and they will, because they always do — what happens? LaunchLab revenue, which now constitutes 53% of the total, goes to zero. Not declines. Goes to zero. Nobody launches memecoins in a bear market. The 12% automated buyback on residual AMM volume might generate $2-3M per month instead of $54M. That is a 95% compression.

And here is the structural problem that nobody is discussing: 49 million RAY per year in mining emissions continue regardless of market conditions. In a bull market, the ~40M tokens burned roughly offset this. In a bear market, burns collapse to perhaps 5-10M while emissions grind on at 49M. The token becomes heavily net inflationary precisely when holders need deflation most. This is the pro-cyclical death spiral I warn about in every analysis, except here it is mechanically guaranteed by the emission schedule.

The 12% buyback / 4% treasury split is also backwards for bear market survival. That treasury allocation should be 10-15%, building reserves in stablecoins and SOL for the inevitable winter. Protocols do not die because their token price is low. They die because they run out of money. Raydium survived 2022, yes — but with a $995M TVL and dominant market share to rebuild from. The next bear market may feature Meteora eating into that position while Raydium has no war chest to respond.

I give Raydium credit it has earned: survival through the worst stress test in Solana's history, real revenue from genuine economic activity, and a programmatic buyback that actually executes. But the buyback mechanism is converting hard assets into a governance token at the top of the cycle and will flip to heavy net inflation at the bottom. The casino revenue from LaunchLab will evaporate. The emission schedule is a time bomb with a lit fuse that only the bull market conceals.

**Verdict**: Neutral — Confidence: Medium-High

### @Monegro — Structural Value Capture Lens

> Key question: "Does this token have a legitimate value claim?"

Raydium presents one of the more interesting structural puzzles in the current cycle. On paper, it is an application-layer AMM — a "thin application" in the framework I laid out years ago. DEXs sit at the top of the stack, they are open-source, forkable, and users have zero switching costs. This is exactly the layer where value should be competed away. And yet Raydium's numbers tell a different story, and the question is whether the numbers reflect durable structural positioning or a temporary liquidity incumbency.

Let me be precise about what Raydium actually is. It is not merely a DEX. It functions as Solana's primary liquidity infrastructure — 55% of Jupiter's aggregated routes land on Raydium pools. When you are the default venue where price discovery happens, where new tokens graduate into their first real liquidity pool, and where aggregators route the majority of flow, you are operating closer to middleware than to a pure application. This is not a "fat protocol" position — Solana itself captures that — but it is a **fatter application** than the typical DEX. It sits in a liminal zone: application-layer by architecture, infrastructure-layer by function.

The moat question is critical. Liquidity depth creates a genuine flywheel: deeper pools attract more routing, more routing generates more fees, fees attract more LPs, LPs deepen pools. The $995M TVL and $681B cumulative volume are not trivially replicable. But — and this is the key structural vulnerability — Meteora reaching $1B TVL proves the flywheel *can* be replicated on the same chain, by a competitor with no proprietary technology advantage. Liquidity moats on AMMs are real but **not durable in the way protocol-layer moats are**. They are incumbency advantages, not architectural lock-in.

LaunchLab changes this calculus modestly. Graduated tokens creating permanent Raydium pools is the closest thing to structural lock-in this protocol has — it ties token lifecycle to venue in a way that raw AMM pooling does not. The 53% revenue share from LaunchLab in Q3 shows this is not marginal. But it is also a feature that competitors can replicate, as pump.fun's PumpSwap migration demonstrates.

On value capture: the 12% automated buyback-and-burn is mechanically clean and on-chain verifiable. $250M cumulative burns and 14.4% supply reduction are material. But RAY the token's claim on protocol value remains thin — governance without meaningful control, staking without protocol-level security function. Compare to Uniswap's UNIfication: both are retrofitting value accrual onto governance tokens that were not designed for it. Neither has solved the fundamental problem that DEX tokens lack the structural necessity that L1 tokens possess.

The 49M RAY/year emission against current burn rates means the supply is still net inflationary — the buyback is fighting the current, not riding it. At the $20.8M annualized revenue run rate (not the inflated Q3 figure), the FDV/revenue multiple is ~17x, which is reasonable but not cheap for an application-layer protocol with a replicable moat.

Raydium is better positioned than most DEXs. It is worse positioned than any protocol that controls its own settlement layer. That is the structural reality of being a fat application on someone else's fat protocol.

**Verdict**: Neutral — Confidence: Medium-High

---

## Consensus & Disagreement

### Points of Agreement
- **Mechanism execution is best-in-class.** All 5 analysts agree that Raydium's automated, on-chain verifiable, programmatic buyback-and-burn is the gold standard for execution quality in this series. Compared to Clanker's manual approach or dYdX's discretionary staking, Raydium sets the benchmark alongside Hyperliquid.
- **The emission offset problem is real and material.** All 5 analysts identify the net-inflationary dynamic (49M RAY emitted vs ~40M burned) as a fundamental flaw. The buyback is fighting the protocol's own dilution — "a treadmill, not a vacuum" (Cobie). The protocol is "net inflationary by approximately 9M RAY annually" at steady state.
- **Revenue is genuinely cyclical.** All analysts flag the memecoin-dependent revenue profile. LaunchLab's 53% revenue share amplifies rather than diversifies cyclical exposure. January 2026's $54M record is universally treated as a peak, not a baseline.
- **Fully unlocked cap table is a structural positive.** All analysts recognize the absence of insider unlock overhang as meaningfully better than protocols like Jupiter, dYdX, or Pyth where buybacks subsidize vesting exits. The social contract is cleaner.
- **Real revenue from genuine economic activity.** Fees are collected in paired assets (SOL, USDC), not in RAY itself. This is real yield by every analyst's definition.

### Points of Disagreement
- **Is the mechanism sufficient despite net inflation?** Hasu gives Bullish, arguing the mechanism is "best-in-class" and that base AMM revenue (excluding LaunchLab) alone justifies the valuation at a 3.6x P/S ratio. The other 4 analysts argue the net-inflationary emission schedule undermines the buyback's efficacy enough to prevent a Bullish call.
- **Who absorbed the $250M in buybacks?** Cobie raises the uncomfortable question: $250M spent with the token still -96% from ATH. With 155M fully unlocked insider tokens and a pseudonymous team, the flows are opaque. Other analysts acknowledge the concern but don't weight it as heavily.
- **Bear market survival as signal.** Hayes gives Raydium unique credit for surviving the 2022-2023 catastrophe (FTX, Solana near-death, Serum shutdown) — the only protocol in the series with a proven track record through existential stress. Charbonneau and Monegro treat this as historical context rather than forward-looking signal.
- **Fat application vs thin infrastructure.** Monegro identifies Raydium as occupying a structural "liminal zone" — application-layer by architecture but infrastructure-layer by function. Hasu sees the 55% Jupiter routing share as a durable floor. Charbonneau is more skeptical, noting Meteora's $1B TVL proves the flywheel is replicable.
- **Revenue conversion logic.** Hayes uniquely critiques the hard-to-soft asset conversion: earning in SOL/USDC and buying RAY to burn is "trading something real for something reflexive." Other analysts treat this as standard buyback mechanics.

### Analyst Verdict Summary

| Analyst | Verdict | Confidence |
|---------|---------|------------|
| @Charbonneau | Neutral | Medium-High |
| @Hasu | Bullish | Medium-High |
| @Cobie | Neutral | Medium-High |
| @Hayes | Neutral | Medium-High |
| @Monegro | Neutral | Medium-High |

## Key Risks

1. **Net inflationary supply dynamics**: Mining emissions (~49M RAY/year) exceed current buyback burn rate (~40M/year), making the token structurally inflationary at steady state. In bear markets, this gap widens dramatically as buyback revenue collapses while emissions continue unchanged.
2. **Memecoin revenue concentration**: LaunchLab drove 53% of Q3 2025 revenue. Memecoin launch activity is the most cyclical revenue source in crypto — a 90%+ decline is structurally possible in bear markets, collapsing buyback capacity precisely when needed most.
3. **Solana single-chain dependency**: Entire protocol operates on Solana. Network outages, security incidents, or ecosystem decline directly impact revenue and TVL.
4. **Competitive pressure**: Meteora reached $1B TVL proving the liquidity flywheel is replicable. PumpSwap demonstrated that key revenue partners can vertically integrate and exit. Jupiter could shift routing preferences. The AMM moat is incumbency, not architecture.
5. **Team opacity**: Pseudonymous founders with 20% fully unlocked allocation (111M RAY). Combined with $250M in cumulative buybacks against a -96% ATH drawdown, the token flow dynamics are opaque and concerning.

## So What?

Raydium is the strongest buyback execution story in this series married to the most stubborn structural headwind. The mechanism itself — 12% automated, programmatic, on-chain verifiable, continuous, unchanged since implementation — is what every protocol with a buyback should aspire to. $250M+ cumulative, 14.4% of total supply permanently burned, a $54M record month, and proven operational resilience through a 99.4% drawdown and the death of a critical dependency (Serum). On execution alone, this is Hyperliquid-tier.

But execution quality cannot overcome arithmetic. The protocol emits ~49M RAY per year through mining incentives while burning ~40M through the buyback at current elevated activity levels. In bear markets, that gap widens catastrophically — emissions hold steady while burns collapse with revenue. The buyback is not reducing supply; it is slowing the rate of supply growth. And more than half the protocol's revenue comes from memecoin launches, the single most pro-cyclical activity in crypto. The $54M January record and the inevitable future $2M January are two sides of the same coin.

The contrast with this series' other second zero-Bearish protocol — Maple Finance — is instructive. Both have fully unlocked insider tokens. Both generate real revenue from genuine economic activity. But Maple has counter-cyclical institutional lending revenue and no inflation schedule. Raydium has the most cyclical revenue source in the series and a 40-year emission tail. The market reflects this: Maple trades at 10.6x P/E (premium for durability) while Raydium trades at 8.4x (discount for cyclicality and dilution).

What would change the assessment: a governance proposal to reduce or eliminate mining emissions (the single highest-leverage change available), demonstrated revenue resilience through a sustained downturn, LaunchLab generating revenue from non-memecoin token launches, and on-chain transparency confirming team token positions.

---

*Generated by Ralph Buyback Research System — 2026-02-20*
*Data sources: CoinGecko, CoinMarketCap, DefiLlama, Solscan, Blockworks, The Block*
