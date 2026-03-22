"""Zone challenge modules — one file per zone, 15 challenges each."""

from app.content.zones.zone_01 import ZONE_1_CHALLENGES
from app.content.zones.zone_02 import ZONE_2_CHALLENGES
from app.content.zones.zone_03 import ZONE_3_CHALLENGES
from app.content.zones.zone_04 import ZONE_4_CHALLENGES
from app.content.zones.zone_05 import ZONE_5_CHALLENGES
from app.content.zones.zone_06 import ZONE_6_CHALLENGES
from app.content.zones.zone_07 import ZONE_7_CHALLENGES
from app.content.zones.zone_08 import ZONE_8_CHALLENGES

ALL_ZONE_CHALLENGES = [
    ZONE_1_CHALLENGES,
    ZONE_2_CHALLENGES,
    ZONE_3_CHALLENGES,
    ZONE_4_CHALLENGES,
    ZONE_5_CHALLENGES,
    ZONE_6_CHALLENGES,
    ZONE_7_CHALLENGES,
    ZONE_8_CHALLENGES,
]

__all__ = [
    "ZONE_1_CHALLENGES",
    "ZONE_2_CHALLENGES",
    "ZONE_3_CHALLENGES",
    "ZONE_4_CHALLENGES",
    "ZONE_5_CHALLENGES",
    "ZONE_6_CHALLENGES",
    "ZONE_7_CHALLENGES",
    "ZONE_8_CHALLENGES",
    "ALL_ZONE_CHALLENGES",
]
