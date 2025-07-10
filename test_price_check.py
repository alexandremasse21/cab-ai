import asyncio
import os

from dotenv import load_dotenv
from web3 import Web3

from bot.dex.sushi import SushiAdapter
from bot.dex.uniswap_v3 import UniswapV3Adapter

# Charger les variables d’environnement (.env)
load_dotenv()

# 🔐 Clé Infura
INFURA_KEY = os.getenv("INFURA_KEY")
INFURA_HTTP = f"https://mainnet.infura.io/v3/{INFURA_KEY}"

# 🔗 Adresse des tokens
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
AMOUNT = Web3.to_wei(1, "ether")

# Connexion au réseau Ethereum
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

            if amount_out is None:
                print(f"{adapter.__class__.__name__:<20}: ❌ No result")
            else:
                # 🔍 Conversion USDC : dépend de l'adapter
                # UniswapV3Adapter retourne déjà un float en USDC
                # SushiAdapter retourne probablement en wei (18 décimales)
                if adapter.__class__.__name__ == "SushiAdapter":
                    readable = float(amount_out) / 1e6  # USDC = 6 décimales
                else:
                    readable = amount_out  # déjà float

                print(f"{adapter.__class__.__name__:<20}: {readable:.2f} USDC")

        except Exception as e:
            print(f"{adapter.__class__.__name__:<20}: ❌ Error - {e}")


if __name__ == "__main__":
    asyncio.run(main())
