#!/usr/bin/env python3
"""On-chain data collector — protocol-specific RPC queries."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# Public RPCs (no API key needed)
PUBLIC_RPCS = {
    "ethereum": "https://eth.llamarpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
    "base": "https://mainnet.base.org",
    "polygon": "https://polygon-rpc.com",
}


def get_rpc_url(chain: str = "ethereum") -> str:
    """Get RPC URL, preferring env var over public."""
    env_url = os.environ.get("ETH_RPC_URL")
    if env_url and chain == "ethereum":
        return env_url
    return PUBLIC_RPCS.get(chain, PUBLIC_RPCS["ethereum"])


def eth_call(rpc_url: str, to: str, data: str) -> str | None:
    """Make an eth_call to a contract."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": to, "data": data}, "latest"],
        "id": 1,
    }
    resp = requests.post(rpc_url, json=payload, timeout=30)
    if resp.status_code != 200:
        return None
    result = resp.json().get("result")
    return result


def get_erc20_total_supply(rpc_url: str, token_address: str) -> int | None:
    """Get ERC20 total supply."""
    # totalSupply() selector: 0x18160ddd
    result = eth_call(rpc_url, token_address, "0x18160ddd")
    if result and result != "0x":
        return int(result, 16)
    return None


def get_eth_balance(rpc_url: str, address: str) -> float | None:
    """Get ETH balance of an address."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [address, "latest"],
        "id": 1,
    }
    resp = requests.post(rpc_url, json=payload, timeout=30)
    if resp.status_code != 200:
        return None
    result = resp.json().get("result")
    if result:
        return int(result, 16) / 1e18
    return None


# Protocol-specific contract addresses for buyback tracking
PROTOCOL_CONTRACTS = {
    "hyperliquid": {
        "chain": "arbitrum",
        "note": "Hyperliquid L1 is its own chain; Assistance Fund operates on-chain",
        "contracts": {},
    },
    "dydx": {
        "chain": "ethereum",
        "contracts": {
            "token": "0x92D6C1e31e14520e676a687F0a93788B716BEff5",
            "staking": "0x65f7BA4Ec257AF7c55fd5854E5f6356bBd0fb8EC",
        },
    },
    "chainlink": {
        "chain": "ethereum",
        "contracts": {
            "token": "0x514910771AF9Ca656af840dff83E8264EcF986CA",
        },
    },
    "raydium": {
        "chain": "solana",
        "note": "Solana-native, requires different RPC approach",
        "contracts": {},
    },
}


def collect(protocol: str) -> dict:
    """Collect on-chain data for a protocol."""
    protocol_key = protocol.lower().strip()
    config = PROTOCOL_CONTRACTS.get(protocol_key)

    result = {
        "source": "onchain",
        "protocol": protocol,
        "collected_at": datetime.utcnow().isoformat(),
    }

    if not config:
        result["note"] = f"No on-chain config for {protocol}. Add contracts to onchain.py."
        return result

    chain = config.get("chain", "ethereum")
    rpc_url = get_rpc_url(chain)

    if config.get("note"):
        result["note"] = config["note"]

    contracts = config.get("contracts", {})
    if "token" in contracts and chain in PUBLIC_RPCS:
        total_supply = get_erc20_total_supply(rpc_url, contracts["token"])
        if total_supply:
            result["token_total_supply_raw"] = total_supply

    result["chain"] = chain
    result["contracts"] = contracts

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python onchain.py <protocol_name>")
        sys.exit(1)

    protocol = sys.argv[1]
    result = collect(protocol)

    data_dir = Path(__file__).parent.parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    out_path = data_dir / f"{protocol}_onchain.json"

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"Data written to {out_path}")
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
