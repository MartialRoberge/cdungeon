"""
Strict type definitions for C:\\DUNGEON challenge data.
All challenge dicts must conform to ChallengeData.
"""

from typing import TypedDict

ROOM_COUNT_PER_ZONE: int = 15
ZONE_COUNT: int = 8
MINI_BOSS_ROOMS: tuple[int, int] = (8, 12)
BOSS_ROOM: int = 15


class TraceValuePayload(TypedDict):
    code: str
    correct_answer: str


class FindBugPayload(TypedDict):
    code: str
    lines: list[dict[str, str]]
    correct_answer: int


class FillBlankPayload(TypedDict):
    code_before: str
    blank_label: str
    code_after: str
    options: list[str]
    correct_answer: str


class MatchTypesPayload(TypedDict):
    values: list[dict[str, str]]
    types: list[dict[str, str]]
    correct_answer: dict[str, str]


class SortOrderPayload(TypedDict):
    cards: list[dict[str, str]]
    display_order: list[str]
    correct_answer: list[str]


class MemoryMapPayload(TypedDict):
    scenario: str
    slots: list[dict[str, str]]
    correct_answer: str


Payload = (
    TraceValuePayload
    | FindBugPayload
    | FillBlankPayload
    | MatchTypesPayload
    | SortOrderPayload
    | MemoryMapPayload
)


class ChallengeData(TypedDict):
    challenge_id: str
    zone: int
    room: int
    is_boss: bool
    is_mini_boss: bool
    challenge_type: str
    title: str
    concept_tags: list[str]
    difficulty: int
    question_prompt: str
    hint: str
    explanation: str
    payload: Payload


class ZoneData(TypedDict):
    zone_number: int
    name: str
    theme: str
    emoji: str
    boss_name: str
    mini_boss_1_name: str
    mini_boss_2_name: str
    description: str


def get_boss_room_id(zone: int) -> str:
    """Return the room_id of the final boss for a given zone."""
    return f"z{zone:02d}_r{BOSS_ROOM:02d}"


def get_mini_boss_room_ids(zone: int) -> tuple[str, str]:
    """Return the room_ids of both mini-bosses for a given zone."""
    return (
        f"z{zone:02d}_r{MINI_BOSS_ROOMS[0]:02d}",
        f"z{zone:02d}_r{MINI_BOSS_ROOMS[1]:02d}",
    )


def is_boss_room(room: int) -> bool:
    """Check if a room number is the final boss."""
    return room == BOSS_ROOM


def is_mini_boss_room(room: int) -> bool:
    """Check if a room number is a mini-boss."""
    return room in MINI_BOSS_ROOMS
