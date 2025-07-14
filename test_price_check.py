import asyncio
import os

from dotenv import load_dotenv
from web3 import Web3

from bot.dex.sushiswap import SushiAdapter
from bot.dex.uniswap_v3 import UniswapV3Adapter
from bot.quote.schema import normalize_quote  # 🎯 Ajout de la normalisation

# Charger les variables d’environnement (.env)
load_dotenv()

INFURA_KEY = os.getenv("INFURA_KEY")
INFURA_HTTP = f"https://mainnet.infura.io/v3/{INFURA_KEY}"

# 🔗 Tokens
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
AMOUNT = Web3.to_wei(1, "ether")

# Connexion
web3 = Web3(Web3.HTTPProvider(INFURA_HTTP))


async def main():
    print("🔎 Testing price quote for 1 WETH → USDC...\n")

    adapters = [
        UniswapV3Adapter(web3),
        SushiAdapter(web3),
    ]

    for adapter in adapters:
        try:
            amount_out = await adapter.get_price(WETH, USDC, AMOUNT)

            if amount_out is None or amount_out == 0:
                print(f"{adapter.__class__.__name__:<20}: ❌ No result")
                continue

            # 🔁 Normalisation du résultat
            quote = normalize_quote(
                token_in="WETH",
                token_out="USDC",
                dex_name=adapter.__class__.__name__,
                amount_in=AMOUNT,
                amount_out=amount_out,
                decimals_out=6,
                gas_used=None,  # Tu peux passer le gas si dispo
            )

            print(f"{quote['dex']:<20}: {quote['price']:.2f} USDC")

        except Exception as e:
            print(f"{adapter.__class__.__name__:<20}: ❌ Error - {e}")


if __name__ == "__main__":
    asyncio.run(main())
