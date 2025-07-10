import os
import pytest
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

pytestmark = pytest.mark.asyncio  # Applique asyncio à toutes les fonctions ici


async def test_uniswap_price():
    adapter = SushiAdapter(web3)
    price = await adapter.get_price(WETH, USDC, AMOUNT)
    assert price is not None
    assert price > 0
    print(f"Uniswap price: {price:.2f} USDC")


@pytest.mark.asyncio
async def test_sushi_invalid_token_addresses():
    adapter = SushiAdapter(web3)
    invalid_token = "0x0000000000000000000000000000000000000000"
    with pytest.raises(Exception):
        await adapter.get_price(invalid_token, invalid_token, 1000)


@pytest.mark.asyncio
async def test_sushi_zero_amount():
    adapter = SushiAdapter(web3)
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    amount = 0

    with pytest.raises(ContractLogicError) as excinfo:
        await adapter.get_price(WETH, USDC, amount)

    assert "INSUFFICIENT_INPUT_AMOUNT" in str(excinfo.value)


@pytest.mark.asyncio
async def test_sushi_large_amount():
    adapter = SushiAdapter(web3)
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    USDC = "0xA0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    large_amount = 10**30
    price = await adapter.get_price(WETH, USDC, large_amount)
    assert price is None or price > 0


@pytest.mark.asyncio
async def test_sushi_unsupported_pair():
    adapter = SushiAdapter(web3)
    FAKE_TOKEN = "0x1111111111111111111111111111111111111111"
    WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    with pytest.raises(Exception):
        await adapter.get_price(FAKE_TOKEN, WETH, 1000)
