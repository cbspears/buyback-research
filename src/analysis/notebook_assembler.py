#!/usr/bin/env python3
"""Assemble the unified cross-protocol comparison Jupyter notebook.

Reads scored_dataset.json, chart_code.json, persona outputs, and
synthesis text to produce output/unified-cross-protocol-comparison.ipynb.
"""

import json
import sys
from datetime import date
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def load_json(path: Path) -> dict | list | None:
    """Load a JSON file, return None if missing."""
    if not path.exists():
        print(f"  Warning: {path} not found")
        return None
    with open(path) as f:
        return json.load(f)


def build_notebook(project_root: Path) -> nbformat.NotebookNode:
    """Build the complete notebook from all data sources."""
    data_dir = project_root / 'data'
    persona_dir = data_dir / 'persona_outputs'

    # Load data
    scored_data = load_json(data_dir / 'scored_dataset.json')
    chart_code = load_json(data_dir / 'chart_code.json')
    synthesis = load_json(data_dir / 'synthesis.json')

    protocols = scored_data['protocols'] if scored_data else []
    stats = scored_data.get('statistics', {}) if scored_data else {}

    # Load persona outputs
    persona_names = ['charbonneau', 'hasu', 'cobie', 'hayes', 'monegro']
    persona_labels = {
        'charbonneau': 'Jon Charbonneau — Protocol Design Lens',
        'hasu': 'Hasu — Game Theory Lens',
        'cobie': 'Cobie — Market Structure Lens',
        'hayes': 'Arthur Hayes — Macro Cyclical Lens',
        'monegro': 'Joel Monegro — Structural Value Capture Lens',
    }
    persona_data = {}
    for name in persona_names:
        data = load_json(persona_dir / f'{name}.json')
        if data:
            persona_data[name] = data

    nb = new_notebook()
    nb.metadata.kernelspec = {
        'display_name': 'Python 3',
        'language': 'python',
        'name': 'python3',
    }
    cells = []

    # -----------------------------------------------------------------------
    # Cell 1: Title & Executive Summary
    # -----------------------------------------------------------------------
    top_3 = ', '.join(p['protocol'] for p in protocols[:3]) if protocols else 'N/A'
    n_protocols = len(protocols)
    verdict_dist = stats.get('verdict_distribution', {})
    bullish_n = verdict_dist.get('Bullish', 0)
    neutral_n = verdict_dist.get('Neutral', 0)
    bearish_n = verdict_dist.get('Bearish', 0)

    cells.append(new_markdown_cell(
        f"# Unified Cross-Protocol Buyback Comparison\n\n"
        f"**Generated**: {date.today().isoformat()}\n\n"
        f"## Executive Summary\n\n"
        f"This notebook synthesizes buyback analysis across **{n_protocols} protocols** "
        f"with 5 analyst perspectives each, producing composite rankings, visualizations, "
        f"and persona-driven portfolio allocations.\n\n"
        f"**Top 3 by Composite Score**: {top_3}\n\n"
        f"**Aggregate Verdict Distribution**: "
        f"{bullish_n} Bullish / {neutral_n} Neutral / {bearish_n} Bearish "
        f"(across {n_protocols * 5} analyst-protocol assessments)\n\n"
        f"**Median Composite Score**: {stats.get('composite', {}).get('median', 'N/A')}/100"
    ))

    # -----------------------------------------------------------------------
    # Cells 2-3: Imports & Data Loading
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell("## Setup"))

    cells.append(new_code_cell(
        "import json\n"
        "from pathlib import Path\n"
        "import pandas as pd\n"
        "import plotly.graph_objects as go\n"
        "import plotly.express as px\n"
        "from plotly.subplots import make_subplots\n\n"
        "# Load scored dataset (relative to notebook location in output/)\n"
        "data_path = Path('..') / 'data' / 'scored_dataset.json'\n"
        "with open(data_path) as f:\n"
        "    raw = json.load(f)\n\n"
        "protocols = raw['protocols']\n"
        "stats = raw['statistics']\n\n"
        "df = pd.DataFrame(protocols)\n"
        "df = df.sort_values('composite_score', ascending=False).reset_index(drop=True)\n"
        "print(f'Loaded {len(df)} protocols')\n"
        "df[['rank', 'protocol', 'token', 'composite_score', 'buyback_yield', 'pe_ratio']].head(13)"
    ))

    # -----------------------------------------------------------------------
    # Cells 4-5: Master Comparison Table
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Master Comparison Table\n\n"
        "All protocols ranked by composite score across 5 dimensions."
    ))

    if chart_code and 'master_table' in chart_code:
        cells.append(new_code_cell(chart_code['master_table']))
    else:
        cells.append(new_code_cell(_default_master_table()))

    # -----------------------------------------------------------------------
    # Cells 6-7: Composite Rankings (stacked bar)
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Composite Score Breakdown\n\n"
        "Horizontal stacked bars showing the 5-dimension breakdown per protocol."
    ))

    if chart_code and 'composite_ranking' in chart_code:
        cells.append(new_code_cell(chart_code['composite_ranking']))
    else:
        cells.append(new_code_cell(_default_composite_bar()))

    # -----------------------------------------------------------------------
    # Cells 8-9: Yield vs P/E Scatter
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Buyback Yield vs P/E Ratio\n\n"
        "Bubble size = market cap. Color = composite score. "
        "Quadrant lines at medians. Upper-left quadrant (high yield, low P/E) "
        "is the sweet spot."
    ))

    if chart_code and 'yield_pe_scatter' in chart_code:
        cells.append(new_code_cell(chart_code['yield_pe_scatter']))
    else:
        cells.append(new_code_cell(_default_yield_pe_scatter()))

    # -----------------------------------------------------------------------
    # Cells 10-11: Supply Dilution Bars
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Supply Dilution Risk (FDV/MCap)\n\n"
        "Horizontal bars of FDV/MCap ratio. Color-coded by severity. "
        "Reference line at 1.0x (fully diluted = circulating)."
    ))

    if chart_code and 'supply_dilution' in chart_code:
        cells.append(new_code_cell(chart_code['supply_dilution']))
    else:
        cells.append(new_code_cell(_default_supply_dilution()))

    # -----------------------------------------------------------------------
    # Cells 12-13: Mechanism Classification
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Mechanism Classification Matrix\n\n"
        "Buyback mechanism types (burn/hold/stake/distribute) "
        "crossed with execution method (automated/periodic/manual)."
    ))

    if chart_code and 'mechanism_matrix' in chart_code:
        cells.append(new_code_cell(chart_code['mechanism_matrix']))
    else:
        cells.append(new_code_cell(_default_mechanism_matrix()))

    # -----------------------------------------------------------------------
    # Cells 14-15: Analyst Sentiment Heatmap
    # -----------------------------------------------------------------------
    cells.append(new_markdown_cell(
        "## Analyst Sentiment Heatmap\n\n"
        "13x5 grid: Bullish (green) / Neutral (yellow) / Bearish (red). "
        "Confidence levels annotated."
    ))

    if chart_code and 'sentiment_heatmap' in chart_code:
        cells.append(new_code_cell(chart_code['sentiment_heatmap']))
    else:
        cells.append(new_code_cell(_default_sentiment_heatmap()))

    # -----------------------------------------------------------------------
    # Cells 16-26: 5 Persona Sections
    # -----------------------------------------------------------------------
    for persona_name in persona_names:
        label = persona_labels[persona_name]
        pdata = persona_data.get(persona_name, {})

        landscape = pdata.get('landscape_analysis', '_Landscape analysis pending._')
        themes = pdata.get('key_themes', [])
        disagreements = pdata.get('disagreements', [])
        portfolio = pdata.get('portfolio', {})

        themes_md = '\n'.join(f'- {t}' for t in themes) if themes else '_Pending._'
        disagree_md = '\n'.join(f'- {d}' for d in disagreements) if disagreements else '_Pending._'

        # Portfolio table
        portfolio_rows = ''
        if portfolio.get('allocations'):
            portfolio_rows = '| Protocol | Allocation | Rationale |\n|----------|-----------|----------|\n'
            for alloc in portfolio['allocations']:
                portfolio_rows += (
                    f"| {alloc.get('protocol', '')} | "
                    f"${alloc.get('amount', 0):,.0f} ({alloc.get('pct', 0):.1f}%) | "
                    f"{alloc.get('rationale', '')} |\n"
                )
            if portfolio.get('cash'):
                portfolio_rows += (
                    f"| **Cash** | ${portfolio['cash'].get('amount', 0):,.0f} "
                    f"({portfolio['cash'].get('pct', 0):.1f}%) | "
                    f"{portfolio['cash'].get('rationale', '')} |\n"
                )

        cells.append(new_markdown_cell(
            f"## @{persona_name.capitalize()} — {label}\n\n"
            f"### Landscape Analysis\n\n{landscape}\n\n"
            f"### Key Themes\n\n{themes_md}\n\n"
            f"### Expected Disagreements\n\n{disagree_md}\n\n"
            f"### Portfolio Allocation ($1M)\n\n{portfolio_rows if portfolio_rows else '_Pending._'}"
        ))

        # Portfolio donut chart
        if portfolio.get('allocations'):
            cells.append(new_code_cell(
                _persona_donut_chart(persona_name, label)
            ))
        else:
            cells.append(new_code_cell(
                f"# Portfolio chart for @{persona_name} — pending persona agent output\n"
                f"print('No portfolio data available for {persona_name}')"
            ))

    # -----------------------------------------------------------------------
    # Cells 27-28: Senior Research Lead Synthesis
    # -----------------------------------------------------------------------
    synthesis_text = ''
    if synthesis:
        synthesis_text = synthesis.get('text', '_Synthesis pending._')
    else:
        synthesis_text = '_Synthesis pending — run the unified pipeline to generate._'

    cells.append(new_markdown_cell(
        f"## Senior Research Lead — Landscape Synthesis\n\n{synthesis_text}"
    ))

    cells.append(new_markdown_cell(
        f"## Methodology & Data Sources\n\n"
        f"### Scoring Methodology\n\n"
        f"Each protocol is scored across 5 equally-weighted dimensions (0-100 each):\n\n"
        f"1. **Buyback Yield** — Percentile rank within cohort. "
        f"Yields >25% receive a 20% haircut (extreme yields correlate with Bearish consensus).\n"
        f"2. **Revenue Quality** — Revenue denomination (stablecoin=25, mixed=15, native=0), "
        f"P/E percentile (inverse), category diversity, cost basis performance.\n"
        f"3. **Supply Cleanliness** — FDV/MCap ratio (1.0x=30pts, decays to 0 at 4.0x), "
        f"% circulating, unlock-to-buyback dynamics.\n"
        f"4. **Analyst Consensus** — Verdict scoring (Bullish=2, Neutral=1, Bearish=0) "
        f"weighted by confidence (High=1.5x, Medium=1.0x, Low=0.75x), normalized to 0-100.\n"
        f"5. **Mechanism Design** — Token flow (burn=30, distribute=18, stake=15), "
        f"execution (automated=25, periodic=18, manual=10), transparency (on-chain=25, opaque=0).\n\n"
        f"**Composite** = equal-weight average of all 5 dimensions.\n\n"
        f"### Data Sources\n\n"
        f"CoinGecko, CoinMarketCap, DefiLlama, Token Terminal, on-chain data, "
        f"protocol governance forums, and individual protocol documentation.\n\n"
        f"### Generation\n\n"
        f"Generated by the Ralph Buyback Research System on {date.today().isoformat()}. "
        f"Source reports: `output/*-report.md`. "
        f"Regenerable via `./loop.sh unified 1`."
    ))

    nb.cells = cells
    return nb


# ---------------------------------------------------------------------------
# Default chart code (used when chart_code.json is not available)
# ---------------------------------------------------------------------------

def _default_master_table() -> str:
    return '''
cols = ['rank', 'protocol', 'token', 'category', 'buyback_yield', 'pe_ratio',
        'fdv_mcap_ratio', 'composite_score', 'mechanism_types', 'revenue_denomination']
display_df = df[cols].copy()
display_df.columns = ['#', 'Protocol', 'Token', 'Category', 'Yield %', 'P/E',
                       'FDV/MCap', 'Score', 'Mechanism', 'Rev Denom']

fig = go.Figure(data=[go.Table(
    header=dict(
        values=list(display_df.columns),
        fill_color='#1a1a2e',
        font=dict(color='white', size=12),
        align='left',
    ),
    cells=dict(
        values=[display_df[col] for col in display_df.columns],
        fill_color=[['#16213e' if i % 2 == 0 else '#0f3460' for i in range(len(display_df))]],
        font=dict(color='white', size=11),
        align='left',
        height=28,
    ),
)])
fig.update_layout(
    title='Master Protocol Comparison',
    height=max(400, 50 * len(display_df)),
    margin=dict(l=20, r=20, t=50, b=20),
)
fig.show()
'''.strip()


def _default_composite_bar() -> str:
    return '''
dims = ['buyback_yield_score', 'revenue_quality_score', 'supply_cleanliness_score',
        'analyst_consensus_score', 'mechanism_design_score']
dim_labels = ['Buyback Yield', 'Revenue Quality', 'Supply Cleanliness',
              'Analyst Consensus', 'Mechanism Design']
colors = ['#e63946', '#457b9d', '#2a9d8f', '#e9c46a', '#264653']

sorted_df = df.sort_values('composite_score', ascending=True)

fig = go.Figure()
for dim, label, color in zip(dims, dim_labels, colors):
    fig.add_trace(go.Bar(
        y=sorted_df['protocol'],
        x=sorted_df[dim],
        name=label,
        orientation='h',
        marker_color=color,
    ))

fig.update_layout(
    barmode='stack',
    title='Composite Score Breakdown by Protocol',
    xaxis_title='Score (0-500 total across 5 dimensions)',
    height=max(500, 45 * len(df)),
    margin=dict(l=150, r=20, t=50, b=40),
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
)
fig.show()
'''.strip()


def _default_yield_pe_scatter() -> str:
    return '''
scatter_df = df.dropna(subset=['buyback_yield', 'pe_ratio']).copy()
scatter_df = scatter_df[scatter_df['pe_ratio'] < 200]  # exclude extreme P/E

fig = px.scatter(
    scatter_df,
    x='pe_ratio',
    y='buyback_yield',
    size='market_cap',
    color='composite_score',
    text='token',
    color_continuous_scale='RdYlGn',
    size_max=60,
    labels={
        'pe_ratio': 'P/E Ratio',
        'buyback_yield': 'Buyback Yield (%)',
        'composite_score': 'Composite Score',
        'market_cap': 'Market Cap',
    },
)

# Quadrant lines at medians
med_pe = scatter_df['pe_ratio'].median()
med_yield = scatter_df['buyback_yield'].median()
fig.add_hline(y=med_yield, line_dash='dash', line_color='gray', opacity=0.5)
fig.add_vline(x=med_pe, line_dash='dash', line_color='gray', opacity=0.5)

fig.update_traces(textposition='top center', textfont_size=10)
fig.update_layout(
    title='Buyback Yield vs P/E Ratio',
    height=600,
    xaxis_title='P/E Ratio (lower = cheaper)',
    yaxis_title='Buyback Yield % (higher = better)',
)
fig.show()
'''.strip()


def _default_supply_dilution() -> str:
    return '''
dilution_df = df.dropna(subset=['fdv_mcap_ratio']).sort_values('fdv_mcap_ratio')

colors = []
for v in dilution_df['fdv_mcap_ratio']:
    if v <= 1.2:
        colors.append('#2a9d8f')  # green: clean
    elif v <= 2.0:
        colors.append('#e9c46a')  # yellow: moderate
    elif v <= 3.0:
        colors.append('#f4a261')  # orange: concerning
    else:
        colors.append('#e63946')  # red: severe

fig = go.Figure(go.Bar(
    y=dilution_df['protocol'],
    x=dilution_df['fdv_mcap_ratio'],
    orientation='h',
    marker_color=colors,
    text=[f"{v:.2f}x" for v in dilution_df['fdv_mcap_ratio']],
    textposition='outside',
))

fig.add_vline(x=1.0, line_dash='dash', line_color='white', opacity=0.6,
              annotation_text='1.0x (fully diluted = circulating)')

fig.update_layout(
    title='Supply Dilution Risk: FDV / Market Cap',
    xaxis_title='FDV/MCap Ratio',
    height=max(400, 40 * len(dilution_df)),
    margin=dict(l=150, r=80, t=50, b=40),
    plot_bgcolor='#1a1a2e',
    paper_bgcolor='#1a1a2e',
    font=dict(color='white'),
)
fig.show()
'''.strip()


def _default_mechanism_matrix() -> str:
    return '''
# Build mechanism classification data
records = []
for _, row in df.iterrows():
    mechs = row.get('mechanism_types', ['unknown'])
    if isinstance(mechs, str):
        mechs = [mechs]
    primary_mech = mechs[0] if mechs else 'unknown'
    records.append({
        'protocol': row['protocol'],
        'token': row['token'],
        'mechanism': primary_mech.capitalize(),
        'execution': (row.get('execution_type') or 'unknown').capitalize(),
        'composite_score': row['composite_score'],
    })

mech_df = pd.DataFrame(records)

fig = px.scatter(
    mech_df,
    x='mechanism',
    y='execution',
    size='composite_score',
    text='token',
    color='composite_score',
    color_continuous_scale='RdYlGn',
    size_max=40,
    labels={'mechanism': 'Token Flow', 'execution': 'Execution Method'},
)

fig.update_traces(textposition='top center', textfont_size=10)
fig.update_layout(
    title='Mechanism Classification Matrix',
    height=500,
    xaxis_title='Post-Buyback Token Flow',
    yaxis_title='Execution Method',
)
fig.show()
'''.strip()


def _default_sentiment_heatmap() -> str:
    return '''
analyst_names = ['Charbonneau', 'Hasu', 'Cobie', 'Hayes', 'Monegro']
verdict_map = {'Bullish': 2, 'Neutral': 1, 'Bearish': 0}
color_map = {2: '#2a9d8f', 1: '#e9c46a', 0: '#e63946'}

sorted_df = df.sort_values('composite_score', ascending=False)
protocol_names = sorted_df['protocol'].tolist()

z_values = []
annotations = []

for i, (_, row) in enumerate(sorted_df.iterrows()):
    row_vals = []
    verdicts = row.get('verdicts', [])
    verdict_dict = {v['analyst']: v for v in verdicts} if verdicts else {}
    for j, analyst in enumerate(analyst_names):
        v = verdict_dict.get(analyst, {})
        direction = v.get('verdict', 'Neutral')
        confidence = v.get('confidence', '')
        score = verdict_map.get(direction, 1)
        row_vals.append(score)
        # Add annotation text
        short_conf = confidence[:3] if confidence else ''
        annotations.append(dict(
            x=j, y=i,
            text=f"{direction[:1]}\\n{short_conf}",
            showarrow=False,
            font=dict(color='white', size=9),
        ))
    z_values.append(row_vals)

fig = go.Figure(data=go.Heatmap(
    z=z_values,
    x=analyst_names,
    y=protocol_names,
    colorscale=[[0, '#e63946'], [0.5, '#e9c46a'], [1, '#2a9d8f']],
    showscale=False,
    zmin=0, zmax=2,
))

fig.update_layout(
    title='Analyst Sentiment Heatmap (Green=Bullish, Yellow=Neutral, Red=Bearish)',
    annotations=annotations,
    height=max(500, 40 * len(protocol_names)),
    margin=dict(l=150, r=20, t=50, b=40),
    yaxis=dict(autorange='reversed'),
)
fig.show()
'''.strip()


def _persona_donut_chart(persona_name: str, label: str) -> str:
    return f'''
# Portfolio allocation for @{persona_name}
import json
from pathlib import Path

persona_file = Path('..') / 'data' / 'persona_outputs' / '{persona_name}.json'
if persona_file.exists():
    with open(persona_file) as f:
        pdata = json.load(f)
    portfolio = pdata.get('portfolio', {{}})
    allocs = portfolio.get('allocations', [])
    cash = portfolio.get('cash', {{}})

    labels = [a['protocol'] for a in allocs]
    values = [a['amount'] for a in allocs]
    if cash:
        labels.append('Cash')
        values.append(cash.get('amount', 0))

    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values,
        hole=0.45,
        textinfo='label+percent',
        textfont_size=10,
    )])
    fig.update_layout(
        title='@{persona_name.capitalize()} — $1M Portfolio Allocation',
        height=450,
        showlegend=True,
    )
    fig.show()
else:
    print('No portfolio data for {persona_name}')
'''.strip()


def main():
    project_root = Path(__file__).parent.parent.parent
    output_dir = project_root / 'output'
    output_dir.mkdir(exist_ok=True)

    print("Assembling unified comparison notebook...")
    nb = build_notebook(project_root)

    out_path = output_dir / 'unified-cross-protocol-comparison.ipynb'
    with open(out_path, 'w') as f:
        nbformat.write(nb, f)
    print(f"Written to {out_path}")
    print(f"Cells: {len(nb.cells)}")

    # Also generate Obsidian-compatible markdown summary
    _write_obsidian_summary(project_root, nb)


def _write_obsidian_summary(project_root: Path, nb: nbformat.NotebookNode):
    """Write an Obsidian-compatible markdown summary."""
    data_dir = project_root / 'data'
    scored_data = load_json(data_dir / 'scored_dataset.json')
    if not scored_data:
        return

    protocols = scored_data['protocols']
    stats = scored_data.get('statistics', {})

    lines = [
        '---',
        'type: analysis',
        'area: bitcoin-research',
        'topics: [buybacks, cross-protocol, comparison]',
        f'created: {date.today().isoformat()}',
        'status: review',
        '---',
        '',
        '# Unified Cross-Protocol Buyback Comparison',
        '',
        f'> Generated {date.today().isoformat()} — {len(protocols)} protocols analyzed',
        '',
        '## Rankings',
        '',
        '| Rank | Protocol | Token | Score | Yield | P/E | FDV/MCap |',
        '|------|----------|-------|-------|-------|-----|----------|',
    ]

    for p in protocols:
        lines.append(
            f"| {p['rank']} | {p['protocol']} | {p['token']} | "
            f"{p['composite_score']:.1f} | "
            f"{p.get('buyback_yield', 'N/A')}% | "
            f"{p.get('pe_ratio', 'N/A')}x | "
            f"{p.get('fdv_mcap_ratio', 'N/A')}x |"
        )

    lines.extend([
        '',
        '## Composite Score Dimensions',
        '',
        '| Protocol | Yield | RevQ | Supply | Consensus | Mechanism |',
        '|----------|-------|------|--------|-----------|-----------|',
    ])

    for p in protocols:
        lines.append(
            f"| {p['protocol']} | "
            f"{p['buyback_yield_score']:.0f} | "
            f"{p['revenue_quality_score']:.0f} | "
            f"{p['supply_cleanliness_score']:.0f} | "
            f"{p['analyst_consensus_score']:.0f} | "
            f"{p['mechanism_design_score']:.0f} |"
        )

    vd = stats.get('verdict_distribution', {})
    lines.extend([
        '',
        '## Statistics',
        '',
        f"- **Protocols analyzed**: {stats.get('count', 0)}",
        f"- **Composite mean**: {stats.get('composite', {}).get('mean', 'N/A')}",
        f"- **Composite median**: {stats.get('composite', {}).get('median', 'N/A')}",
        f"- **Verdict distribution**: {vd.get('Bullish', 0)}B / "
        f"{vd.get('Neutral', 0)}N / {vd.get('Bearish', 0)}Be",
        '',
        '## Links',
        '',
        '- [[unified-cross-protocol-comparison.ipynb|Full Interactive Notebook]]',
        '- Individual reports: ' + ', '.join(
            f"[[{p['source_file']}|{p['token']}]]" for p in protocols
        ),
        '',
        '---',
        '',
        f'*Generated by Ralph Buyback Research System — {date.today().isoformat()}*',
    ])

    out_path = project_root / 'output' / 'unified-comparison-summary.md'
    with open(out_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Obsidian summary written to {out_path}")


if __name__ == '__main__':
    main()
