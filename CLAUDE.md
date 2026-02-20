# Ralph Buyback Research

Multi-agent crypto buyback research system. Project Lead orchestrates Discovery, Data Collection, and 5 Analyst Persona subagents.

## Project Structure
- `specs/` — Research specifications and analyst persona prompts
- `src/` — Python data collection and analysis tooling
- `data/` — Raw collected data (gitignored)
- `output/` — Final Obsidian-compatible research reports
- `logs/` — Loop execution logs (gitignored)

## Key Files
- `IMPLEMENTATION_PLAN.md` — Persistent state between loop iterations
- `PROMPT_build.md` — Main orchestrator prompt (build mode)
- `PROMPT_plan.md` — Planning/gap analysis prompt
- `specs/protocols.md` — Protocol registry
- `specs/personas/*.md` — Analyst persona system prompts

## Conventions
- Python 3.11+, venv at `./venv`
- All collectors output JSON to `data/`
- Reports use Obsidian frontmatter (type, area, topics, status)
- One protocol per report, one report per loop iteration
- Git commit after each completed report
- Commit format: `research({protocol}): add buyback analysis report`

## Running
```bash
source venv/bin/activate
./loop.sh build 15   # 15 iterations
./loop.sh plan 1     # planning mode
```
