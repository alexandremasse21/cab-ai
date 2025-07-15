import time
from bot.quote.schema import normalize_quote

def test_normalize_quote_basic():
    quote = normalize_quote(
        token_in="WETH",
        token_out="USDC",
        dex_name="UniswapV3Adapter",
        amount_in=10**18,
        amount_out=3005123456,  # in micro USDC (6 decimals)
        decimals_out=6,
        gas_used=None
    )

    assert quote["pair"] == "WETH/USDC"
    assert quote["dex"] == "UniswapV3Adapter"
    assert abs(quote["price"] - 3005.123456) < 0.000001  # float rounding tolerance
    assert isinstance(quote["ts"], int)
    assert abs(time.time() - quote["ts"]) < 5  # timestamp is recent
    assert quote["gas"] is None


def test_normalize_quote_with_gas():
    quote = normalize_quote(
        token_in="WETH",
        token_out="USDC",
        dex_name="SushiAdapter",
        amount_in=10**18,
        amount_out=2999123456,
        decimals_out=6,
        gas_used=94000
    )

    assert quote["dex"] == "SushiAdapter"
    assert quote["gas"] == 94000
