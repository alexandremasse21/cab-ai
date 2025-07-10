import os

from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import ContractLogicError

from bot.dex.sushiswap import SushiAdapter

load_dotenv()

INFURA_KEY = os.getenv("INFURA_KEY")
INFURA_HTTP = f"https://mainnet.infura.io/v3/{INFURA_KEY}"
web3 = Web3(Web3.HTTPProvider(INFURA_HTTP))

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
AMOUNT = Web3.to_wei(1, "ether")


async def test_uniswap_price():
    adapter = SushiAdapter(web3)
    price = await adapter.get_price(WETH, USDC, AMOUNT)
    assert price is not None
    assert price > 0
    print(f"Uniswap price: {price:.2f} USDC")
