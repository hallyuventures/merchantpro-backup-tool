from abc import ABC, abstractmethod

from ..layout import BlockLayout


class BaseBlock(ABC):

    def __init__(self, product):
        self.product = product

    @abstractmethod
    def measure(self, context) -> BlockLayout:
        """Calculează și returnează layout-ul blocului."""
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        draw,
        x: int,
        y: int,
        layout: BlockLayout,
        context,
    ) -> None:
        """Desenează blocul folosind layout-ul deja calculat."""
        raise NotImplementedError