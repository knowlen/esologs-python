"""
Mixin classes for ESO Logs API client.

These mixins organize API methods by functional area.
"""

from esologs.mixins.character import CharacterMixin
from esologs.mixins.game_data import GameDataMixin
from esologs.mixins.guild import GuildMixin
from esologs.mixins.report import ReportMixin
from esologs.mixins.world_data import WorldDataMixin

__all__ = [
    "CharacterMixin",
    "GameDataMixin",
    "GuildMixin",
    "ReportMixin",
    "WorldDataMixin",
]
