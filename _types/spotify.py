from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    import datetime


class SpotifyData(NamedTuple):
    title: str
    artists: str | list[str]
    album: str | None
    duration: datetime.datetime
