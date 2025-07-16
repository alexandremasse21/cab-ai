# Run: pipenv run python data_fetching/sushiswap_data.py
import os
import time
from datetime import datetime
from typing import List

import requests

GRAPH_URL = "https://gateway.thegraph.com/api/subgraphs/id/GyZ9MgVQkTWuXGMSd3LXESvpevE8S8aD3uktJh7kbVmc"
API_KEY = os.getenv("THE_GRAPH_API_KEY")

HEADERS = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

# Pools SushiSwap
POOLS = {
    "WETH/USDC": "0x397ff1542f962076d0bfe58ea045ffa2d347aca0",
    "WETH/DAI": "0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f",
    "WETH/USDT": "0x06da0fd433c1a5d7a4faa01111c044910a184553",
}


def fetch_swaps(pair_name: str, pair_address: str, limit: int = 10) -> List[dict]:
    query = f"""
    {{
      swaps(
        first: {limit},
        orderBy: timestamp,
        orderDirection: desc,
        where: {{ pair: "{pair_address.lower()}" }}
      ) {{
        id
        timestamp
        amount0In
        amount0Out
        amount1In
        amount1Out
        amountUSD
        sender
        to
      }}
    }}
    """

    response = requests.post(
        GRAPH_URL,
        headers=HEADERS,
        json={"query": query, "operationName": "Swaps", "variables": {}},
    )

    data = response.json()

    if "errors" in data:
        print(f"⚠️ GraphQL error for {pair_name}: {data['errors']}")
        return []

    print(f"\n🍣 Last {limit} swaps for {pair_name}:\n")
    for swap in data["data"]["swaps"]:
        ts = datetime.fromtimestamp(int(swap["timestamp"]))
        print(
            f"🕒 {ts} | 💵 {swap['amountUSD']} USD | sender: {swap['sender']} → {swap['to']}"
        )
        print(f"  ↪ amount0In: {swap['amount0In']} | amount1Out: {swap['amount1Out']}")
        print("-" * 50)
        time.sleep(0.05)

    return data["data"]["swaps"]


if __name__ == "__main__":
    for name, addr in POOLS.items():
        fetch_swaps(name, addr, limit=10)
