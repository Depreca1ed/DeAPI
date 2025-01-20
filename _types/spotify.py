from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple
from dataclasses import dataclass

if TYPE_CHECKING:
    import datetime


class SpotifyData(NamedTuple):
    title: str
    artists: str | list[str]
    album: str | None
    duration: datetime.datetime

@dataclass
class SpotifyInput:
    icon: str
    title: str
    artist: str | list[str]
    album: str | None
