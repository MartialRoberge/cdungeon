"""
Zone 2 — Logic Labyrinth
Cours 3 : Booleens, tables de verite, &&/||/!, if/else, switch,
           ternaire, for, while, do-while, break/continue

15 salles  |  difficultes : 1,1,2,2 | 2,2,2 | 3 | 2,3,3 | 3 | 3,3 | 4
"""

from app.content.challenge_types import ChallengeData

# ────────────────────────────────────────────────────────────
# Room  1 — Introduction (difficulty 1)
# ────────────────────────────────────────────────────────────
_z02_r01: ChallengeData = {
    "challenge_id": "z02_r01",
    "zone": 2,
    "room": 1,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "Le Portail de Verite",
    "concept_tags": ["booleen", "operateur_logique", "&&"],
    "difficulty": 1,
    "question_prompt": (
        "Un parchemin est cloue sur la porte du labyrinthe. "
        "Quel nombre s'affiche quand tu executes ce sort ?"
    ),
    "hint": "En C, une expression vraie vaut 1, une expression fausse vaut 0.",
    "explanation": (
        "5 > 3 est vrai (1) et 2 < 4 est vrai (1). "
        "1 && 1 donne 1. printf affiche donc 1."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int a = 5, b = 3, c = 2, d = 4;\n'
            '    printf("%d", (a > b) && (c < d));\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "1",
    },
}

# ────────────────────────────────────────────────────────────
# Room  2 — Introduction (difficulty 1)
# ────────────────────────────────────────────────────────────
_z02_r02: ChallengeData = {
    "challenge_id": "z02_r02",
    "zone": 2,
    "room": 2,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "fill_blank",
    "title": "Le Couloir des Conditions",
    "concept_tags": ["if", "else", "condition"],
    "difficulty": 1,
    "question_prompt": (
        "Le mur du couloir porte un sort incomplet. "
        "Quel mot-cle faut-il placer dans le blanc pour que "
        "le programme affiche \"mineur\" quand age vaut 15 ?"
    ),
    "hint": "Le bloc qui s'execute quand la condition du if est fausse commence par…",
    "explanation": (
        "Quand age (15) est inferieur a 18, la condition du if est fausse. "
        "C'est le bloc else qui s'execute et affiche \"mineur\"."
    ),
    "payload": {
        "code_before": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int age = 15;\n'
            '    if (age >= 18) {\n'
            '        printf("majeur");\n'
            '    }'
        ),
        "blank_label": "???",
        "code_after": (
            ' {\n'
            '        printf("mineur");\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "options": ["elif", "else", "otherwise", "default"],
        "correct_answer": "else",
    },
}

# ────────────────────────────────────────────────────────────
# Room  3 — Introduction (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r03: ChallengeData = {
    "challenge_id": "z02_r03",
    "zone": 2,
    "room": 3,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "match_types",
    "title": "La Table de Verite Magique",
    "concept_tags": ["booleen", "table_de_verite", "&&", "||", "!"],
    "difficulty": 2,
    "question_prompt": (
        "Les runes sur le sol forment une table de verite. "
        "Associe chaque expression a son resultat (0 ou 1)."
    ),
    "hint": "&& = ET (les deux vrais), || = OU (au moins un vrai), ! = NON (inverse).",
    "explanation": (
        "1 && 0 = 0 (faux car un operande est faux). "
        "1 || 0 = 1 (vrai car au moins un est vrai). "
        "!0 = 1 (NON de faux = vrai). "
        "!(1 && 1) = !1 = 0."
    ),
    "payload": {
        "values": [
            {"id": "v1", "display": "1 && 0"},
            {"id": "v2", "display": "1 || 0"},
            {"id": "v3", "display": "!0"},
            {"id": "v4", "display": "!(1 && 1)"},
        ],
        "types": [
            {"id": "t0", "label": "0 (faux)"},
            {"id": "t1", "label": "1 (vrai)"},
        ],
        "correct_answer": {
            "v1": "t0",
            "v2": "t1",
            "v3": "t1",
            "v4": "t0",
        },
    },
}

# ────────────────────────────────────────────────────────────
# Room  4 — Introduction (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r04: ChallengeData = {
    "challenge_id": "z02_r04",
    "zone": 2,
    "room": 4,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "L'Escalier Ternaire",
    "concept_tags": ["ternaire", "condition"],
    "difficulty": 2,
    "question_prompt": (
        "Un escalier magique monte ou descend selon un sort ternaire. "
        "Qu'affiche ce programme ?"
    ),
    "hint": "L'operateur ternaire : condition ? valeur_si_vrai : valeur_si_faux.",
    "explanation": (
        "x vaut 7 et y vaut 3. 7 > 3 est vrai, donc l'operateur ternaire "
        "renvoie x - y = 4. printf affiche 4."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int x = 7, y = 3;\n'
            '    int res = (x > y) ? x - y : x + y;\n'
            '    printf("%d", res);\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "4",
    },
}

# ────────────────────────────────────────────────────────────
# Room  5 — Consolidation (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r05: ChallengeData = {
    "challenge_id": "z02_r05",
    "zone": 2,
    "room": 5,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "sort_order",
    "title": "Les Dalles du Switch",
    "concept_tags": ["switch", "case", "break"],
    "difficulty": 2,
    "question_prompt": (
        "Les dalles du sol sont dans le desordre ! "
        "Remets les lignes dans l'ordre pour former un switch correct "
        "qui affiche le nom du jour (1 = lundi)."
    ),
    "hint": "switch(variable) { case valeur: instructions; break; default: ... }",
    "explanation": (
        "Un switch commence par switch(jour), puis chaque case, "
        "son instruction, un break, et on finit par default + "
        "l'accolade fermante."
    ),
    "payload": {
        "cards": [
            {"id": "c1", "text": 'switch (jour) {'},
            {"id": "c2", "text": '    case 1: printf("lundi"); break;'},
            {"id": "c3", "text": '    case 2: printf("mardi"); break;'},
            {"id": "c4", "text": '    default: printf("autre"); break;'},
            {"id": "c5", "text": '}'},
        ],
        "display_order": ["c4", "c2", "c5", "c1", "c3"],
        "correct_answer": ["c1", "c2", "c3", "c4", "c5"],
    },
}

# ────────────────────────────────────────────────────────────
# Room  6 — Consolidation (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r06: ChallengeData = {
    "challenge_id": "z02_r06",
    "zone": 2,
    "room": 6,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "find_bug",
    "title": "Le Piege de la Boucle For",
    "concept_tags": ["for", "boucle", "bug"],
    "difficulty": 2,
    "question_prompt": (
        "Un piege magique a corrompu ce sort ! "
        "Ce programme devrait afficher les nombres de 1 a 5, "
        "mais il boucle a l'infini. "
        "Quelle ligne contient le bug ?"
    ),
    "hint": "Regarde bien la condition de continuation dans le for.",
    "explanation": (
        "Ligne 3 : la condition est i != 0 au lieu de i <= 5. "
        "Comme i demarre a 1 et ne vaut jamais 0 en incrementant, "
        "la boucle ne s'arrete jamais."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    for (int i = 1; i != 0; i++) {\n'
            '        printf("%d ", i);\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "lines": [
            {"id": "1", "text": '#include <stdio.h>'},
            {"id": "2", "text": 'int main(void) {'},
            {"id": "3", "text": '    for (int i = 1; i != 0; i++) {'},
            {"id": "4", "text": '        printf("%d ", i);'},
            {"id": "5", "text": '    }'},
            {"id": "6", "text": '    return 0;'},
            {"id": "7", "text": '}'},
        ],
        "correct_answer": 3,
    },
}

# ────────────────────────────────────────────────────────────
# Room  7 — Consolidation (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r07: ChallengeData = {
    "challenge_id": "z02_r07",
    "zone": 2,
    "room": 7,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "La Fontaine While",
    "concept_tags": ["while", "boucle", "compteur"],
    "difficulty": 2,
    "question_prompt": (
        "Une fontaine enchantee compte ses gouttes avec une boucle while. "
        "Combien de fois le mot \"goutte\" est-il affiche ?"
    ),
    "hint": "Suis la valeur de n a chaque tour de boucle jusqu'a ce que la condition soit fausse.",
    "explanation": (
        "n commence a 10. A chaque tour, n est divise par 2 : "
        "10 -> 5 -> 2 -> 1 -> 0. Quand n vaut 0 la boucle s'arrete. "
        "Il y a donc 4 affichages."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int n = 10;\n'
            '    while (n > 0) {\n'
            '        printf("goutte\\n");\n'
            '        n = n / 2;\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "4",
    },
}

# ────────────────────────────────────────────────────────────
# Room  8 — MINI-BOSS #1 (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r08: ChallengeData = {
    "challenge_id": "z02_r08",
    "zone": 2,
    "room": 8,
    "is_boss": False,
    "is_mini_boss": True,
    "challenge_type": "memory_map",
    "title": "MINI-BOSS : Le Piege Conditionnel",
    "concept_tags": ["if", "else_if", "condition", "evaluation"],
    "difficulty": 3,
    "question_prompt": (
        "Le Piege Conditionnel te soumet a une epreuve de logique ! "
        "Apres execution du code ci-dessous, quelle est la valeur "
        "stockee dans la variable result ?"
    ),
    "hint": (
        "Evalue les conditions dans l'ordre : le premier if/else if "
        "dont la condition est vraie est execute, les autres sont ignores."
    ),
    "explanation": (
        "x vaut 15. La premiere condition (x > 20) est fausse. "
        "La deuxieme (x > 10) est vraie, donc result = x * 2 = 30. "
        "Le else n'est pas execute."
    ),
    "payload": {
        "scenario": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int x = 15;\n'
            '    int result;\n'
            '    if (x > 20) {\n'
            '        result = x * 3;\n'
            '    } else if (x > 10) {\n'
            '        result = x * 2;\n'
            '    } else {\n'
            '        result = x;\n'
            '    }\n'
            '    printf("%d", result);\n'
            '    return 0;\n'
            '}'
        ),
        "slots": [
            {"id": "s1", "label": "result = 45"},
            {"id": "s2", "label": "result = 30"},
            {"id": "s3", "label": "result = 15"},
            {"id": "s4", "label": "result = 0"},
        ],
        "correct_answer": "s2",
    },
}

# ────────────────────────────────────────────────────────────
# Room  9 — Maitrise (difficulty 2)
# ────────────────────────────────────────────────────────────
_z02_r09: ChallengeData = {
    "challenge_id": "z02_r09",
    "zone": 2,
    "room": 9,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "fill_blank",
    "title": "Le Passage Do-While",
    "concept_tags": ["do_while", "boucle"],
    "difficulty": 2,
    "question_prompt": (
        "Un passage secret ne s'ouvre que si la boucle s'execute au moins "
        "une fois, meme si la condition est fausse des le depart. "
        "Quel mot-cle manque pour completer la boucle ?"
    ),
    "hint": "Quelle boucle en C garantit au moins une execution du corps ?",
    "explanation": (
        "La boucle do { ... } while (condition); execute d'abord le bloc, "
        "puis verifie la condition. Meme si n vaut 0, le printf s'execute "
        "une fois."
    ),
    "payload": {
        "code_before": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int n = 0;'
        ),
        "blank_label": "???",
        "code_after": (
            ' {\n'
            '        printf("passage ouvert\\n");\n'
            '        n--;\n'
            '    } while (n > 0);\n'
            '    return 0;\n'
            '}'
        ),
        "options": ["for", "while", "do", "repeat"],
        "correct_answer": "do",
    },
}

# ────────────────────────────────────────────────────────────
# Room 10 — Maitrise (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r10: ChallengeData = {
    "challenge_id": "z02_r10",
    "zone": 2,
    "room": 10,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "Le Labyrinthe Break",
    "concept_tags": ["for", "break", "boucle"],
    "difficulty": 3,
    "question_prompt": "Un aventurier parcourt un couloir avec une boucle for. Un piege le force a s'arreter avec break. Qu'affiche ce programme ?",
    "hint": "break sort immediatement de la boucle la plus proche.",
    "explanation": (
        "La boucle demarre a i = 0. Quand i atteint 3, "
        "le if (i == 3) declenche break AVANT le printf de ce tour. "
        "Le dernier printf execute est donc celui pour i = 2. "
        "Sortie : 0 1 2 — la derniere valeur affichee est 2."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    for (int i = 0; i < 10; i++) {\n'
            '        if (i == 3) break;\n'
            '        printf("%d ", i);\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "0 1 2",
    },
}

# ────────────────────────────────────────────────────────────
# Room 11 — Maitrise (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r11: ChallengeData = {
    "challenge_id": "z02_r11",
    "zone": 2,
    "room": 11,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "find_bug",
    "title": "Le Sort Continue Corrompu",
    "concept_tags": ["for", "continue", "boucle", "bug"],
    "difficulty": 3,
    "question_prompt": (
        "Ce programme devrait afficher uniquement les nombres impairs "
        "de 1 a 9, mais il affiche tous les nombres. "
        "Quelle ligne est buguee ?"
    ),
    "hint": "continue saute le reste du corps de la boucle. Verifie la condition du if.",
    "explanation": (
        "Ligne 4 : la condition est i % 2 != 0 (impair) au lieu de "
        "i % 2 == 0 (pair). Pour ne PAS afficher les pairs, "
        "il faut sauter quand i est pair, donc la condition du if "
        "devrait etre i % 2 == 0."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    for (int i = 1; i <= 9; i++) {\n'
            '        if (i % 2 != 0) continue;\n'
            '        printf("%d ", i);\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "lines": [
            {"id": "1", "text": '#include <stdio.h>'},
            {"id": "2", "text": 'int main(void) {'},
            {"id": "3", "text": '    for (int i = 1; i <= 9; i++) {'},
            {"id": "4", "text": '        if (i % 2 != 0) continue;'},
            {"id": "5", "text": '        printf("%d ", i);'},
            {"id": "6", "text": '    }'},
            {"id": "7", "text": '    return 0;'},
            {"id": "8", "text": '}'},
        ],
        "correct_answer": 4,
    },
}

# ────────────────────────────────────────────────────────────
# Room 12 — MINI-BOSS #2 (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r12: ChallengeData = {
    "challenge_id": "z02_r12",
    "zone": 2,
    "room": 12,
    "is_boss": False,
    "is_mini_boss": True,
    "challenge_type": "sort_order",
    "title": "MINI-BOSS : La Boucle Infernale",
    "concept_tags": ["while", "if", "break", "boucle", "condition"],
    "difficulty": 3,
    "question_prompt": (
        "La Boucle Infernale a melange les lignes de ce programme ! "
        "Remets-les en ordre pour qu'il affiche la somme des entiers "
        "de 1 a 10 (55)."
    ),
    "hint": (
        "Initialise les variables, ecris la boucle while avec sa condition, "
        "le corps qui accumule et incremente, puis l'affichage final."
    ),
    "explanation": (
        "On initialise sum = 0 et i = 1, puis la boucle while(i <= 10) "
        "ajoute i a sum et incremente i. Apres la boucle, on affiche sum "
        "qui vaut 55."
    ),
    "payload": {
        "cards": [
            {"id": "c1", "text": "int sum = 0, i = 1;"},
            {"id": "c2", "text": "while (i <= 10) {"},
            {"id": "c3", "text": "    sum = sum + i;"},
            {"id": "c4", "text": "    i++;"},
            {"id": "c5", "text": "}"},
            {"id": "c6", "text": 'printf("%d", sum);'},
        ],
        "display_order": ["c4", "c6", "c2", "c1", "c5", "c3"],
        "correct_answer": ["c1", "c2", "c3", "c4", "c5", "c6"],
    },
}

# ────────────────────────────────────────────────────────────
# Room 13 — Expert (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r13: ChallengeData = {
    "challenge_id": "z02_r13",
    "zone": 2,
    "room": 13,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "La Salle des Boucles Imbriquees",
    "concept_tags": ["for", "boucle_imbriquee", "compteur"],
    "difficulty": 3,
    "question_prompt": (
        "Deux boucles for imbriquees tournent dans cette salle sombre. "
        "Combien d'etoiles (*) sont affichees au total ?"
    ),
    "hint": "La boucle externe tourne 3 fois, la boucle interne tourne 4 fois a chaque passage.",
    "explanation": (
        "La boucle externe (i) va de 0 a 2 : 3 iterations. "
        "Pour chaque i, la boucle interne (j) va de 0 a 3 : 4 iterations. "
        "Total : 3 x 4 = 12 etoiles."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int count = 0;\n'
            '    for (int i = 0; i < 3; i++) {\n'
            '        for (int j = 0; j < 4; j++) {\n'
            '            printf("*");\n'
            '            count++;\n'
            '        }\n'
            '    }\n'
            '    printf("\\n%d", count);\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "12",
    },
}

# ────────────────────────────────────────────────────────────
# Room 14 — Expert (difficulty 3)
# ────────────────────────────────────────────────────────────
_z02_r14: ChallengeData = {
    "challenge_id": "z02_r14",
    "zone": 2,
    "room": 14,
    "is_boss": False,
    "is_mini_boss": False,
    "challenge_type": "memory_map",
    "title": "Le Grimoire des Conditions Chainees",
    "concept_tags": ["switch", "case", "break", "fall_through"],
    "difficulty": 3,
    "question_prompt": (
        "Le grimoire contient un switch sans break dans certains cases. "
        "Quelle est la sortie du programme ? "
        "Attention au fall-through !"
    ),
    "hint": (
        "Sans break, l'execution \"tombe\" dans le case suivant "
        "(fall-through) jusqu'a rencontrer un break ou la fin du switch."
    ),
    "explanation": (
        "note vaut 2. On entre dans case 2, qui affiche \"B\". "
        "Il n'y a pas de break, donc on tombe dans case 3 "
        "et on affiche \"C\". Le break de case 3 arrete le switch. "
        "Resultat : BC."
    ),
    "payload": {
        "scenario": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int note = 2;\n'
            '    switch (note) {\n'
            '        case 1: printf("A"); break;\n'
            '        case 2: printf("B");\n'
            '        case 3: printf("C"); break;\n'
            '        default: printf("D");\n'
            '    }\n'
            '    return 0;\n'
            '}'
        ),
        "slots": [
            {"id": "s1", "label": "Sortie : B"},
            {"id": "s2", "label": "Sortie : BC"},
            {"id": "s3", "label": "Sortie : BCD"},
            {"id": "s4", "label": "Sortie : ABCD"},
        ],
        "correct_answer": "s2",
    },
}

# ────────────────────────────────────────────────────────────
# Room 15 — BOSS FINAL (difficulty 4)
# ────────────────────────────────────────────────────────────
_z02_r15: ChallengeData = {
    "challenge_id": "z02_r15",
    "zone": 2,
    "room": 15,
    "is_boss": True,
    "is_mini_boss": False,
    "challenge_type": "trace_value",
    "title": "BOSS : Le Golem Infinite Loop",
    "concept_tags": [
        "while", "for", "break", "continue",
        "condition", "boucle_imbriquee",
    ],
    "difficulty": 4,
    "question_prompt": (
        "Le Golem Infinite Loop te defie ! "
        "Ce programme combine boucle while, for, break et continue. "
        "Quelle est la valeur finale de total affichee par le printf ?"
    ),
    "hint": (
        "Suis l'execution pas a pas : la boucle externe while controle i, "
        "la boucle interne for controle j. Attention aux conditions "
        "break et continue."
    ),
    "explanation": (
        "i=0 : j parcourt 0..4. j==1 → continue (saute). j==3 → break "
        "(sort du for). total += j pour j=0,2 → total = 0+2 = 2. "
        "i=1 : j parcourt 0..4. j==1 → continue. j==3 → break. "
        "total += j pour j=0,2 → total = 2+0+2 = 4. "
        "i=2 : j parcourt 0..4. j==1 → continue. j==3 → break. "
        "total += j pour j=0,2 → total = 4+0+2 = 6. "
        "i=3 : condition while (i < 3) fausse, on sort. "
        "printf affiche 6."
    ),
    "payload": {
        "code": (
            '#include <stdio.h>\n'
            'int main(void) {\n'
            '    int total = 0;\n'
            '    int i = 0;\n'
            '    while (i < 3) {\n'
            '        for (int j = 0; j < 5; j++) {\n'
            '            if (j == 1) continue;\n'
            '            if (j == 3) break;\n'
            '            total += j;\n'
            '        }\n'
            '        i++;\n'
            '    }\n'
            '    printf("%d", total);\n'
            '    return 0;\n'
            '}'
        ),
        "correct_answer": "6",
    },
}

# ════════════════════════════════════════════════════════════
#  Export
# ════════════════════════════════════════════════════════════
ZONE_2_CHALLENGES: dict[str, ChallengeData] = {
    "z02_r01": _z02_r01,
    "z02_r02": _z02_r02,
    "z02_r03": _z02_r03,
    "z02_r04": _z02_r04,
    "z02_r05": _z02_r05,
    "z02_r06": _z02_r06,
    "z02_r07": _z02_r07,
    "z02_r08": _z02_r08,
    "z02_r09": _z02_r09,
    "z02_r10": _z02_r10,
    "z02_r11": _z02_r11,
    "z02_r12": _z02_r12,
    "z02_r13": _z02_r13,
    "z02_r14": _z02_r14,
    "z02_r15": _z02_r15,
}
