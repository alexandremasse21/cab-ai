import pytest

from scripts.show_spreads import fetch_quotes


@pytest.mark.asyncio
async def test_fetch_quotes_returns_data():
    quotes = await fetch_quotes()
    assert isinstance(quotes, list)
    assert len(quotes) > 0
    assert "pair" in quotes[0]
    assert "spread" in quotes[0]
    assert "from" in quotes[0]
    assert "to" in quotes[0]
