# Run: pipenv run pytest tests/test_uniswap_v3.py
import pytest
from unittest.mock import MagicMock
from bot.dex.uniswap_v3 import UniswapV3Adapter

@pytest.mark.asyncio
async def test_uniswap_get_price_mock():
    mock_web3 = MagicMock()
    mock_contract = MagicMock()

    # Mock de retour simulant un prix de 3000.00 USDC (avec 6 décimales)
    mock_quote = [3_000_000, 0, 0, 0]  # ← important : 3_000_000 / 1e6 = 3.0

    # Simule le contrat et sa méthode
    mock_contract.functions.quoteExactInputSingle.return_value.call.return_value = mock_quote
    mock_web3.eth.contract.return_value = mock_contract

    adapter = UniswapV3Adapter(mock_web3)

    # Adresses Ethereum valides fictives
    token_in = "0x0000000000000000000000000000000000000001"
    token_out = "0x0000000000000000000000000000000000000002"
    amount_in = 1_000_000_000_000_000_000  # 1 ETH en wei

    result = await adapter.get_price(token_in, token_out, amount_in)

    assert result == 3.0
