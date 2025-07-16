# Run: pipenv run pytest tests/test_sushiswap_fetcher.py
from unittest.mock import patch
from data_fetching.sushiswap_data import fetch_swaps

MOCK_RESPONSES = {
    "0x397ff1542f962076d0bfe58ea045ffa2d347aca0": {  # WETH/USDC
        "data": {
            "swaps": [
                {
                    "timestamp": "1721151659",
                    "amount0In": "100",
                    "amount1Out": "0.03",
                    "amountUSD": "1234.56",
                    "sender": "0xabc123",
                    "to": "0xdef456"
                }
            ]
        }
    },
    "0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f": {  # WETH/DAI
        "data": {
            "swaps": [
                {
                    "timestamp": "1721151000",
                    "amount0In": "200",
                    "amount1Out": "0.07",
                    "amountUSD": "4321.00",
                    "sender": "0x111111",
                    "to": "0x222222"
                }
            ]
        }
    },
    "0x06da0fd433C1A5d7a4faa01111c044910A184553": {  # WETH/USDT
        "data": {
            "swaps": [
                {
                    "timestamp": "1721150000",
                    "amount0In": "50",
                    "amount1Out": "0.01",
                    "amountUSD": "987.65",
                    "sender": "0xaaaaaa",
                    "to": "0xbbbbbb"
                }
            ]
        }
    }
}

@patch('data_fetching.sushiswap_data.requests.post')
def test_fetch_multiple_pools(mock_post):
    for pair_name, pair_address in [
        ("WETH/USDC", "0x397ff1542f962076d0bfe58ea045ffa2d347aca0"),
        ("WETH/DAI", "0xc3d03e4f041fd4cd388c549ee2a29a9e5075882f"),
        ("WETH/USDT", "0x06da0fd433C1A5d7a4faa01111c044910A184553")
    ]:
        mock_post.return_value.json.return_value = MOCK_RESPONSES[pair_address]

        swaps = fetch_swaps(pair_name, pair_address, limit=1)

        assert isinstance(swaps, list)
        assert len(swaps) == 1
        assert "amountUSD" in swaps[0]
        assert "sender" in swaps[0]

@patch('data_fetching.sushiswap_data.requests.post')
def test_fetch_swaps_with_error(mock_post):
    mock_post.return_value.json.return_value = {
        "errors": [{"message": "Invalid pair"}]
    }

    swaps = fetch_swaps("WETH/FAKE", "0xdeadbeef", limit=1)
    assert swaps == []

@patch('data_fetching.sushiswap_data.requests.post')
def test_fetch_swaps_empty(mock_post):
    mock_post.return_value.json.return_value = {
        "data": {
            "swaps": []
        }
    }

    swaps = fetch_swaps("WETH/USDC", "0x1234", limit=1)
    assert swaps == []