from dataclasses import dataclass, field
from typing import Any


@dataclass
class BlockLayout:
    width: int
    height: int
    data: dict[str, Any] = field(default_factory=dict)