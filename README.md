---
type: project
area: bitcoin-research
status: active
created: 2026-02-19
tags: [buybacks, tokenomics, research, multi-agent]
---

# Ralph Buyback Research

Autonomous multi-agent research system analyzing crypto protocol buyback mechanisms. Uses the Ralph Wiggum technique (autonomous looping) with a Project Lead orchestrating 5 analyst persona subagents that model real crypto researchers.

## Analyst Personas

| Persona | Lens | Focus |
|---------|------|-------|
| @Charbonneau | Protocol design | TEV/REV framework, mechanism tradeoffs |
| @Hasu | Game theory | Incentive compatibility, corporate finance |
| @Cobie | Market structure | Exit liquidity, unlock dynamics, political economy |
| @Hayes | Macro cyclical | Liquidity regimes, pro-cyclicality, opportunity cost |
| @Monegro | Structural value | Fat protocols, moats, forkability |

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./loop.sh build 1    # Single iteration test
./loop.sh build 15   # Full overnight run
```

## Architecture

See [[IMPLEMENTATION_PLAN]] for current state and progress tracking.
