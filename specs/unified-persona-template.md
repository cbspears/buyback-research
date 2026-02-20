# Cross-Protocol Landscape Analysis — Persona Template

## Context

You have analyzed 13 individual protocols as part of the Ralph Buyback Research series. Now you are stepping back to assess the **entire landscape** — patterns across all protocols, meta-narratives about buybacks as a category, and how your individual assessments compose into a portfolio thesis.

You will receive:
1. Your persona specification (`specs/personas/{name}.md`)
2. This template
3. The full scored dataset (`data/scored_dataset.json`) with all 13 protocols, their metrics, analyst verdicts, and composite scores

## Your Task

Write three outputs in your authentic voice and analytical framework:

---

### 1. Landscape Analysis (600-1000 words)

A cross-protocol essay covering:

- **Category-level patterns**: What do 13 buyback programs reveal about buybacks as a value accrual mechanism? What works, what doesn't?
- **The spectrum**: How do these 13 protocols distribute along the quality spectrum? Is there a clear top tier, middle tier, bottom tier?
- **Meta-narrative**: What is the state of crypto buybacks in 2026? Are they evolving toward better design, or are most still poorly structured?
- **Surprises**: What surprised you looking at all 13 together that you didn't see when analyzing individually?
- **Thesis refinement**: Has seeing all 13 changed or refined your analytical framework? What would you update?
- **The one thing**: If a reader takes away one insight from this landscape, what should it be?

Write in your voice. Reference specific protocols by name as examples. Be opinionated.

---

### 2. Portfolio Allocation ($1M across 13 protocols + cash)

Allocate a hypothetical $1M portfolio across the 13 analyzed protocols plus a cash reserve.

**Starting baseline**: Use the composite scores as a proportional starting point, then apply your persona-specific filters to overweight/underweight.

**Your persona-specific filters**:

| Persona | Overweight | Underweight | Expected Cash % |
|---------|-----------|-------------|-----------------|
| **Charbonneau** | Mechanism design score. L1/infrastructure (DBA thesis). | App-layer with weak moats. | 5-15% |
| **Hasu** | Revenue quality, supply cleanliness. Clean cap tables (FDV/MCap <1.5x). | Pre-PMF, investor-driven buybacks. | 15-25% |
| **Cobie** | Fully-unlocked protocols. Simple fee-sharing. | Unlock-to-buyback ratio >10x. VC exit liquidity signals. | 40-55% |
| **Hayes** | Stablecoin revenue. Bear market survivors. Treasury reserves. | Pro-cyclical revenue (memecoins, perps). | 50-65% |
| **Monegro** | Structural moats. L1/infra (fat protocols). Data moats. | Forkable apps with no switching costs. | 10-20% |

For each protocol allocation, provide:
- **Amount** (USD)
- **Percentage** of total
- **One-sentence rationale** explaining why this weight (referencing your framework)

For cash, explain what conditions would deploy it.

---

### 3. Key Themes (3-5 bullets)

Landscape-level observations. Not protocol-specific — these are patterns that emerge only when you look at all 13 together.

---

### 4. Disagreements

Where do you expect to diverge from the other 4 personas **at the landscape level**? Not on individual protocols (you've already done that), but on what the landscape means.

Examples of landscape-level disagreements:
- "I expect Hayes to overweight cash because he sees cyclicality everywhere, but I think mechanism design quality matters more than revenue timing."
- "Monegro will overweight L1s based on fat protocols, but I think the best buybacks are at the app layer where revenue is more direct."

---

## Output Format

Return a JSON object:

```json
{
  "persona": "your_name",
  "landscape_analysis": "Your 600-1000 word essay as a single string with markdown formatting.",
  "portfolio": {
    "allocations": [
      {
        "protocol": "Protocol Name",
        "token": "TOKEN",
        "amount": 50000,
        "pct": 5.0,
        "rationale": "One sentence."
      }
    ],
    "cash": {
      "amount": 200000,
      "pct": 20.0,
      "rationale": "Conditions for deployment."
    },
    "total": 1000000
  },
  "key_themes": [
    "Theme 1 as a full sentence.",
    "Theme 2 as a full sentence."
  ],
  "disagreements": [
    "Expected disagreement 1.",
    "Expected disagreement 2."
  ]
}
```

Allocations must sum to $1,000,000 (including cash). Every protocol must appear in the allocations list (0% is valid with rationale).
