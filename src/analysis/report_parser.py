#!/usr/bin/env python3
"""Parse all output/*.md buyback reports into structured JSON.

Extracts YAML frontmatter, key metrics tables, analyst verdicts,
mechanism classification, revenue denomination, and one-line summaries
from each report. Outputs data/master_dataset.json.
"""

import json
import re
import sys
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Numeric helpers
# ---------------------------------------------------------------------------

def clean_numeric(raw: str) -> float | None:
    """Strip formatting from a numeric string and return a float.

    Handles: $, %, x, ~, commas, B/M/K suffixes, ranges (take midpoint).
    Returns None if unparseable.
    """
    if not raw or raw.strip().lower() in ("n/a", "—", "-", "undisclosed", "unknown"):
        return None

    s = raw.strip()

    # Handle ranges like "4.5-15.0" or "$0.053-0.056" or "~$400-700K"
    range_match = re.match(
        r"^[~$]*\s*([\d,.]+)\s*[-–to]+\s*[~$]*([\d,.]+)\s*([BMKx%]?)$",
        s, re.IGNORECASE,
    )
    if range_match:
        lo = _parse_single(range_match.group(1) + range_match.group(3))
        hi = _parse_single(range_match.group(2) + range_match.group(3))
        if lo is not None and hi is not None:
            return (lo + hi) / 2
        # Fall through to single parse

    return _parse_single(s)


def _parse_single(s: str) -> float | None:
    """Parse a single numeric value after stripping symbols."""
    s = s.strip()
    # Remove leading symbols
    s = re.sub(r'^[~$≈]+', '', s)
    # Remove trailing description in parens: "$25M+ (Q4 ARR: $30M)" → "$25M+"
    s = re.sub(r'\s*\(.*\)', '', s)
    # Remove trailing text after number+suffix: "~$6.25M (at $25M rev)" handled above
    s = s.strip()

    # Detect and remove suffix
    suffix = 1.0
    if s.upper().endswith('B'):
        suffix = 1e9
        s = s[:-1]
    elif s.upper().endswith('M'):
        suffix = 1e6
        s = s[:-1]
    elif s.upper().endswith('K'):
        suffix = 1e3
        s = s[:-1]

    # Remove %, x suffixes
    s = re.sub(r'[%x]+$', '', s, flags=re.IGNORECASE)
    # Remove plus signs
    s = s.replace('+', '')
    # Remove commas
    s = s.replace(',', '')
    # Remove remaining non-numeric except . and -
    s = s.strip()

    if not s:
        return None

    try:
        return float(s) * suffix
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

def extract_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter between --- delimiters."""
    match = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    try:
        fm = yaml.safe_load(match.group(1))
        return fm if isinstance(fm, dict) else {}
    except yaml.YAMLError:
        return {}


def extract_one_liner(text: str) -> str | None:
    """Extract the blockquote one-line summary after the H1 title."""
    match = re.search(
        r'^#\s+.+?\n\s*\n>\s*\*\*One-line summary\*\*:\s*(.+?)(?:\n\n|\Z)',
        text, re.MULTILINE | re.DOTALL,
    )
    if match:
        summary = match.group(1).strip()
        # Collapse multi-line blockquote
        summary = re.sub(r'\n>\s*', ' ', summary)
        return summary
    # Fallback: any blockquote right after H1
    match = re.search(r'^#\s+.+?\n\s*\n>\s*(.+?)(?:\n\n|\Z)', text, re.MULTILINE | re.DOTALL)
    if match:
        return re.sub(r'\n>\s*', ' ', match.group(1).strip())
    return None


def extract_table(text: str, header_pattern: str) -> list[dict]:
    """Extract a markdown table following a heading matching header_pattern.

    Returns list of {col_name: value} dicts.
    """
    # Find the section header
    header_re = re.compile(
        r'^#{1,3}\s+' + header_pattern + r'\s*$',
        re.MULTILINE | re.IGNORECASE,
    )
    hdr_match = header_re.search(text)
    if not hdr_match:
        return []

    rest = text[hdr_match.end():]

    # Find table lines
    lines = []
    in_table = False
    for line in rest.split('\n'):
        stripped = line.strip()
        if stripped.startswith('|') and '|' in stripped[1:]:
            in_table = True
            lines.append(stripped)
        elif in_table:
            break

    if len(lines) < 3:  # header + separator + at least one row
        return []

    # Parse header
    cols = [c.strip() for c in lines[0].split('|')[1:-1]]
    rows = []
    for line in lines[2:]:  # skip separator
        vals = [c.strip() for c in line.split('|')[1:-1]]
        if len(vals) == len(cols):
            rows.append(dict(zip(cols, vals)))

    return rows


def extract_key_metrics(text: str) -> dict:
    """Extract the Key Metrics table as a flat dict."""
    rows = extract_table(text, r'Key Metrics')
    result = {}
    for row in rows:
        metric = row.get('Metric', '')
        value = row.get('Value', '')
        if metric and value:
            result[metric] = value
    return result


def extract_verdict_table(text: str) -> list[dict]:
    """Extract the Analyst Verdict Summary table."""
    rows = extract_table(text, r'Analyst Verdict Summary')
    verdicts = []
    for row in rows:
        analyst = row.get('Analyst', '').strip().lstrip('@')
        verdict_raw = row.get('Verdict', '').strip()
        confidence = row.get('Confidence', '').strip()

        # Parse primary verdict direction
        primary = _extract_primary_verdict(verdict_raw)

        verdicts.append({
            'analyst': analyst,
            'verdict': primary,
            'verdict_raw': verdict_raw,
            'confidence': confidence,
        })
    return verdicts


def _extract_primary_verdict(verdict_str: str) -> str:
    """Extract the primary verdict direction from potentially compound verdicts.

    E.g. "Bullish on mechanism design, Neutral on token at current FDV"
         → "Bullish" (first directional match)
    """
    verdict_str = verdict_str.strip()
    # Direct match first
    for direction in ('Bullish', 'Neutral', 'Bearish'):
        if verdict_str.startswith(direction):
            return direction
    # Search for first occurrence
    for direction in ('Bullish', 'Neutral', 'Bearish'):
        if direction.lower() in verdict_str.lower():
            return direction
    return verdict_str


def extract_verdicts_from_sections(text: str) -> list[dict]:
    """Fallback: extract verdicts from **Verdict**: lines in analyst sections."""
    pattern = re.compile(
        r'###\s+@(\w+)\s.*?\n'
        r'.*?'
        r'\*\*Verdict\*\*:?\s*(.+?)$',
        re.MULTILINE | re.DOTALL,
    )
    verdicts = []
    # Non-greedy: find each analyst section
    sections = re.split(r'(?=###\s+@)', text)
    for section in sections:
        match = re.search(
            r'###\s+@(\w+)\s', section
        )
        if not match:
            continue
        analyst = match.group(1)

        verdict_match = re.search(
            r'\*\*Verdict\*\*:?\s*(.+?)$', section, re.MULTILINE
        )
        if not verdict_match:
            continue

        line = verdict_match.group(1).strip()
        # Parse "Bullish — Confidence: High" or "Neutral | Confidence: Medium"
        parts = re.split(r'[—|]', line)
        verdict_raw = parts[0].strip()
        confidence = ''
        for part in parts[1:]:
            if 'confidence' in part.lower():
                confidence = re.sub(r'(?i)confidence:?\s*', '', part).strip()

        verdicts.append({
            'analyst': analyst,
            'verdict': _extract_primary_verdict(verdict_raw),
            'verdict_raw': verdict_raw,
            'confidence': confidence,
        })

    return verdicts


# ---------------------------------------------------------------------------
# Mechanism & revenue classification
# ---------------------------------------------------------------------------

MECHANISM_KEYWORDS = {
    'burn': ['burn', 'burned', 'burning', 'buy-and-burn', 'buyback-and-burn',
             'permanently burned', 'deflationary', 'supply reduction'],
    'lock': ['lock', 'locked', 'one-sided LP', 'LP lock', 'permanently locked'],
    'stake': ['stake', 'staking', 'staked', 'distribute to stakers',
              'staking rewards', 'stSYRUP'],
    'distribute': ['distribute', 'distribution', 'revenue sharing',
                   'fee sharing', 'holders revenue'],
    'hold': ['hold', 'held', 'treasury hold', 'strategic fund', 'SSF',
             'accumulate', 'reserve', 'Chainlink Reserve'],
}

REVENUE_KEYWORDS = {
    'stablecoin': ['USDC', 'USDT', 'stablecoin', 'stablecoin-denominated',
                   'USD-denominated'],
    'native': ['native token', 'own token', 'RAY', 'HYPE-denominated',
               'token-denominated'],
    'eth': ['WETH', 'ETH-denominated', 'ETH'],
    'mixed': ['mixed', 'paired assets', 'SOL, USDC', 'multiple assets'],
}


def classify_mechanism(text: str) -> list[str]:
    """Classify buyback mechanism type(s) from report text."""
    # Focus on the Buyback Mechanism section
    mech_section = _extract_section(text, 'Buyback Mechanism')
    search_text = mech_section if mech_section else text

    found = []
    for mtype, keywords in MECHANISM_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in search_text.lower():
                if mtype not in found:
                    found.append(mtype)
                break

    return found if found else ['unknown']


def classify_revenue_denomination(text: str) -> str:
    """Classify revenue denomination from report text."""
    rev_section = _extract_section(text, 'Revenue Model')
    search_text = rev_section if rev_section else text

    scores = {'stablecoin': 0, 'native': 0, 'eth': 0, 'mixed': 0}
    for dtype, keywords in REVENUE_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in search_text.lower():
                scores[dtype] += 1

    # ETH counts as stablecoin-adjacent (hard asset)
    if scores['eth'] > 0 and scores['stablecoin'] == 0:
        scores['stablecoin'] += scores['eth']

    if scores['stablecoin'] > 0 and scores['native'] > 0:
        return 'mixed'
    if scores['stablecoin'] > 0 or scores['eth'] > 0:
        return 'stablecoin'
    if scores['native'] > 0:
        return 'native'
    if scores['mixed'] > 0:
        return 'mixed'
    return 'unknown'


def classify_execution(text: str) -> str:
    """Classify buyback execution type."""
    mech_section = _extract_section(text, 'Buyback Mechanism')
    search_text = (mech_section or text).lower()

    if any(kw in search_text for kw in ['automated', 'programmatic', 'smart contract',
                                          'continuous', 'automatic']):
        return 'automated'
    if any(kw in search_text for kw in ['manual', 'discretionary']):
        return 'manual'
    if any(kw in search_text for kw in ['semi', 'periodic', 'quarterly', 'monthly']):
        return 'periodic'
    return 'unknown'


def classify_transparency(text: str) -> str:
    """Classify buyback transparency level."""
    mech_section = _extract_section(text, 'Buyback Mechanism')
    search_text = (mech_section or text).lower()

    if any(kw in search_text for kw in ['on-chain verifiable', 'on-chain',
                                          'verifiable', 'explorer', 'solscan']):
        return 'on-chain verifiable'
    if any(kw in search_text for kw in ['dashboard', 'tracker', 'disclosed']):
        return 'dashboard'
    return 'opaque'


def _extract_section(text: str, heading: str) -> str | None:
    """Extract text between a heading and the next same-level heading."""
    pattern = re.compile(
        r'^##\s+' + re.escape(heading) + r'\s*\n(.*?)(?=^##\s|\Z)',
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


# ---------------------------------------------------------------------------
# Supply dynamics extraction
# ---------------------------------------------------------------------------

def extract_supply_dynamics(text: str) -> dict:
    """Extract supply-related fields from the Supply Dynamics section."""
    rows = extract_table(text, r'(?:Supply Dynamics|Metric)')
    # The supply dynamics table sometimes has the same Metric/Value structure
    # as Key Metrics, so look specifically in the Supply Dynamics section
    section = _extract_section(text, 'Supply Dynamics')
    if section:
        # Re-parse tables within this section only
        lines = []
        in_table = False
        for line in section.split('\n'):
            stripped = line.strip()
            if stripped.startswith('|') and '|' in stripped[1:]:
                in_table = True
                lines.append(stripped)
            elif in_table:
                break

        if len(lines) >= 3:
            cols = [c.strip() for c in lines[0].split('|')[1:-1]]
            rows = []
            for line in lines[2:]:
                vals = [c.strip() for c in line.split('|')[1:-1]]
                if len(vals) == len(cols):
                    rows.append(dict(zip(cols, vals)))

    result = {}
    for row in rows:
        metric = row.get('Metric', '')
        value = row.get('Value', '')
        metric_lower = metric.lower()

        if 'circulating' in metric_lower:
            # Extract percentage if present
            pct_match = re.search(r'([\d.]+)%', value)
            if pct_match:
                result['pct_circulating'] = float(pct_match.group(1))
        elif 'fdv/mcap' in metric_lower or 'fdv / mcap' in metric_lower:
            result['fdv_mcap_ratio'] = clean_numeric(value)
        elif 'inflation' in metric_lower and 'net' not in metric_lower:
            result['annual_inflation'] = value
        elif 'net' in metric_lower and ('inflation' in metric_lower or 'emission' in metric_lower):
            result['net_inflation'] = value
        elif 'unlock' in metric_lower or 'insider' in metric_lower:
            result['unlock_status'] = value

    return result


# ---------------------------------------------------------------------------
# Main parsing pipeline
# ---------------------------------------------------------------------------

def parse_report(filepath: Path) -> dict | None:
    """Parse a single report file into a structured dict."""
    text = filepath.read_text(encoding='utf-8')

    # Frontmatter
    fm = extract_frontmatter(text)
    if not fm.get('protocol'):
        return None

    # One-liner
    one_liner = extract_one_liner(text)

    # Key Metrics
    metrics_raw = extract_key_metrics(text)

    # Parse key numeric metrics
    market_cap = clean_numeric(metrics_raw.get('Market Cap', ''))
    fdv = clean_numeric(metrics_raw.get('FDV', ''))

    # FDV/MCap from table, fallback to compute
    fdv_mcap_raw = metrics_raw.get('FDV/MCap', '')
    fdv_mcap = clean_numeric(fdv_mcap_raw)
    if fdv_mcap is None and market_cap and fdv and market_cap > 0:
        fdv_mcap = fdv / market_cap

    # Revenue — look for various keys
    annual_rev = None
    for key in ('Annual Revenue', 'Annualized Revenue', 'Annual Revenue (est)',
                'Annual Revenue (on-chain)', 'Cumulative Revenue'):
        if key in metrics_raw:
            annual_rev = clean_numeric(metrics_raw[key])
            if annual_rev is not None:
                break

    # Buyback allocation
    buyback_alloc_raw = metrics_raw.get('Buyback Allocation', '')
    buyback_alloc = clean_numeric(buyback_alloc_raw)

    # Annual buyback
    annual_buyback = None
    for key in ('Annual Buyback', 'Annual Buyback (est)', 'Annual Buyback (run-rate)',
                'Annual Reserve Accumulation (est)'):
        if key in metrics_raw:
            annual_buyback = clean_numeric(metrics_raw[key])
            if annual_buyback is not None:
                break

    # Buyback yield — prefer frontmatter, fallback to table
    buyback_yield = fm.get('buyback_yield')
    if buyback_yield is not None:
        # Handle string values with % suffix
        buyback_yield = clean_numeric(str(buyback_yield))
    if buyback_yield is None:
        buyback_yield = clean_numeric(metrics_raw.get('Buyback Yield', ''))

    # P/E ratio — prefer frontmatter
    pe_ratio = fm.get('pe_ratio')
    if pe_ratio is not None:
        pe_ratio = clean_numeric(str(pe_ratio))
    if pe_ratio is None:
        pe_ratio = clean_numeric(metrics_raw.get('P/E Ratio', ''))

    # Price vs ATH
    price_vs_ath = clean_numeric(metrics_raw.get('Price vs ATH', ''))
    # If the table has a combined string like "-65.5% ($0.228 vs $0.66 ATH)"
    ath_match = re.search(r'(-?[\d.]+)%', metrics_raw.get('Price vs ATH', ''))
    if ath_match:
        price_vs_ath = float(ath_match.group(1))

    # Verdicts — primary: table, fallback: section parsing
    verdicts = extract_verdict_table(text)
    if not verdicts:
        verdicts = extract_verdicts_from_sections(text)

    # Classifications
    mechanism_types = classify_mechanism(text)
    revenue_denom = classify_revenue_denomination(text)
    execution_type = classify_execution(text)
    transparency = classify_transparency(text)

    # Supply dynamics
    supply_info = extract_supply_dynamics(text)

    return {
        'protocol': fm.get('protocol', ''),
        'token': fm.get('token', ''),
        'category': fm.get('category', ''),
        'created': str(fm.get('created', '')),
        'source_file': filepath.name,

        # Quantitative metrics
        'market_cap': market_cap,
        'fdv': fdv,
        'fdv_mcap_ratio': fdv_mcap,
        'annual_revenue': annual_rev,
        'buyback_allocation_pct': buyback_alloc,
        'annual_buyback': annual_buyback,
        'buyback_yield': buyback_yield,
        'pe_ratio': pe_ratio,
        'price_vs_ath_pct': price_vs_ath,

        # Supply
        'pct_circulating': supply_info.get('pct_circulating'),
        'unlock_status': supply_info.get('unlock_status'),
        'annual_inflation': supply_info.get('annual_inflation'),
        'net_inflation': supply_info.get('net_inflation'),

        # Classifications
        'mechanism_types': mechanism_types,
        'revenue_denomination': revenue_denom,
        'execution_type': execution_type,
        'transparency': transparency,

        # Analyst verdicts
        'verdicts': verdicts,

        # Narrative
        'one_liner': one_liner,

        # Raw metrics for reference
        'raw_metrics': metrics_raw,
    }


def parse_all_reports(output_dir: Path | None = None) -> list[dict]:
    """Parse all *-report.md files in the output directory."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent.parent / 'output'

    reports = []
    for filepath in sorted(output_dir.glob('*-report.md')):
        parsed = parse_report(filepath)
        if parsed:
            reports.append(parsed)
            print(f"  Parsed: {filepath.name} → {parsed['protocol']} ({parsed['token']})")
        else:
            print(f"  SKIP: {filepath.name} (no protocol in frontmatter)")

    return reports


def main():
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'output'
    data_dir = project_root / 'data'
    data_dir.mkdir(exist_ok=True)

    print(f"Parsing reports from {output_dir}...")
    reports = parse_all_reports(output_dir)
    print(f"\nParsed {len(reports)} reports.")

    out_path = data_dir / 'master_dataset.json'
    with open(out_path, 'w') as f:
        json.dump(reports, f, indent=2, default=str)
    print(f"Written to {out_path}")

    # Summary
    print("\n--- Summary ---")
    for r in reports:
        verdict_str = ', '.join(
            f"{v['analyst']}={v['verdict']}" for v in r.get('verdicts', [])
        )
        print(f"  {r['protocol']:20s} | {r['token']:8s} | "
              f"Yield={r['buyback_yield']}% | P/E={r['pe_ratio']}x | "
              f"Mechanism={r['mechanism_types']} | {verdict_str}")


if __name__ == '__main__':
    main()
