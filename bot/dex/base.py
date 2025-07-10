

from abc import ABC, abstractmethod


class DexAdapter(ABC):
    @abstractmethod
    async def get_price(
        self, token_in: str, token_out: str, amount_in_wei: int
    ) -> int:
        pass
