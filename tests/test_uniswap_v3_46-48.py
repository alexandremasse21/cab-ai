# Run: pipenv run pytest tests/test_uniswap_v3_46-48.py
import pytest
from unittest.mock import MagicMock
from bot.dex.uniswap_v3 import UniswapV3Adapter

@pytest.mark.asyncio
async def test_uniswap_get_price_error(monkeypatch):
    mock_web3 = MagicMock()
    mock_contract = MagicMock()
    
    # Simuler une exception sur le call
    mock_contract.functions.quoteExactInputSingle.return_value.call.side_effect = Exception("Mocked error")
    mock_web3.eth.contract.return_value = mock_contract

    adapter = UniswapV3Adapter(mock_web3)

    result = await adapter.get_price(
        "0x0000000000000000000000000000000000000001",
        "0x0000000000000000000000000000000000000002",
        10**18
    )

    assert result is None
