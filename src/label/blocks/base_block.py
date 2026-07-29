from abc import ABC, abstractmethod

from ..layout import BlockLayout


class BaseBlock(ABC):

    def __init__(self, product):
        self.product = product

    @abstractmethod
    def measure(
        self,
        draw,
        context,
    ) -> BlockLayout:
        """Calculeaza si returneaza layout-ul blocului."""
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
        """Deseneaza blocul folosind layout-ul calculat."""
        raise NotImplementedError