"""
Zone 6 — STRING CAVERNS
15 challenges autour du Cours 7 :
char[], '\0', strlen, strcpy, strcat, strcmp, strncpy, sprintf, sscanf, rand(), srand()

Difficulté : 2,2,3,3 | 3,3,3 | 3 | 3,4,4 | 4 | 4,4 | 5
Rooms 1-4 intro, 5-7 consolidation, 8 mini-boss, 9-11 maîtrise,
12 mini-boss, 13-14 expert, 15 boss
"""

from app.content.challenge_types import ChallengeData

ZONE_6_CHALLENGES: dict[str, ChallengeData] = {

    # ────────────────────────────────────────────
    # ROOM 1 — Intro (difficulté 2)
    # ────────────────────────────────────────────
    "z06_r01": {
        "challenge_id": "z06_r01",
        "zone": 6, "room": 1, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Les Reliques du Char",
        "concept_tags": ["char-array", "string-literal", "null-terminator"],
        "difficulty": 2,
        "question_prompt": "Dans les cavernes, chaque cristal porte un symbole. Associe chaque déclaration à ce qu'elle crée réellement en mémoire.",
        "hint": "Une chaîne entre \"\" ajoute automatiquement un '\\0' à la fin. Un char simple non.",
        "explanation": "char c = 'A' crée un seul caractère. char s[] = \"AB\" crée un tableau de 3 cases : 'A', 'B', '\\0'. Le '\\0' marque la fin de toute chaîne C.",
        "payload": {
            "values": [
                {"id": "v1", "display": "char c = 'A';"},
                {"id": "v2", "display": 'char s[] = "AB";'},
                {"id": "v3", "display": "char t[5];"},
                {"id": "v4", "display": 'char *p = "Hi";'},
            ],
            "types": [
                {"id": "t1", "label": "1 octet — un seul caractère"},
                {"id": "t2", "label": "3 octets — 'A','B','\\0'"},
                {"id": "t3", "label": "5 octets — contenu indéfini"},
                {"id": "t4", "label": "Pointeur vers zone en lecture seule"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    # ────────────────────────────────────────────
    # ROOM 2 — Intro (difficulté 2)
    # ────────────────────────────────────────────
    "z06_r02": {
        "challenge_id": "z06_r02",
        "zone": 6, "room": 2, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "L'Écho du Null",
        "concept_tags": ["strlen", "null-terminator"],
        "difficulty": 2,
        "question_prompt": "Le mage des cavernes invoque strlen. Quelle valeur renvoie l'incantation ?",
        "hint": "strlen compte les caractères AVANT le '\\0'. Elle ne compte pas le '\\0' lui-même.",
        "explanation": "\"ECE\" contient 3 caractères ('E','C','E') puis le '\\0'. strlen retourne 3, pas 4.",
        "payload": {
            "code": '#include <string.h>\nchar mot[] = "ECE";\nint n = strlen(mot);\nprintf("%d\\n", n);',
            "correct_answer": "3",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 3 — Intro (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r03": {
        "challenge_id": "z06_r03",
        "zone": 6, "room": 3, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "La Copie Magique",
        "concept_tags": ["strcpy", "char-array"],
        "difficulty": 3,
        "question_prompt": "L'apprenti veut copier une chaîne dans un tableau. Quelle fonction d'invocation utiliser ?",
        "hint": "En C on ne peut pas faire dest = src pour les tableaux. Il faut une fonction de <string.h> qui copie caractère par caractère.",
        "explanation": "strcpy(dest, src) copie src dans dest, y compris le '\\0'. Attention : dest doit être assez grand !",
        "payload": {
            "code_before": "char dest[20];\n",
            "blank_label": "___",
            "code_after": '(dest, "Bonjour");',
            "options": ["strcpy", "strcat", "strcmp", "strlen"],
            "correct_answer": "strcpy",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 4 — Intro (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r04": {
        "challenge_id": "z06_r04",
        "zone": 6, "room": 4, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Piège du Débordement",
        "concept_tags": ["strcpy", "buffer-overflow"],
        "difficulty": 3,
        "question_prompt": "Ce code compile, mais il cache un piège mortel ! Trouve la ligne dangereuse.",
        "hint": "Compte les caractères de la chaîne source + le '\\0'. Le tableau destination est-il assez grand ?",
        "explanation": "\"Bonjour\" fait 7 caractères + '\\0' = 8 octets, mais dest ne fait que 5. strcpy déborde du buffer = comportement indéfini !",
        "payload": {
            "code": '#include <string.h>\nint main() {\n  char dest[5];\n  strcpy(dest, "Bonjour");\n  printf("%s\\n", dest);\n  return 0;\n}',
            "lines": [
                {"id": "1", "text": "#include <string.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": "  char dest[5];"},
                {"id": "4", "text": '  strcpy(dest, "Bonjour");'},
                {"id": "5", "text": '  printf("%s\\n", dest);'},
                {"id": "6", "text": "  return 0;"},
                {"id": "7", "text": "}"},
            ],
            "correct_answer": 4,
        },
    },

    # ────────────────────────────────────────────
    # ROOM 5 — Consolidation (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r05": {
        "challenge_id": "z06_r05",
        "zone": 6, "room": 5, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "La Fusion des Runes",
        "concept_tags": ["strcat", "strlen"],
        "difficulty": 3,
        "question_prompt": "Le sorcier concatène deux fragments de rune. Quelle longueur obtient-il ?",
        "hint": "strcat ajoute la 2e chaîne à la fin de la 1re (remplace le '\\0' de la 1re). strlen mesure le résultat.",
        "explanation": "\"Bon\" (3 car.) + \"jour\" (4 car.) = \"Bonjour\" (7 car.). strlen retourne 7.",
        "payload": {
            "code": 'char buf[20] = "Bon";\nstrcat(buf, "jour");\nint n = strlen(buf);\nprintf("%d\\n", n);',
            "correct_answer": "7",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 6 — Consolidation (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r06": {
        "challenge_id": "z06_r06",
        "zone": 6, "room": 6, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Rituel de la Chaîne Sûre",
        "concept_tags": ["strncpy", "null-terminator", "safe-copy"],
        "difficulty": 3,
        "question_prompt": "Remets dans l'ordre les étapes pour copier une chaîne en toute sécurité avec strncpy.",
        "hint": "strncpy ne garantit PAS le '\\0' final si la source est trop longue. Il faut le forcer à la main.",
        "explanation": "Bonne pratique : déclarer le buffer → copier avec strncpy(dest, src, sizeof(dest)-1) → forcer dest[sizeof(dest)-1] = '\\0' pour garantir la terminaison.",
        "payload": {
            "cards": [
                {"id": "c1", "text": "char dest[10];"},
                {"id": "c2", "text": "strncpy(dest, src, sizeof(dest) - 1);"},
                {"id": "c3", "text": "dest[sizeof(dest) - 1] = '\\0';"},
                {"id": "c4", "text": "printf(\"%s\\n\", dest);"},
            ],
            "display_order": ["c3", "c1", "c4", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    # ────────────────────────────────────────────
    # ROOM 7 — Consolidation (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r07": {
        "challenge_id": "z06_r07",
        "zone": 6, "room": 7, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Carte des Cavernes",
        "concept_tags": ["char-array", "null-terminator", "memory-layout"],
        "difficulty": 3,
        "question_prompt": "Le tableau char msg[6] = \"Hello\" est rangé en mémoire. Quel slot contient le '\\0' de fin ?",
        "hint": "\"Hello\" = 'H','e','l','l','o' puis '\\0'. Ça fait 6 caractères en tout, dans les cases 0 à 5.",
        "explanation": "msg[0]='H', msg[1]='e', msg[2]='l', msg[3]='l', msg[4]='o', msg[5]='\\0'. Le terminateur est en position 5.",
        "payload": {
            "scenario": "char msg[6] = \"Hello\"; — Où se trouve le '\\0' ?",
            "slots": [
                {"id": "s0", "label": "msg[0] = 'H'"},
                {"id": "s1", "label": "msg[1] = 'e'"},
                {"id": "s2", "label": "msg[2] = 'l'"},
                {"id": "s3", "label": "msg[3] = 'l'"},
                {"id": "s4", "label": "msg[4] = 'o'"},
                {"id": "s5", "label": "msg[5] = ???"},
            ],
            "correct_answer": "s5",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 8 — MINI-BOSS 1 (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r08": {
        "challenge_id": "z06_r08",
        "zone": 6, "room": 8, "is_boss": False, "is_mini_boss": True,
        "challenge_type": "trace_value",
        "title": "MINI-BOSS : Le Gardien du Null",
        "concept_tags": ["strcmp", "null-terminator", "comparison"],
        "difficulty": 3,
        "question_prompt": "Le Gardien du Null te met au défi ! Ce code compare deux chaînes. Que vaut le résultat ?",
        "hint": "strcmp retourne 0 si les chaînes sont identiques, un nombre négatif si s1 < s2 (ordre alphabétique), positif si s1 > s2.",
        "explanation": "strcmp(\"abc\", \"abc\") retourne 0 car les deux chaînes sont identiques caractère par caractère, y compris leur '\\0'.",
        "payload": {
            "code": '#include <string.h>\nchar a[] = "abc";\nchar b[] = "abc";\nint cmp = strcmp(a, b);\nif (cmp == 0) printf("EGAL");\nelse printf("DIFFERENT");',
            "correct_answer": "EGAL",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 9 — Maîtrise (difficulté 3)
    # ────────────────────────────────────────────
    "z06_r09": {
        "challenge_id": "z06_r09",
        "zone": 6, "room": 9, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "Le Scribe de sprintf",
        "concept_tags": ["sprintf", "formatting"],
        "difficulty": 3,
        "question_prompt": "Le scribe veut écrire un message formaté dans un buffer. Quelle fonction utilise-t-il ?",
        "hint": "C'est comme printf, mais au lieu d'écrire sur l'écran, ça écrit dans une chaîne de caractères.",
        "explanation": "sprintf écrit dans un buffer char[] au lieu de la console. Syntaxe : sprintf(buf, \"format\", args...).",
        "payload": {
            "code_before": "char buf[50];\nint score = 42;\n",
            "blank_label": "___",
            "code_after": '(buf, "Score: %d", score);',
            "options": ["sprintf", "printf", "fprintf", "scanf"],
            "correct_answer": "sprintf",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 10 — Maîtrise (difficulté 4)
    # ────────────────────────────────────────────
    "z06_r10": {
        "challenge_id": "z06_r10",
        "zone": 6, "room": 10, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Déchiffreur de sscanf",
        "concept_tags": ["sscanf", "parsing"],
        "difficulty": 4,
        "question_prompt": "Le déchiffreur extrait des valeurs depuis une chaîne. Que contient la variable age après l'incantation ?",
        "hint": "sscanf fonctionne comme scanf mais lit depuis une chaîne au lieu du clavier. Le format \"%*s %d\" ignore un mot puis lit un entier.",
        "explanation": "sscanf lit dans la chaîne \"Age 21\". Le format \"%*s\" ignore \"Age\" (le * signifie ignorer), puis \"%d\" lit 21 dans la variable age.",
        "payload": {
            "code": 'char info[] = "Age 21";\nint age;\nsscanf(info, "%*s %d", &age);\nprintf("%d\\n", age);',
            "correct_answer": "21",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 11 — Maîtrise (difficulté 4)
    # ────────────────────────────────────────────
    "z06_r11": {
        "challenge_id": "z06_r11",
        "zone": 6, "room": 11, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Comparateur Trompeur",
        "concept_tags": ["strcmp", "comparison", "equality"],
        "difficulty": 4,
        "question_prompt": "Ce code devrait vérifier si deux mots de passe sont identiques, mais il ne marche jamais. Trouve le bug !",
        "hint": "En C, l'opérateur == compare les ADRESSES des chaînes, pas leur contenu. Il faut utiliser une fonction de <string.h>.",
        "explanation": "Ligne 4 : pass1 == pass2 compare les pointeurs (adresses mémoire), pas le contenu. Il faut utiliser strcmp(pass1, pass2) == 0.",
        "payload": {
            "code": '#include <string.h>\nchar pass1[] = "secret";\nchar pass2[] = "secret";\nif (pass1 == pass2) {\n  printf("Accès autorisé !\\n");\n}',
            "lines": [
                {"id": "1", "text": "#include <string.h>"},
                {"id": "2", "text": 'char pass1[] = "secret";'},
                {"id": "3", "text": 'char pass2[] = "secret";'},
                {"id": "4", "text": "if (pass1 == pass2) {"},
                {"id": "5", "text": '  printf("Accès autorisé !\\n");'},
                {"id": "6", "text": "}"},
            ],
            "correct_answer": 4,
        },
    },

    # ────────────────────────────────────────────
    # ROOM 12 — MINI-BOSS 2 (difficulté 4)
    # ────────────────────────────────────────────
    "z06_r12": {
        "challenge_id": "z06_r12",
        "zone": 6, "room": 12, "is_boss": False, "is_mini_boss": True,
        "challenge_type": "memory_map",
        "title": "MINI-BOSS : Le Démon des Buffers",
        "concept_tags": ["strcat", "buffer-overflow", "memory-layout"],
        "difficulty": 4,
        "question_prompt": "Le Démon des Buffers te montre un tableau char buf[8] = \"Bon\". Après strcat(buf, \"jour!\"), quel slot est le premier à déborder hors du buffer ?",
        "hint": "buf[8] peut contenir les indices 0 à 7. \"Bon\" + \"jour!\" = \"Bonjour!\" = 8 caractères + '\\0' = 9 octets. Où se trouve le 9e octet ?",
        "explanation": "\"Bonjour!\" fait 8 caractères. Avec le '\\0', il faut 9 octets. buf[8] s'arrête à l'indice 7. Le '\\0' serait écrit en buf[8] — hors limites ! C'est un buffer overflow.",
        "payload": {
            "scenario": "char buf[8] = \"Bon\"; strcat(buf, \"jour!\"); — 'B','o','n','j','o','u','r','!','\\0'. Quel slot est hors du buffer (indice >= 8) ?",
            "slots": [
                {"id": "s0", "label": "buf[0] = 'B'"},
                {"id": "s1", "label": "buf[1] = 'o'"},
                {"id": "s2", "label": "buf[2] = 'n'"},
                {"id": "s3", "label": "buf[3] = 'j'"},
                {"id": "s4", "label": "buf[4] = 'o'"},
                {"id": "s5", "label": "buf[5] = 'u'"},
                {"id": "s6", "label": "buf[6] = 'r'"},
                {"id": "s7", "label": "buf[7] = '!'"},
                {"id": "s8", "label": "buf[8] = '\\0' (HORS LIMITES !)"},
            ],
            "correct_answer": "s8",
        },
    },

    # ────────────────────────────────────────────
    # ROOM 13 — Expert (difficulté 4)
    # ────────────────────────────────────────────
    "z06_r13": {
        "challenge_id": "z06_r13",
        "zone": 6, "room": 13, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "L'Arsenal des Chaînes",
        "concept_tags": ["strlen", "strcpy", "strcat", "strcmp", "sprintf", "sscanf"],
        "difficulty": 4,
        "question_prompt": "Six artefacts magiques, six pouvoirs. Associe chaque fonction à sa description !",
        "hint": "str-len = longueur, str-cpy = copie, str-cat = concaténation, str-cmp = comparaison, s-printf = écrire dans chaîne, s-scanf = lire depuis chaîne.",
        "explanation": "strlen mesure, strcpy copie, strcat concatène, strcmp compare, sprintf formate vers un buffer, sscanf parse depuis une chaîne.",
        "payload": {
            "values": [
                {"id": "v1", "display": "strlen(s)"},
                {"id": "v2", "display": "strcpy(d, s)"},
                {"id": "v3", "display": "strcat(d, s)"},
                {"id": "v4", "display": "strcmp(a, b)"},
                {"id": "v5", "display": "sprintf(buf, fmt, ...)"},
                {"id": "v6", "display": "sscanf(str, fmt, ...)"},
            ],
            "types": [
                {"id": "t1", "label": "Retourne la longueur"},
                {"id": "t2", "label": "Copie src dans dest"},
                {"id": "t3", "label": "Ajoute src à la fin de dest"},
                {"id": "t4", "label": "Compare deux chaînes"},
                {"id": "t5", "label": "Écrit un texte formaté dans un buffer"},
                {"id": "t6", "label": "Lit des valeurs depuis une chaîne"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4", "v5": "t5", "v6": "t6"},
        },
    },

    # ────────────────────────────────────────────
    # ROOM 14 — Expert (difficulté 4)
    # ────────────────────────────────────────────
    "z06_r14": {
        "challenge_id": "z06_r14",
        "zone": 6, "room": 14, "is_boss": False, "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Générateur d'Aléatoire",
        "concept_tags": ["rand", "srand", "modulo"],
        "difficulty": 4,
        "question_prompt": "Remets dans l'ordre les étapes pour générer un nombre aléatoire entre 1 et 6 (comme un dé) en C.",
        "hint": "srand initialise le générateur (une seule fois !). rand() génère un nombre. Le modulo % limite l'intervalle. +1 décale de [0..5] à [1..6].",
        "explanation": "D'abord inclure les headers, puis initialiser le seed avec srand(time(NULL)), puis générer avec rand() % 6 + 1 pour obtenir 1 à 6.",
        "payload": {
            "cards": [
                {"id": "c1", "text": "#include <stdlib.h>"},
                {"id": "c2", "text": "#include <time.h>"},
                {"id": "c3", "text": "srand(time(NULL));"},
                {"id": "c4", "text": "int de = rand() % 6 + 1;"},
                {"id": "c5", "text": "printf(\"Dé : %d\\n\", de);"},
            ],
            "display_order": ["c4", "c2", "c5", "c1", "c3"],
            "correct_answer": ["c1", "c2", "c3", "c4", "c5"],
        },
    },

    # ────────────────────────────────────────────
    # ROOM 15 — BOSS FINAL (difficulté 5)
    # ────────────────────────────────────────────
    "z06_r15": {
        "challenge_id": "z06_r15",
        "zone": 6, "room": 15, "is_boss": True, "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "BOSS : L'Oracle des Chaînes",
        "concept_tags": ["strings", "char-array", "strcpy", "strcat", "strlen", "null-terminator"],
        "difficulty": 5,
        "question_prompt": "L'Oracle des Chaînes te lance l'ultime défi ! Ce code manipule plusieurs fonctions de chaînes. Quelle est la valeur finale affichée ?",
        "hint": "Suis pas à pas : strcpy copie, strcat concatène (ajoute à la fin), strlen mesure. Attention à bien compter chaque caractère !",
        "explanation": "strcpy met \"C est\" (5 car.) dans buf. strcat ajoute \" super\" → \"C est super\" (11 car.). strlen(\"C est super\") = 11. Puis result = 11 + 1 = 12.",
        "payload": {
            "code": '#include <string.h>\nchar buf[50];\nstrcpy(buf, "C est");\nstrcat(buf, " super");\nint len = strlen(buf);\nint result = len + 1;\nprintf("%d\\n", result);',
            "correct_answer": "12",
        },
    },
}
