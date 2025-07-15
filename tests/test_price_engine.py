# Run: pipenv run pytest tests/test_price_engine.py
from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.mark.asyncio
async def test_price_engine_main(monkeypatch, capsys):
    # Mock pour Uniswap
    mock_uni_adapter = MagicMock()
    mock_uni_adapter.get_price = AsyncMock(return_value=3005.12)

    # Mock pour Sushiswap
    mock_sushi_adapter = MagicMock()
    mock_sushi_adapter.get_price = AsyncMock(return_value=3001000)  # 6 décimales (USDC)

    # Monkeypatch les adaptateurs
    monkeypatch.setattr(
        "bot.price_engine.UniswapV3Adapter", lambda web3: mock_uni_adapter
    )
    monkeypatch.setattr(
        "bot.price_engine.SushiAdapter", lambda web3: mock_sushi_adapter
    )

    # Monkeypatch Web3 provider
    mock_web3 = MagicMock()
    monkeypatch.setattr("bot.price_engine.Web3", MagicMock(return_value=mock_web3))
    monkeypatch.setattr("bot.price_engine.Web3.to_wei", lambda x, u: int(x * 1e18))
    monkeypatch.setattr("bot.price_engine.Web3.from_wei", lambda x, u: x / 1e6)

    # Monkeypatch dotenv
    monkeypatch.setattr("bot.price_engine.load_dotenv", lambda: None)
    monkeypatch.setattr(
        "bot.price_engine.os.getenv", lambda key: "https://example-rpc-url"
    )

    # Import et exécute `main()` de manière isolée
    from bot import price_engine

    await price_engine.main()

    # Vérifie la sortie console
    captured = capsys.readouterr()
    assert "Raw Uniswap output: 3005.12" in captured.out
    assert "Uniswap: 3005.12 USDC" in captured.out
    assert "SushiSwap: 3.001 USDC" in captured.out
