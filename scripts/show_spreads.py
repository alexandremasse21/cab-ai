# Run: pipenv run python -m scripts.show_spreads

import asyncio
import os

from dotenv import load_dotenv
from web3 import Web3

from bot.dex.sushiswap import SushiAdapter
from bot.dex.uniswap_v3 import UniswapV3Adapter

load_dotenv()

INFURA_KEY = os.getenv("INFURA_KEY")
INFURA_URL = f"https://mainnet.infura.io/v3/{INFURA_KEY}"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

TOKENS = [
    (
        "WETH",
        "USDC",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    ),
    (
        "WETH",
        "DAI",
        "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    ),
    (
        "DAI",
        "USDC",
        "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    ),
]

AMOUNT_IN = Web3.to_wei(1, "ether")


async def fetch_quotes():
    adapters = [
        UniswapV3Adapter(web3),
        SushiAdapter(web3),
    ]

    quotes = []

    # Iterate over all token pairs
    for symbol_in, symbol_out, addr_in, addr_out in TOKENS:
        for i in range(len(adapters)):
            for j in range(len(adapters)):
                if i == j:
                    continue

                dex_a = adapters[i]
                dex_b = adapters[j]

                try:
                    out_a = await dex_a.get_price(addr_in, addr_out, AMOUNT_IN)
                    out_b = await dex_b.get_price(addr_in, addr_out, AMOUNT_IN)

                    if out_a and out_b and out_a > 0:
                        spread = (out_b - out_a) / out_a * 100

                        quote = {
                            "pair": f"{symbol_in}/{symbol_out}",
                            "from": dex_a.__class__.__name__,
                            "to": dex_b.__class__.__name__,
                            "price_a": out_a,
                            "price_b": out_b,
                            "spread": spread,
                        }
                        quotes.append(quote)

                except Exception as e:
                    print(f"[⚠️] Error on {symbol_in}/{symbol_out}: {e}")
                    continue

    # ✅ Moved OUTSIDE the loop to return all results
    return sorted(quotes, key=lambda x: abs(x["spread"]), reverse=True)


async def main_loop():
    while True:
        quotes = await fetch_quotes()
        os.system("cls" if os.name == "nt" else "clear")

        print("🔁 Top 5 arbitrage spreads (Mainnet)\n")
        for q in quotes[:5]:
            print(f"{q['pair']} | {q['from']} → {q['to']} | Spread: {q['spread']:.2f}%")

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main_loop())
