"""
All challenge content for C:\\DUNGEON.
8 zones x 15 rooms = 120 rooms total.
Each room has one challenge. Challenge types rotate to keep it fresh.
"""

from app.content.challenge_types import ChallengeData, ZoneData
from app.content.zones import (
    ZONE_1_CHALLENGES,
    ZONE_2_CHALLENGES,
    ZONE_3_CHALLENGES,
    ZONE_4_CHALLENGES,
    ZONE_5_CHALLENGES,
    ZONE_6_CHALLENGES,
    ZONE_7_CHALLENGES,
    ZONE_8_CHALLENGES,
)

CHALLENGES: dict[str, ChallengeData] = {}
CHALLENGES.update(ZONE_1_CHALLENGES)
CHALLENGES.update(ZONE_2_CHALLENGES)
CHALLENGES.update(ZONE_3_CHALLENGES)
CHALLENGES.update(ZONE_4_CHALLENGES)
CHALLENGES.update(ZONE_5_CHALLENGES)
CHALLENGES.update(ZONE_6_CHALLENGES)
CHALLENGES.update(ZONE_7_CHALLENGES)
CHALLENGES.update(ZONE_8_CHALLENGES)


# Zone metadata
ZONES: list[ZoneData] = [
    {
        "zone_number": 1, "name": "Stack Village", "theme": "village",
        "emoji": "\U0001f3e0", "boss_name": "Le Golem des Types",
        "mini_boss_1_name": "Le Garde des Variables",
        "mini_boss_2_name": "La Sentinelle Printf",
        "description": "Variables, types, printf/scanf. Les fondations.",
    },
    {
        "zone_number": 2, "name": "Logic Labyrinth", "theme": "labyrinth",
        "emoji": "\U0001f300", "boss_name": "Le Golem Infinite Loop",
        "mini_boss_1_name": "Le Piege Conditionnel",
        "mini_boss_2_name": "La Boucle Infernale",
        "description": "if/else, boucles, logique booleenne.",
    },
    {
        "zone_number": 3, "name": "Function Factory", "theme": "factory",
        "emoji": "\u2699\ufe0f", "boss_name": "L'Usine Recursive",
        "mini_boss_1_name": "Le Gardien des Prototypes",
        "mini_boss_2_name": "Le Spectre du Scope",
        "description": "Fonctions, parametres, multi-fichiers.",
    },
    {
        "zone_number": 4, "name": "Data Fortress", "theme": "fortress",
        "emoji": "\U0001f3f0", "boss_name": "La Forteresse des Donnees",
        "mini_boss_1_name": "La Sentinelle des Tableaux",
        "mini_boss_2_name": "Le Titan du Tri",
        "description": "Tableaux, structures, typedef.",
    },
    {
        "zone_number": 5, "name": "Pointer Abyss", "theme": "abyss",
        "emoji": "\U0001f573\ufe0f", "boss_name": "Le Dragon Segfault",
        "mini_boss_1_name": "Le Fantome de l'Adresse",
        "mini_boss_2_name": "L'Arithmeticien des Pointeurs",
        "description": "Pointeurs, adresses, passage par reference.",
    },
    {
        "zone_number": 6, "name": "String Caverns", "theme": "cavern",
        "emoji": "\U0001f524", "boss_name": "L'Oracle des Chaines",
        "mini_boss_1_name": "Le Gardien du Null",
        "mini_boss_2_name": "Le Demon des Buffers",
        "description": "Chaines de caracteres, fonctions string, aleatoire.",
    },
    {
        "zone_number": 7, "name": "Heap Wastes", "theme": "wasteland",
        "emoji": "\u2623\ufe0f", "boss_name": "L'Hydre Memory Leak",
        "mini_boss_1_name": "Le Spectre du Malloc",
        "mini_boss_2_name": "Le Gardien du Free",
        "description": "malloc, calloc, free, fuites memoire.",
    },
    {
        "zone_number": 8, "name": "File Sanctum", "theme": "sanctum",
        "emoji": "\U0001f4dc", "boss_name": "Le Gardien du Sanctuaire",
        "mini_boss_1_name": "Le Gardien des Modes",
        "mini_boss_2_name": "Le Spectre Binaire",
        "description": "Fichiers texte et binaires, fopen/fclose.",
    },
]
