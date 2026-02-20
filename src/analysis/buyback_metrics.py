#!/usr/bin/env python3
"""Buyback metrics calculator — yield, P/E, revenue sustainability."""

import json
import sys
from pathlib import Path


def load_protocol_data(protocol: str) -> dict:
    """Load all collected data for a protocol."""
    data_dir = Path(__file__).parent.parent.parent / "data"
    combined = {}

    for suffix in ["defillama", "coingecko", "onchain", "snapshot"]:
        path = data_dir / f"{protocol}_{suffix}.json"
        if path.exists():
            with open(path) as f:
                combined[suffix] = json.load(f)

    return combined


def calculate_metrics(data: dict) -> dict:
    """Calculate buyback-specific metrics from collected data."""
    metrics = {}

    # Extract key values
    dl = data.get("defillama", {})
    cg = data.get("coingecko", {})

    # Market data
    market = cg.get("market_data", {})
    mcap = market.get("market_cap")
    fdv = market.get("fully_diluted_valuation")
    price = market.get("price_usd")
    circ_supply = market.get("circulating_supply")
    total_supply = market.get("total_supply")

    # Revenue data
    estimates = dl.get("estimates", {})
    annual_revenue = estimates.get("annual_revenue")
    annual_holders_revenue = estimates.get("annual_holders_revenue")

    revenue = dl.get("revenue", {})
    daily_fees = revenue.get("daily_fees")
    daily_revenue = revenue.get("daily_revenue")
    daily_holders = revenue.get("daily_holders_revenue")

    # Core metrics
    metrics["market_cap"] = mcap
    metrics["fdv"] = fdv
    metrics["price_usd"] = price
    metrics["circulating_supply"] = circ_supply
    metrics["total_supply"] = total_supply

    # Supply metrics
    if circ_supply and total_supply:
        metrics["pct_circulating"] = round(circ_supply / total_supply * 100, 2)
        metrics["dilution_remaining_pct"] = round((total_supply - circ_supply) / total_supply * 100, 2)

    if fdv and mcap:
        metrics["fdv_mcap_ratio"] = round(fdv / mcap, 2)

    # Revenue metrics
    metrics["daily_fees"] = daily_fees
    metrics["daily_revenue"] = daily_revenue
    metrics["daily_holders_revenue"] = daily_holders
    metrics["annual_revenue_est"] = annual_revenue
    metrics["annual_holders_revenue_est"] = annual_holders_revenue

    # Buyback yield = annual buyback $ / market cap
    if annual_holders_revenue and mcap:
        metrics["buyback_yield_pct"] = round(annual_holders_revenue / mcap * 100, 2)

    # P/E ratio = market cap / annual revenue
    if mcap and annual_revenue and annual_revenue > 0:
        metrics["pe_ratio"] = round(mcap / annual_revenue, 2)

    # FDV P/E = FDV / annual revenue
    if fdv and annual_revenue and annual_revenue > 0:
        metrics["fdv_pe_ratio"] = round(fdv / annual_revenue, 2)

    # Revenue per token
    if annual_revenue and circ_supply and circ_supply > 0:
        metrics["revenue_per_token"] = round(annual_revenue / circ_supply, 4)

    # Buyback per token
    if annual_holders_revenue and circ_supply and circ_supply > 0:
        metrics["buyback_per_token"] = round(annual_holders_revenue / circ_supply, 4)

    # Daily volume context
    volume_24h = market.get("total_volume_24h")
    if volume_24h and daily_holders:
        metrics["buyback_to_volume_ratio"] = round(daily_holders / volume_24h * 100, 4)

    # Revenue allocation rate (how much of fees go to holders)
    if daily_fees and daily_holders and daily_fees > 0:
        metrics["holders_fee_share_pct"] = round(daily_holders / daily_fees * 100, 2)

    return metrics


def format_metrics_table(metrics: dict, protocol: str) -> str:
    """Format metrics as a markdown table for reports."""
    lines = [f"## {protocol} — Key Buyback Metrics\n"]
    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")

    def fmt(val, prefix="", suffix="", decimals=2):
        if val is None:
            return "N/A"
        if isinstance(val, float):
            if abs(val) >= 1e9:
                return f"{prefix}{val/1e9:.{decimals}f}B{suffix}"
            if abs(val) >= 1e6:
                return f"{prefix}{val/1e6:.{decimals}f}M{suffix}"
            if abs(val) >= 1e3:
                return f"{prefix}{val/1e3:.{decimals}f}K{suffix}"
            return f"{prefix}{val:.{decimals}f}{suffix}"
        return f"{prefix}{val}{suffix}"

    lines.append(f"| Market Cap | {fmt(metrics.get('market_cap'), '$')} |")
    lines.append(f"| FDV | {fmt(metrics.get('fdv'), '$')} |")
    lines.append(f"| FDV/MCap Ratio | {fmt(metrics.get('fdv_mcap_ratio'), suffix='x')} |")
    lines.append(f"| Price | {fmt(metrics.get('price_usd'), '$', decimals=4)} |")
    lines.append(f"| % Circulating | {fmt(metrics.get('pct_circulating'), suffix='%')} |")
    lines.append(f"| Annual Revenue (est) | {fmt(metrics.get('annual_revenue_est'), '$')} |")
    lines.append(f"| Annual Buyback (est) | {fmt(metrics.get('annual_holders_revenue_est'), '$')} |")
    lines.append(f"| Buyback Yield | {fmt(metrics.get('buyback_yield_pct'), suffix='%')} |")
    lines.append(f"| P/E Ratio | {fmt(metrics.get('pe_ratio'), suffix='x')} |")
    lines.append(f"| FDV P/E | {fmt(metrics.get('fdv_pe_ratio'), suffix='x')} |")
    lines.append(f"| Revenue/Token | {fmt(metrics.get('revenue_per_token'), '$', decimals=4)} |")
    lines.append(f"| Holders Fee Share | {fmt(metrics.get('holders_fee_share_pct'), suffix='%')} |")
    lines.append(f"| Buyback/Volume Ratio | {fmt(metrics.get('buyback_to_volume_ratio'), suffix='%', decimals=4)} |")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python buyback_metrics.py <protocol_name>")
        sys.exit(1)

    protocol = sys.argv[1]
    data = load_protocol_data(protocol)

    if not data:
        print(f"No data found for {protocol}. Run collectors first.")
        sys.exit(1)

    metrics = calculate_metrics(data)

    # Output
    data_dir = Path(__file__).parent.parent.parent / "data"
    out_path = data_dir / f"{protocol}_metrics.json"
    with open(out_path, "w") as f:
        json.dump(metrics, f, indent=2, default=str)

    print(format_metrics_table(metrics, protocol))
    print(f"\nMetrics written to {out_path}")

    # JSON output for subagent consumption
    print("\n---JSON_OUTPUT_START---")
    print(json.dumps(metrics, indent=2, default=str))
    print("---JSON_OUTPUT_END---")


if __name__ == "__main__":
    main()
