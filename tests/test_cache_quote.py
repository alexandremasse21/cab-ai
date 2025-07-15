import time

from bot.cache.quote_cache import cache_quote, get_cached_quote


def test_cache_quote_basic():
    pair = "WETH/USDC"
    dex = "UniswapV3Adapter"
    price = 3005.55

    # ✅ Met en cache
    cache_quote(pair, dex, price)

    # ✅ Immédiatement disponible
    cached = get_cached_quote(pair, dex)
    assert cached == price, "La valeur devrait être retrouvée immédiatement"

    # ✅ Attendre expiration (TTL = 5s dans ton code)
    time.sleep(6)
    expired = get_cached_quote(pair, dex)
    assert expired is None, "La valeur devrait avoir expiré après 5s"
