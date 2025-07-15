from unittest.mock import MagicMock

import pytest

from bot.dex.sushiswap import SushiAdapter


@pytest.mark.asyncio
async def test_sushi_get_price_mock():
    mock_web3 = MagicMock()
    mock_contract = MagicMock()

    # Simule un retour pour getAmountsOut: 1 ETH => 2995.12 USDC (6 décimales)
    mock_contract.functions.getAmountsOut.return_value.call.return_value = [
        1_000_000_000_000_000_000,  # input
        2_995_120_000,  # output
    ]
    mock_web3.eth.contract.return_value = mock_contract

    adapter = SushiAdapter(mock_web3)

    token_in = "0x0000000000000000000000000000000000000001"
    token_out = "0x0000000000000000000000000000000000000002"
    amount_in = 1_000_000_000_000_000_000  # 1 ETH en wei

    result = await adapter.get_price(token_in, token_out, amount_in)

    # 💡 USDC a 6 décimales → 2995.12 USDC = 2995120000
    assert result == 2_995_120_000
