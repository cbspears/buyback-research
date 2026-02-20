#!/usr/bin/env python3
"""Automated protocol discovery pipeline.

Identifies protocols with active buyback programs by:
1. Pulling DefiLlama holdersRevenue data
2. Comparing against the protocol registry
3. Querying Snapshot for governance proposals mentioning buybacks
4. Outputting new candidates with basic metrics
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from collectors.defillama import get_holders_revenue_all
from collectors.snapshot_gov import search_global


def load_registry() -> set:
    """Load known protocols from specs/protocols.md."""
    registry_path = Path(__file__).parent.parent.parent / "specs" / "protocols.md"
    known = set()

    if not registry_path.exists():
        return known

    content = registry_path.read_text()
    # Extract protocol names from table rows (first column after |)
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("|") and not line.startswith("| Protocol") and not line.startswith("| #") and not line.startswith("|---"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2 and parts[1] and not parts[1].startswith("("):
                known.add(parts[1].lower())

    return known


def discover_from_defillama() -> list:
    """Find protocols with holdersRevenue not in our registry."""
    print("Scanning DefiLlama for protocols with holders revenue...")
    protocols = get_holders_revenue_all()

    known = load_registry()
    new_protocols = []

    for p in protocols:
        name = (p.get("name") or "").lower()
        slug = (p.get("slug") or "").lower()

        # Check if already known
        if name in known or slug in known:
            continue

        # Check if any known name is a substring
        is_known = False
        for k in known:
            if k in name or name in k or k in slug or slug in k:
                is_known = True
                break

        if not is_known:
            new_protocols.append(p)

    return new_protocols


def discover_from_governance() -> list:
    """Find protocols discussing buybacks via Snapshot governance."""
    print("Scanning Snapshot.org for buyback governance proposals...")
    results = search_global()

    known = load_registry()
    new_spaces = []
    seen_spaces = set()

    for r in results:
        space = (r.get("space") or "").lower()
        space_name = (r.get("space_name") or "").lower()

        if space in seen_spaces:
            continue
        seen_spaces.add(space)

        # Check if already known
        is_known = False
        for k in known:
            if k in space or k in space_name or space in k or space_name in k:
                is_known = True
                break

        if not is_known and space:
            new_spaces.append({
                "space": r.get("space"),
                "space_name": r.get("space_name"),
                "sample_proposal": r.get("title"),
                "keyword": r.get("keyword"),
                "votes": r.get("votes"),
            })

    return new_spaces


def run_discovery() -> dict:
    """Run full discovery pipeline."""
    print("=" * 60)
    print("Protocol Discovery Pipeline")
    print("=" * 60)

    known = load_registry()
    print(f"Known protocols in registry: {len(known)}")

    # DefiLlama discovery
    defillama_new = discover_from_defillama()
    print(f"New protocols from DefiLlama (holdersRevenue): {len(defillama_new)}")

    # Snapshot governance discovery
    governance_new = discover_from_governance()
    print(f"New protocols from Snapshot governance: {len(governance_new)}")

    result = {
        "source": "discovery_pipeline",
        "collected_at": datetime.utcnow().isoformat(),
        "known_protocols": len(known),
        "new_from_defillama": defillama_new,
        "new_from_defillama_count": len(defillama_new),
        "new_from_governance": governance_new,
        "new_from_governance_count": len(governance_new),
        "summary": {
            "total_new_candidates": len(defillama_new) + len(governance_new),
            "recommendation": "Review candidates and add promising ones to specs/protocols.md",
        },
    }

    return result


def main():
    result = run_discovery()

    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    out_path = data_dir / "discovery_results.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\nResults written to {out_path}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("Discovery Summary")
    print(f"{'=' * 60}")
    print(f"Known protocols: {result['known_protocols']}")
    print(f"New from DefiLlama: {result['new_from_defillama_count']}")
    print(f"New from Governance: {result['new_from_governance_count']}")

    if result["new_from_defillama"]:
        print("\nTop new DefiLlama protocols:")
        for p in result["new_from_defillama"][:10]:
            rev = p.get("holders_revenue_24h", 0)
            print(f"  - {p.get('name')} ({p.get('category')}): ${rev:,.0f}/day holders revenue")

    if result["new_from_governance"]:
        print("\nGovernance buyback proposals found:")
        for g in result["new_from_governance"][:10]:
            print(f"  - {g.get('space_name')} ({g.get('space')}): \"{g.get('sample_proposal')}\"")

    # Output JSON to stdout for subagent consumption
    print("\n---JSON_OUTPUT_START---")
    print(json.dumps(result, indent=2, default=str))
    print("---JSON_OUTPUT_END---")


if __name__ == "__main__":
    main()
