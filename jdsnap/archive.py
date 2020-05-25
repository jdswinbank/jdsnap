from dataclasses import dataclass
from datetime import datetime

__all__ = ["Archive"]


@dataclass(frozen=True)
class Archive(object):
    name: str
    date: datetime
