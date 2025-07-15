import json

from web3 import Web3


class UniswapV3Adapter:
    def __init__(self, web3):
        self.web3 = web3

        with open("abi/UniswapV3QuoterV2.json") as f:
            abi = json.load(f)

        self.quoter_address = Web3.to_checksum_address(
            "0x61fFE014bA17989E743c5F6cB21bF9697530B21e"
        )
        self.contract = self.web3.eth.contract(address=self.quoter_address, abi=abi)

    async def get_price(self, token_in, token_out, amount_in_wei):
        print("\n🔍 Debugging UniswapV3Adapter:")
        print(f"- token_in:     {token_in}")
        print(f"- token_out:    {token_out}")
        print(f"- amount_in:    {amount_in_wei} wei")
        print(f"- Using quoter: {self.quoter_address}")

        try:
            fee = 3000
            sqrt_price_limit_x96 = 0

            params = {
                "tokenIn": Web3.to_checksum_address(token_in),
                "tokenOut": Web3.to_checksum_address(token_out),
                "fee": fee,
                "amountIn": amount_in_wei,
                "sqrtPriceLimitX96": sqrt_price_limit_x96,
            }

            print(f"- Using struct params: {params}")
            result = self.contract.functions.quoteExactInputSingle(params).call()
            print(f"✅ Result: {result} (raw)")

            amount_out = result[0]
            print(f"💡 amountOut: {amount_out}")

            return float(amount_out) / 1e6

        except Exception as e:
            print(f"❌ Exception occurred: {e}")
            return None
