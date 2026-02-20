#!/usr/bin/env python3
"""Snapshot.org governance proposal scanner — finds buyback/fee-switch proposals."""

import json
import sys
from datetime import datetime
from pathlib import Path

import requests

SNAPSHOT_GRAPHQL = "https://hub.snapshot.org/graphql"

# Map protocol names to Snapshot space IDs
SNAPSHOT_SPACES = {
    "hyperliquid": None,  # No Snapshot governance
    "jupiter": "jup.eth",
    "ethena": "ethena.eth",
    "jito": "jito.dcf.eth",
    "etherfi": "etherfi.eth",
    "ether.fi": "etherfi.eth",
    "pyth": "pythdao.eth",
    "pyth-network": "pythdao.eth",
    "chainlink": None,  # Uses own governance
    "dydx": "dydxgov.eth",
    "maple": "maple.eth",
    "maple-finance": "maple.eth",
    "raydium": None,  # No Snapshot governance
    "uniswap": "uniswapgovernance.eth",
    "arbitrum": "arbitrumfoundation.eth",
    "aave": "aave.eth",
    "berachain": None,
    "eigenlayer": None,
}

BUYBACK_KEYWORDS = [
    "buyback", "buy back", "buy-back",
    "repurchase", "fee switch", "fee-switch",
    "revenue share", "revenue distribution",
    "token burn", "burn mechanism",
    "treasury buyback", "protocol owned",
]


def search_proposals(space: str, keywords: list = None, limit: int = 20) -> list:
    """Search Snapshot proposals for a given space."""
    if keywords is None:
        keywords = BUYBACK_KEYWORDS

    query = """
    query Proposals($space: String!, $first: Int!) {
        proposals(
            first: $first,
            skip: 0,
            where: { space: $space },
            orderBy: "created",
            orderDirection: desc
        ) {
            id
            title
            body
            choices
            start
            end
            state
            scores_total
            votes
            author
            link
        }
    }
    """

    resp = requests.post(
        SNAPSHOT_GRAPHQL,
        json={"query": query, "variables": {"space": space, "first": limit}},
        timeout=30,
    )
    if resp.status_code != 200:
        return []

    data = resp.json()
    proposals = data.get("data", {}).get("proposals", [])

    # Filter for buyback-related proposals
    relevant = []
    for p in proposals:
        text = (p.get("title", "") + " " + p.get("body", "")).lower()
        matching_keywords = [kw for kw in keywords if kw in text]
        if matching_keywords:
            relevant.append({
                "id": p["id"],
                "title": p["title"],
                "state": p["state"],
                "votes": p["votes"],
                "scores_total": p["scores_total"],
                "start": p["start"],
                "end": p["end"],
                "matching_keywords": matching_keywords,
                "link": p.get("link", f"https://snapshot.org/#/{space}/proposal/{p['id']}"),
            })

    return relevant


def scan_all_spaces() -> dict:
    """Scan all known Snapshot spaces for buyback-related proposals."""
    results = {}
    for protocol, space in SNAPSHOT_SPACES.items():
        if space is None:
            continue
        print(f"  Scanning {protocol} ({space})...")
        proposals = search_proposals(space)
        if proposals:
            results[protocol] = {
                "space": space,
                "buyback_proposals": proposals,
                "count": len(proposals),
            }
    return results


def search_global(keywords: list = None, limit: int = 50) -> list:
    """Global search across all Snapshot spaces for buyback proposals."""
    if keywords is None:
        keywords = BUYBACK_KEYWORDS

    # Search using the title field
    all_results = []
    for keyword in keywords[:5]:  # Limit to avoid rate limiting
        query = """
        query Proposals($keyword: String!, $first: Int!) {
            proposals(
                first: $first,
                where: { title_contains: $keyword, state: "closed" },
                orderBy: "scores_total",
                orderDirection: desc
            ) {
                id
                title
                space { id name }
                state
                scores_total
                votes
                start
                end
            }
        }
        """
        resp = requests.post(
            SNAPSHOT_GRAPHQL,
            json={"query": query, "variables": {"keyword": keyword, "first": limit}},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json()
            proposals = data.get("data", {}).get("proposals", [])
            for p in proposals:
                all_results.append({
                    "title": p["title"],
                    "space": p.get("space", {}).get("id"),
                    "space_name": p.get("space", {}).get("name"),
                    "state": p["state"],
                    "votes": p["votes"],
                    "scores_total": p["scores_total"],
                    "keyword": keyword,
                })

    # Deduplicate by title
    seen = set()
    unique = []
    for r in all_results:
        if r["title"] not in seen:
            seen.add(r["title"])
            unique.append(r)

    return sorted(unique, key=lambda x: x.get("scores_total") or 0, reverse=True)


def collect(protocol: str) -> dict:
    """Collect governance data for a specific protocol."""
    space = SNAPSHOT_SPACES.get(protocol.lower())
    if space is None:
        return {
            "source": "snapshot",
            "protocol": protocol,
            "collected_at": datetime.utcnow().isoformat(),
            "note": f"No Snapshot space configured for {protocol}",
            "proposals": [],
        }

    print(f"Collecting Snapshot governance data for {protocol} ({space})...")
    proposals = search_proposals(space)

    return {
        "source": "snapshot",
        "protocol": protocol,
        "space": space,
        "collected_at": datetime.utcnow().isoformat(),
        "buyback_proposals": proposals,
        "count": len(proposals),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python snapshot_gov.py <protocol_name>")
        print("       python snapshot_gov.py --scan-all")
        print("       python snapshot_gov.py --global-search")
        sys.exit(1)

    mode = sys.argv[1]
    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    if mode == "--scan-all":
        result = {
            "source": "snapshot_scan",
            "collected_at": datetime.utcnow().isoformat(),
            "spaces_scanned": scan_all_spaces(),
        }
        out_path = data_dir / "snapshot_scan.json"
    elif mode == "--global-search":
        result = {
            "source": "snapshot_global",
            "collected_at": datetime.utcnow().isoformat(),
            "results": search_global(),
        }
        out_path = data_dir / "snapshot_global.json"
    else:
        result = collect(mode)
        out_path = data_dir / f"{mode}_snapshot.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"Data written to {out_path}")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
