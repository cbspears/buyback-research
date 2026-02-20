#!/usr/bin/env python3
"""5-dimension composite scoring and ranking engine.

Reads data/master_dataset.json, computes scores across 5 dimensions,
and outputs data/scored_dataset.json with rankings.
"""

import json
import statistics
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Dimension 1: Buyback Yield (0-100)
# ---------------------------------------------------------------------------

def score_buyback_yield(protocols: list[dict]) -> dict[str, float]:
    """Percentile rank with penalty for extreme yields (>25%)."""
    yields = {}
    for p in protocols:
        y = p.get('buyback_yield')
        if y is not None and y > 0:
            yields[p['protocol']] = y

    if not yields:
        return {p['protocol']: 0 for p in protocols}

    sorted_vals = sorted(yields.values())
    n = len(sorted_vals)

    scores = {}
    for p in protocols:
        name = p['protocol']
        y = yields.get(name)
        if y is None:
            scores[name] = 0
            continue

        # Percentile rank (0-100)
        rank = sorted_vals.index(y) + 1
        percentile = (rank / n) * 100

        # Penalty: yields >25% get 20% haircut
        if y > 25:
            percentile *= 0.8

        scores[name] = round(min(percentile, 100), 1)

    return scores


# ---------------------------------------------------------------------------
# Dimension 2: Revenue Quality (0-100)
# ---------------------------------------------------------------------------

CATEGORY_SCORES = {
    'l1': 25, 'perps l1': 25,
    'lending': 20, 'rwa lending': 20, 'rwa lending / on-chain asset management': 20,
    'aggregator': 20,
    'oracle': 18, 'oracle / middleware infrastructure': 18,
    'dex': 15, 'dex / amm': 15, 'amm': 15,
    'perps dex': 15, 'perps dex (cosmos appchain)': 15, 'perps dex (bnb chain)': 15,
    'liquid staking': 15, 'liquid restaking': 15,
    'stablecoin / synthetic dollar': 15,
    'launchpad': 8, 'token deployer': 8, 'token deployer / launchpad': 8,
}


def score_revenue_quality(protocols: list[dict]) -> dict[str, float]:
    """Revenue denomination, P/E percentile, category quality, cost basis."""
    # Collect valid P/E ratios for percentile calc
    pe_vals = []
    for p in protocols:
        pe = p.get('pe_ratio')
        if pe is not None and pe > 0:
            pe_vals.append(pe)

    scores = {}
    for p in protocols:
        name = p['protocol']
        total = 0

        # Revenue denomination (0-25)
        denom = p.get('revenue_denomination', 'unknown')
        if denom == 'stablecoin':
            total += 25
        elif denom == 'mixed':
            total += 15
        elif denom == 'native':
            total += 0

        # P/E percentile inverse (0-25): lower P/E = higher score
        pe = p.get('pe_ratio')
        if pe is not None and pe > 0 and pe_vals:
            if pe > 100:
                pe_score = 0
            else:
                # Count how many have higher P/E (worse)
                better_count = sum(1 for v in pe_vals if v >= pe)
                pe_score = (better_count / len(pe_vals)) * 25
            total += pe_score

        # Category diversity score (0-25)
        cat = (p.get('category') or '').lower().strip()
        cat_score = CATEGORY_SCORES.get(cat, 10)
        total += cat_score

        # Cost basis: if price vs ATH is deeply negative, score lower (0-25)
        ath_pct = p.get('price_vs_ath_pct')
        if ath_pct is not None:
            # ath_pct is negative (e.g. -65.5 means 65.5% below ATH)
            drawdown = abs(ath_pct) if ath_pct < 0 else ath_pct
            # 0% drawdown = 25pts, 100% drawdown = 0pts
            cost_score = max(0, 25 * (1 - drawdown / 100))
            total += cost_score
        else:
            total += 12.5  # neutral if unknown

        scores[name] = round(min(total, 100), 1)

    return scores


# ---------------------------------------------------------------------------
# Dimension 3: Supply Cleanliness (0-100)
# ---------------------------------------------------------------------------

def score_supply_cleanliness(protocols: list[dict]) -> dict[str, float]:
    """FDV/MCap ratio, % circulating, unlock status."""
    scores = {}
    for p in protocols:
        name = p['protocol']
        total = 0

        # FDV/MCap: 1.0x=30pts, linear decay to 0 at 4.0x
        fdv_mcap = p.get('fdv_mcap_ratio')
        if fdv_mcap is not None:
            if fdv_mcap <= 1.0:
                total += 30
            elif fdv_mcap >= 4.0:
                total += 0
            else:
                total += 30 * (1 - (fdv_mcap - 1.0) / 3.0)

        # % Circulating: 100%=30pts, linear to 0 at 20%
        pct_circ = p.get('pct_circulating')
        if pct_circ is not None:
            if pct_circ >= 100:
                total += 30
            elif pct_circ <= 20:
                total += 0
            else:
                total += 30 * (pct_circ - 20) / 80

        # Unlock status (0-40): fully unlocked is best
        unlock = (p.get('unlock_status') or '').lower()
        if 'fully unlocked' in unlock or 'fully vested' in unlock:
            total += 40
        elif 'partial' in unlock:
            total += 20
        elif unlock:
            # Some unlock info exists but not fully unlocked
            total += 10
        else:
            # Check fdv_mcap as proxy: near 1.0 implies mostly unlocked
            if fdv_mcap is not None and fdv_mcap < 1.2:
                total += 35
            elif fdv_mcap is not None and fdv_mcap < 1.5:
                total += 25
            elif fdv_mcap is not None and fdv_mcap < 2.0:
                total += 15
            else:
                total += 5

        scores[name] = round(min(total, 100), 1)

    return scores


# ---------------------------------------------------------------------------
# Dimension 4: Analyst Consensus (0-100)
# ---------------------------------------------------------------------------

VERDICT_SCORES = {'Bullish': 2, 'Neutral': 1, 'Bearish': 0}
CONFIDENCE_WEIGHTS = {
    'High': 1.5,
    'Medium-High': 1.25,
    'Med-High': 1.25,
    'Medium': 1.0,
    'Low': 0.75,
}


def score_analyst_consensus(protocols: list[dict]) -> dict[str, float]:
    """Weighted verdict scoring normalized to 0-100."""
    scores = {}
    for p in protocols:
        name = p['protocol']
        verdicts = p.get('verdicts', [])

        if not verdicts:
            scores[name] = 50  # neutral default
            continue

        weighted_sum = 0
        weight_total = 0

        for v in verdicts:
            verdict_val = VERDICT_SCORES.get(v.get('verdict', ''), 1)
            conf = v.get('confidence', 'Medium')
            conf_weight = CONFIDENCE_WEIGHTS.get(conf, 1.0)

            weighted_sum += verdict_val * conf_weight
            weight_total += conf_weight

        if weight_total > 0:
            # Max possible = 2 * weight_total (all Bullish High)
            raw = weighted_sum / weight_total  # 0 to 2
            normalized = (raw / 2) * 100
        else:
            normalized = 50

        scores[name] = round(normalized, 1)

    return scores


# ---------------------------------------------------------------------------
# Dimension 5: Mechanism Design (0-100)
# ---------------------------------------------------------------------------

TOKEN_FLOW_SCORES = {'burn': 30, 'distribute': 18, 'stake': 15, 'hold': 12, 'lock': 12}
EXECUTION_SCORES = {'automated': 25, 'periodic': 18, 'manual': 10, 'unknown': 5}
TRANSPARENCY_SCORES = {'on-chain verifiable': 25, 'dashboard': 15, 'opaque': 0}


def score_mechanism_design(protocols: list[dict]) -> dict[str, float]:
    """Token flow + execution + transparency scoring."""
    scores = {}
    for p in protocols:
        name = p['protocol']
        total = 0

        # Token flow: take the best mechanism type (0-30)
        mechanisms = p.get('mechanism_types', ['unknown'])
        best_flow = max(TOKEN_FLOW_SCORES.get(m, 0) for m in mechanisms)
        total += best_flow

        # Execution type (0-25)
        exec_type = p.get('execution_type', 'unknown')
        total += EXECUTION_SCORES.get(exec_type, 5)

        # Automation component — inferred from execution (0-20)
        if exec_type == 'automated':
            total += 20
        elif exec_type == 'periodic':
            total += 12
        elif exec_type == 'manual':
            total += 5
        else:
            total += 5

        # Transparency (0-25)
        transp = p.get('transparency', 'opaque')
        total += TRANSPARENCY_SCORES.get(transp, 0)

        scores[name] = round(min(total, 100), 1)

    return scores


# ---------------------------------------------------------------------------
# Composite scoring
# ---------------------------------------------------------------------------

def compute_composite(protocols: list[dict]) -> list[dict]:
    """Compute all 5 dimensions and composite score for each protocol."""
    d1 = score_buyback_yield(protocols)
    d2 = score_revenue_quality(protocols)
    d3 = score_supply_cleanliness(protocols)
    d4 = score_analyst_consensus(protocols)
    d5 = score_mechanism_design(protocols)

    results = []
    for p in protocols:
        name = p['protocol']

        dimensions = {
            'buyback_yield_score': d1.get(name, 0),
            'revenue_quality_score': d2.get(name, 0),
            'supply_cleanliness_score': d3.get(name, 0),
            'analyst_consensus_score': d4.get(name, 0),
            'mechanism_design_score': d5.get(name, 0),
        }

        composite = round(
            sum(dimensions.values()) / 5, 1
        )

        results.append({
            **p,
            **dimensions,
            'composite_score': composite,
        })

    # Sort by composite score descending
    results.sort(key=lambda x: x['composite_score'], reverse=True)

    # Add ranks
    for i, r in enumerate(results):
        r['rank'] = i + 1

    return results


def compute_statistics(scored: list[dict]) -> dict:
    """Compute summary statistics across the scored dataset."""
    composites = [s['composite_score'] for s in scored]
    yields = [s['buyback_yield'] for s in scored if s.get('buyback_yield')]
    pe_ratios = [s['pe_ratio'] for s in scored if s.get('pe_ratio') and s['pe_ratio'] < 500]

    stats = {
        'count': len(scored),
        'composite': {
            'mean': round(statistics.mean(composites), 1) if composites else 0,
            'median': round(statistics.median(composites), 1) if composites else 0,
            'stdev': round(statistics.stdev(composites), 1) if len(composites) > 1 else 0,
            'min': round(min(composites), 1) if composites else 0,
            'max': round(max(composites), 1) if composites else 0,
        },
        'buyback_yield': {
            'mean': round(statistics.mean(yields), 2) if yields else 0,
            'median': round(statistics.median(yields), 2) if yields else 0,
        },
        'pe_ratio': {
            'mean': round(statistics.mean(pe_ratios), 1) if pe_ratios else 0,
            'median': round(statistics.median(pe_ratios), 1) if pe_ratios else 0,
        },
    }

    # Category grouping
    categories = {}
    for s in scored:
        cat = s.get('category', 'Unknown')
        categories.setdefault(cat, []).append(s['protocol'])
    stats['categories'] = categories

    # Verdict distribution
    verdict_counts = {'Bullish': 0, 'Neutral': 0, 'Bearish': 0}
    for s in scored:
        for v in s.get('verdicts', []):
            direction = v.get('verdict', '')
            if direction in verdict_counts:
                verdict_counts[direction] += 1
    stats['verdict_distribution'] = verdict_counts

    return stats


def main():
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / 'data'

    master_path = data_dir / 'master_dataset.json'
    if not master_path.exists():
        print(f"Error: {master_path} not found. Run report_parser.py first.")
        sys.exit(1)

    with open(master_path) as f:
        protocols = json.load(f)

    print(f"Scoring {len(protocols)} protocols...")
    scored = compute_composite(protocols)
    stats = compute_statistics(scored)

    output = {
        'protocols': scored,
        'statistics': stats,
    }

    out_path = data_dir / 'scored_dataset.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2, default=str)
    print(f"Written to {out_path}")

    # Print rankings
    print("\n--- Composite Rankings ---")
    print(f"{'Rank':>4} {'Protocol':20s} {'Composite':>10} {'Yield':>8} "
          f"{'RevQ':>6} {'Supply':>7} {'Consens':>8} {'MechD':>7}")
    print("-" * 80)
    for s in scored:
        print(f"{s['rank']:>4} {s['protocol']:20s} {s['composite_score']:>10.1f} "
              f"{s['buyback_yield_score']:>8.1f} {s['revenue_quality_score']:>6.1f} "
              f"{s['supply_cleanliness_score']:>7.1f} {s['analyst_consensus_score']:>8.1f} "
              f"{s['mechanism_design_score']:>7.1f}")

    print(f"\nStatistics: mean={stats['composite']['mean']}, "
          f"median={stats['composite']['median']}, "
          f"stdev={stats['composite']['stdev']}")
    print(f"Verdict distribution: {stats['verdict_distribution']}")


if __name__ == '__main__':
    main()
