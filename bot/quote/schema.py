from time import time
from typing import Optional


def normalize_quote(
    token_in: str,
    token_out: str,
    dex_name: str,
    amount_in: int,
    amount_out: int,
    decimals_out: int = 6,
    gas_used: Optional[int] = None,
):
    return {
        "pair": f"{token_in}/{token_out}",
        "dex": dex_name,
        "price": round(amount_out / (10**decimals_out), 6),
        "ts": int(time()),
        "gas": gas_used,
    }
