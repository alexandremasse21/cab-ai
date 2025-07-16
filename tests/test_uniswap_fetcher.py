# Run: pipenv run pytest tests/test_uniswap_fetcher.py
import pytest
from unittest.mock import patch, MagicMock
from data_fetching.uniswap_data import fetch_swaps

MOCK_GRAPHQL_RESPONSE = {
    "data": {
        "swaps": [
            {
                "id": "0xabc",
                "timestamp": "1720000000",
                "amount0": "1.0",
                "amount1": "3284.01",
                "amountUSD": "3284.01",
                "sender": "0x123",
                "recipient": "0x456"
            }
        ]
    }
}

@patch('data_fetching.uniswap_data.requests.post')
def test_fetch_swaps_mock(mock_post):
    mock_post.return_value.json.return_value = MOCK_GRAPHQL_RESPONSE

    swaps = fetch_swaps("WETH/USDC", "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8", limit=1)

    assert isinstance(swaps, list)
    assert len(swaps) == 1
    assert swaps[0]["amountUSD"] == "3284.01"
    assert swaps[0]["sender"] == "0x123"

@patch('data_fetching.uniswap_data.requests.post')
def test_uniswap_fetch_error(mock_post):
    mock_post.return_value.json.return_value = {
        "errors": [{"message": "Invalid"}]
    }
    swaps = fetch_swaps("UNI/FAKE", "0x0", limit=1)
    assert swaps == []

@patch('data_fetching.uniswap_data.requests.post')
def test_uniswap_fetch_empty(mock_post):
    mock_post.return_value.json.return_value = {
        "data": {
            "swaps": []
        }
    }
    swaps = fetch_swaps("UNI/USDC", "0x1", limit=1)
    assert swaps == []