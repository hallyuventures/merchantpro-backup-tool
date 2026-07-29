from abc import ABC, abstractmethod


class BaseBlock(ABC):

    def __init__(self, product):
        self.product = product

    @abstractmethod
    def measure(self, context):
        """Returnează înălțimea blocului în pixeli."""
        pass

    @abstractmethod
    def render(self, draw, x, y, context):
        """Desenează blocul la coordonatele x, y."""
        pass