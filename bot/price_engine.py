import asyncio
import os

from dex.sushiswap import SushiAdapter
from dex.uniswap_v3 import UniswapV3Adapter
from dotenv import load_dotenv
from web3 import Web3

# Token addresses (Ethereum mainnet)
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"

# Amount to simulate swap: 1 ETH in wei
amount_in = Web3.to_wei(1, "ether")

# RPC connection
load_dotenv()

RPC_URL = os.getenv("RPC_URL")
web3 = Web3(Web3.HTTPProvider(RPC_URL))


async def main():
    u = UniswapV3Adapter(web3)
    s = SushiAdapter(web3)

    quote_uni = await u.get_price(WETH, USDC, amount_in)
    quote_sushi = await s.get_price(WETH, USDC, amount_in)

    print("Raw Uniswap output:", quote_uni, type(quote_uni))
    print("Uniswap:", quote_uni, "USDC")  # déjà float en USDC

    print("SushiSwap:", Web3.from_wei(quote_sushi, "mwei"), "USDC")


if __name__ == "__main__":
    asyncio.run(main())
