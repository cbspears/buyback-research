#!/usr/bin/env python3
"""Cross-protocol comparison tables and rankings."""

import json
import sys
from pathlib import Path

from .buyback_metrics import load_protocol_data, calculate_metrics


def load_all_metrics() -> dict:
    """Load and calculate metrics for all protocols with data."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    protocols = set()

    # Find all protocols with DefiLlama data
    for f in data_dir.glob("*_defillama.json"):
        name = f.stem.replace("_defillama", "")
        protocols.add(name)

    all_metrics = {}
    for protocol in sorted(protocols):
        data = load_protocol_data(protocol)
        if data:
            metrics = calculate_metrics(data)
            metrics["protocol"] = protocol
            all_metrics[protocol] = metrics

    return all_metrics


def rank_by_buyback_yield(metrics: dict) -> list:
    """Rank protocols by buyback yield."""
    items = []
    for name, m in metrics.items():
        yield_pct = m.get("buyback_yield_pct")
        if yield_pct is not None:
            items.append({"protocol": name, "buyback_yield_pct": yield_pct, **m})
    return sorted(items, key=lambda x: x["buyback_yield_pct"], reverse=True)


def rank_by_pe(metrics: dict) -> list:
    """Rank protocols by P/E ratio (lower = cheaper)."""
    items = []
    for name, m in metrics.items():
        pe = m.get("pe_ratio")
        if pe is not None and pe > 0:
            items.append({"protocol": name, "pe_ratio": pe, **m})
    return sorted(items, key=lambda x: x["pe_ratio"])


def generate_comparison_table(metrics: dict) -> str:
    """Generate markdown comparison table."""
    lines = ["# Buyback Protocol Comparison\n"]
    lines.append("| Protocol | MCap | Revenue | Buyback Yield | P/E | FDV/MCap | Holders Share |")
    lines.append("|----------|------|---------|---------------|-----|----------|---------------|")

    def fmt_m(val):
        if val is None:
            return "N/A"
        if val >= 1e9:
            return f"${val/1e9:.1f}B"
        if val >= 1e6:
            return f"${val/1e6:.0f}M"
        return f"${val:,.0f}"

    sorted_protocols = sorted(
        metrics.items(),
        key=lambda x: x[1].get("buyback_yield_pct") or 0,
        reverse=True,
    )

    for name, m in sorted_protocols:
        mcap = fmt_m(m.get("market_cap"))
        rev = fmt_m(m.get("annual_revenue_est"))
        byield = f"{m.get('buyback_yield_pct', 'N/A')}%"
        pe = f"{m.get('pe_ratio', 'N/A')}x"
        fdv_mcap = f"{m.get('fdv_mcap_ratio', 'N/A')}x"
        holders = f"{m.get('holders_fee_share_pct', 'N/A')}%"
        lines.append(f"| {name} | {mcap} | {rev} | {byield} | {pe} | {fdv_mcap} | {holders} |")

    return "\n".join(lines)


def main():
    metrics = load_all_metrics()

    if not metrics:
        print("No protocol data found. Run collectors first.")
        sys.exit(1)

    table = generate_comparison_table(metrics)
    print(table)

    # Save comparison
    data_dir = Path(__file__).parent.parent.parent / "data"
    out_path = data_dir / "comparison_table.md"
    with open(out_path, "w") as f:
        f.write(table)

    print(f"\nComparison table written to {out_path}")

    # JSON output
    out_json = data_dir / "comparison_metrics.json"
    with open(out_json, "w") as f:
        json.dump(metrics, f, indent=2, default=str)
    print(f"Full metrics written to {out_json}")


if __name__ == "__main__":
    main()
