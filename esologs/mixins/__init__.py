"""
Mixin classes for ESO Logs API client.

These mixins organize API methods by functional area.
"""

from .character import CharacterMixin
from .game_data import GameDataMixin
from .guild import GuildMixin
from .report import ReportMixin
from .world_data import WorldDataMixin

__all__ = [
    "CharacterMixin",
    "GameDataMixin",
    "GuildMixin",
    "ReportMixin",
    "WorldDataMixin",
]
