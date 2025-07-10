import json

from web3 import Web3

from .base import DexAdapter

# SushiSwap Router address on Ethereum mainnet
address = "0xd9e1cE17f2641F24aE83637ab66a2CCA9C378B9F"

SUSHI_ROUTER = Web3.to_checksum_address(address)

with open("abi/UniswapV2Router02.json") as f:
    ABI = json.load(f)


class SushiAdapter(DexAdapter):
    def __init__(self, web3: Web3):
        self.web3 = web3
        self.router = web3.eth.contract(
            address=SUSHI_ROUTER,
            abi=ABI)

    async def get_price(self, token_in, token_out, amount_in_wei):
        path = [
            Web3.to_checksum_address(token_in),
            Web3.to_checksum_address(token_out)]
        amounts = self.router.functions.getAmountsOut(
            amount_in_wei,
            path).call()
        return amounts[-1]
