# Run: pipenv run python data_fetching/uniswap_data.py
import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("THE_GRAPH_API_KEY")

GRAPH_URL = "https://gateway.thegraph.com/api/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
}

# 🧩 Uniswap V3 Pools (Mainnet)
POOLS = {
    "WETH/USDC": "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8",
    "WETH/DAI": "0xC2e9f25be6257c210d7adf0d4cd6e3e881ba25f8",
    "DAI/USDC": "0x6c6bc977e13df9b0de53b251522280bb72383700",
}


def fetch_swaps(pool_name, pool_address, limit=10):
    query = f"""
    {{
      swaps(
        first: {limit},
        orderBy: timestamp,
        orderDirection: desc,
        where: {{ pool: "{pool_address.lower()}" }}
      ) {{
        id
        timestamp
        amount0
        amount1
        amountUSD
        sender
        recipient
      }}
    }}
    """
    response = requests.post(GRAPH_URL, headers=HEADERS, json={"query": query})
    data = response.json()

    if "errors" in data:
        print(f"⚠️ Error fetching {pool_name}:")
        print(data["errors"])
        return []

    print(f"\n🔄 Last {limit} swaps for {pool_name}:\n")
    for swap in data["data"]["swaps"]:
        ts = datetime.fromtimestamp(int(swap["timestamp"]))
        print(
            f"🕒 {ts} | 💵 {swap['amountUSD']} USD | sender: {swap['sender']} → {swap['recipient']}"
        )
        print(f"  ↪ amount0: {swap['amount0']} | amount1: {swap['amount1']}")
        print("-" * 50)
        time.sleep(0.1)

    return data["data"]["swaps"]


if __name__ == "__main__":
    for name, address in POOLS.items():
        fetch_swaps(name, address)
