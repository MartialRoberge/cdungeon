"""
Zone 1 — Stack Village
Cours 1+2 : Algo, binaire, types, variables, printf/scanf, opérateurs, compilation.
15 salles : 4 intro → 3 consolidation → mini-boss → 3 maîtrise → mini-boss → 2 expert → boss.
"""

from app.content.challenge_types import ChallengeData

ZONE_1_CHALLENGES: dict[str, ChallengeData] = {

    # ──────────────────────────────────────────────
    # ROOMS 1-4  —  Introduction (difficulty 1)
    # ──────────────────────────────────────────────

    "z01_r01": {
        "challenge_id": "z01_r01",
        "zone": 1,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "L'Armurerie des Types",
        "concept_tags": ["types", "variables"],
        "difficulty": 1,
        "question_prompt": (
            "Bienvenue à Stack Village, aventurier ! Avant de partir en quête, "
            "tu dois ranger chaque artefact dans le bon coffre. "
            "Associe chaque valeur à son type C."
        ),
        "hint": (
            "int = nombre entier, float = décimal simple, "
            "double = décimal haute précision, char = un seul caractère entre apostrophes."
        ),
        "explanation": (
            "En C, chaque variable a un type strict. 42 est un entier (int), "
            "'Z' est un caractère (char), 3.14 un décimal simple (float) "
            "et 2.718281828 un décimal de haute précision (double)."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "42"},
                {"id": "v2", "display": "'Z'"},
                {"id": "v3", "display": "3.14f"},
                {"id": "v4", "display": "2.718281828"},
            ],
            "types": [
                {"id": "t1", "label": "int"},
                {"id": "t2", "label": "float"},
                {"id": "t3", "label": "double"},
                {"id": "t4", "label": "char"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t4", "v3": "t2", "v4": "t3"},
        },
    },

    "z01_r02": {
        "challenge_id": "z01_r02",
        "zone": 1,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "Le Parchemin Incomplet",
        "concept_tags": ["variables", "declaration"],
        "difficulty": 1,
        "question_prompt": (
            "Un vieux parchemin a été retrouvé dans la taverne du village, "
            "mais un mot a été effacé par l'humidité. "
            "Complète la déclaration pour stocker l'âge d'un aventurier."
        ),
        "hint": "Pour déclarer un nombre entier en C, on utilise le mot-clé 'int'.",
        "explanation": (
            "'int' est le type pour les nombres entiers en C. "
            "La syntaxe complète est : int nom_variable = valeur;"
        ),
        "payload": {
            "code_before": "#include <stdio.h>\n\nint main() {",
            "blank_label": "???",
            "code_after": " age = 20;\n    printf(\"Age : %d\\n\", age);\n    return 0;\n}",
            "options": ["int", "char", "void", "return"],
            "correct_answer": "int",
        },
    },

    "z01_r03": {
        "challenge_id": "z01_r03",
        "zone": 1,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "La Pierre de Calcul",
        "concept_tags": ["variables", "operateurs", "arithmetique"],
        "difficulty": 1,
        "question_prompt": (
            "Tu découvres une ancienne Pierre de Calcul gravée de runes. "
            "Suis l'exécution pas à pas : quelle est la valeur finale de 'tresor' ?"
        ),
        "hint": "Lis chaque ligne dans l'ordre. Chaque '=' remplace la valeur actuelle de la variable.",
        "explanation": (
            "tresor = 10, puis tresor = 10 + 5 = 15, puis tresor = 15 * 2 = 30. "
            "Les opérations se font dans l'ordre d'apparition."
        ),
        "payload": {
            "code": (
                "int tresor = 10;\n"
                "tresor = tresor + 5;\n"
                "tresor = tresor * 2;"
            ),
            "correct_answer": "30",
        },
    },

    "z01_r04": {
        "challenge_id": "z01_r04",
        "zone": 1,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Grimoire Maudit",
        "concept_tags": ["syntaxe", "point-virgule", "compilation"],
        "difficulty": 1,
        "question_prompt": (
            "Un apprenti sorcier a recopié un sort, mais il a fait une faute ! "
            "Le compilateur refuse de lancer le programme. "
            "Sur quelle ligne se cache le bug ?"
        ),
        "hint": "En C, chaque instruction doit se terminer par un point-virgule ;",
        "explanation": (
            "La ligne 3 oublie le point-virgule après la déclaration. "
            "Sans ';', le compilateur ne sait pas où finit l'instruction."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "int main() {\n"
                "    int potions = 5\n"
                '    printf("Potions : %d\\n", potions);\n'
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "#include <stdio.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": "    int potions = 5"},
                {"id": "4", "text": '    printf("Potions : %d\\n", potions);'},
                {"id": "5", "text": "    return 0;"},
                {"id": "6", "text": "}"},
            ],
            "correct_answer": 3,
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 5-7  —  Consolidation (difficulty 1,2,2)
    # ──────────────────────────────────────────────

    "z01_r05": {
        "challenge_id": "z01_r05",
        "zone": 1,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Rituel de Compilation",
        "concept_tags": ["compilation", "workflow", "gcc"],
        "difficulty": 1,
        "question_prompt": (
            "Pour invoquer un programme en C, il faut suivre un rituel précis. "
            "Remets les étapes de la compilation dans le bon ordre !"
        ),
        "hint": "On écrit d'abord le code, ensuite on le compile, puis on exécute le résultat.",
        "explanation": (
            "Le cycle de développement en C : "
            "1) Écrire le code source (.c), "
            "2) Compiler avec gcc, "
            "3) Obtenir l'exécutable, "
            "4) Lancer le programme."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "Écrire le code dans main.c"},
                {"id": "c2", "text": "Compiler avec gcc main.c -o main"},
                {"id": "c3", "text": "Obtenir le fichier exécutable 'main'"},
                {"id": "c4", "text": "Lancer le programme avec ./main"},
            ],
            "display_order": ["c4", "c2", "c1", "c3"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    "z01_r06": {
        "challenge_id": "z01_r06",
        "zone": 1,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Carte des Coffres",
        "concept_tags": ["variables", "memoire", "types"],
        "difficulty": 2,
        "question_prompt": (
            "Chaque variable est rangée dans un coffre en mémoire. "
            "Après l'exécution de ce code, quel coffre contient la variable 'bouclier' ?"
        ),
        "hint": (
            "Les variables locales sont empilées sur la stack. "
            "Un int occupe 4 octets. La première variable est à l'adresse la plus basse."
        ),
        "explanation": (
            "Après déclaration, epee est en 0x100 (valeur 7), "
            "bouclier en 0x104 (valeur 3), et armure en 0x108 (valeur 12). "
            "Chaque int occupe 4 octets consécutifs sur la stack."
        ),
        "payload": {
            "scenario": (
                "int epee = 7;\n"
                "int bouclier = 3;\n"
                "int armure = 12;"
            ),
            "slots": [
                {"id": "s1", "label": "0x100 — epee (7)"},
                {"id": "s2", "label": "0x104 — bouclier (3)"},
                {"id": "s3", "label": "0x108 — armure (12)"},
            ],
            "correct_answer": "s2",
        },
    },

    "z01_r07": {
        "challenge_id": "z01_r07",
        "zone": 1,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "L'Incantation printf",
        "concept_tags": ["printf", "format_specifiers"],
        "difficulty": 2,
        "question_prompt": (
            "Le mage de Stack Village veut afficher le prix d'une potion. "
            "Quel spécificateur de format doit-il utiliser dans printf pour un float ?"
        ),
        "hint": (
            "%d pour int, %f pour float/double, %c pour char, %s pour les chaînes."
        ),
        "explanation": (
            "Le spécificateur %f est utilisé pour afficher un float ou un double. "
            "%d est réservé aux entiers, %c aux caractères, %s aux chaînes."
        ),
        "payload": {
            "code_before": (
                '#include <stdio.h>\n\n'
                'int main() {\n'
                '    float prix = 9.99;\n'
                '    printf("Potion : '
            ),
            "blank_label": "???",
            "code_after": (
                '\\n", prix);\n'
                '    return 0;\n'
                '}'
            ),
            "options": ["%d", "%f", "%c", "%s"],
            "correct_answer": "%f",
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 8  —  MINI-BOSS #1 (difficulty 2)
    # ──────────────────────────────────────────────

    "z01_r08": {
        "challenge_id": "z01_r08",
        "zone": 1,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "trace_value",
        "title": "MINI-BOSS : Le Garde des Variables",
        "concept_tags": ["variables", "operateurs", "affectation", "arithmetique"],
        "difficulty": 2,
        "question_prompt": (
            "Le Garde des Variables te barre la route ! "
            "Pour passer, tu dois prouver que tu sais tracer l'exécution d'un programme. "
            "Quelle est la valeur affichée par le printf ?"
        ),
        "hint": (
            "Attention à l'ordre des opérations : "
            "la division entière entre deux int tronque le résultat (pas d'arrondi)."
        ),
        "explanation": (
            "a = 17, b = 5. c = 17 / 5 = 3 (division entière, pas 3.4). "
            "d = 17 % 5 = 2 (reste de la division). "
            "resultat = 3 + 2 = 5. Le printf affiche 5."
        ),
        "payload": {
            "code": (
                "int a = 17;\n"
                "int b = 5;\n"
                "int c = a / b;\n"
                "int d = a % b;\n"
                "int resultat = c + d;\n"
                'printf("%d", resultat);'
            ),
            "correct_answer": "5",
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 9-11  —  Maîtrise (difficulty 2,2,3)
    # ──────────────────────────────────────────────

    "z01_r09": {
        "challenge_id": "z01_r09",
        "zone": 1,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Piège du Format",
        "concept_tags": ["printf", "format_specifiers", "types"],
        "difficulty": 2,
        "question_prompt": (
            "Un piège magique a corrompu ce programme ! "
            "Le code compile, mais l'affichage est complètement faux. "
            "Sur quelle ligne se trouve l'erreur ?"
        ),
        "hint": (
            "Vérifie que chaque spécificateur de format correspond "
            "au type de la variable affichée. %d attend un int, %f attend un float/double."
        ),
        "explanation": (
            "La ligne 4 utilise %d pour afficher un float. "
            "Il faut utiliser %f pour les nombres à virgule. "
            "Le compilateur ne signale pas toujours cette erreur, mais le résultat sera aberrant."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "int main() {\n"
                "    float temperature = 36.6;\n"
                '    printf("Temp : %d\\n", temperature);\n'
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "#include <stdio.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": "    float temperature = 36.6;"},
                {"id": "4", "text": '    printf("Temp : %d\\n", temperature);'},
                {"id": "5", "text": "    return 0;"},
                {"id": "6", "text": "}"},
            ],
            "correct_answer": 4,
        },
    },

    "z01_r10": {
        "challenge_id": "z01_r10",
        "zone": 1,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Protocole scanf",
        "concept_tags": ["scanf", "variables", "entrees_sorties"],
        "difficulty": 2,
        "question_prompt": (
            "Pour demander un nombre à l'utilisateur, il faut lancer un rituel "
            "en plusieurs étapes. Remets ces lignes dans le bon ordre pour créer "
            "un programme qui lit un entier et l'affiche."
        ),
        "hint": (
            "D'abord on déclare la variable, puis on demande la saisie (scanf), "
            "puis on affiche le résultat (printf). N'oublie pas le & devant la variable dans scanf !"
        ),
        "explanation": (
            "Le bon ordre : 1) Déclarer la variable 'n', "
            "2) Afficher un message d'invitation, "
            "3) Lire la saisie avec scanf (le & passe l'adresse de n), "
            "4) Afficher la valeur lue."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "int n;"},
                {"id": "c2", "text": 'printf("Entrez un nombre : ");'},
                {"id": "c3", "text": 'scanf("%d", &n);'},
                {"id": "c4", "text": 'printf("Vous avez saisi : %d\\n", n);'},
            ],
            "display_order": ["c3", "c4", "c1", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    "z01_r11": {
        "challenge_id": "z01_r11",
        "zone": 1,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Marché aux Conversions",
        "concept_tags": ["binaire", "representation", "conversion"],
        "difficulty": 3,
        "question_prompt": (
            "Au marché de Stack Village, les marchands utilisent différentes "
            "représentations des nombres. Associe chaque valeur à sa représentation décimale."
        ),
        "hint": (
            "En binaire : 1010 = 8+2 = 10. "
            "En hexadécimal : 0xFF = 15*16+15 = 255. "
            "En octal : 017 = 1*8+7 = 15."
        ),
        "explanation": (
            "0b1010 en binaire = 10 en décimal. "
            "0xFF en hexadécimal = 255 en décimal. "
            "017 en octal = 15 en décimal. "
            "42 est déjà en décimal."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "0b1010"},
                {"id": "v2", "display": "0xFF"},
                {"id": "v3", "display": "017"},
                {"id": "v4", "display": "42"},
            ],
            "types": [
                {"id": "t1", "label": "10"},
                {"id": "t2", "label": "255"},
                {"id": "t3", "label": "15"},
                {"id": "t4", "label": "42"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 12  —  MINI-BOSS #2 (difficulty 3)
    # ──────────────────────────────────────────────

    "z01_r12": {
        "challenge_id": "z01_r12",
        "zone": 1,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "memory_map",
        "title": "MINI-BOSS : La Sentinelle du Cast",
        "concept_tags": ["types", "cast", "conversion", "memoire"],
        "difficulty": 3,
        "question_prompt": (
            "La Sentinelle du Cast te défie ! Après l'exécution de ce code, "
            "quelle est la valeur stockée dans la variable 'resultat' ? "
            "Choisis le bon emplacement mémoire."
        ),
        "hint": (
            "Quand on divise deux int en C, le résultat est un int (troncature). "
            "Même si la variable de destination est un float, la division est déjà faite en entier."
        ),
        "explanation": (
            "7 / 2 donne 3 (division entière entre deux int), pas 3.5. "
            "Le résultat 3 est ensuite converti en float : resultat vaut 3.0. "
            "Pour obtenir 3.5, il faudrait écrire 7.0 / 2 ou (float)7 / 2."
        ),
        "payload": {
            "scenario": (
                "int a = 7;\n"
                "int b = 2;\n"
                "float resultat = a / b;"
            ),
            "slots": [
                {"id": "s1", "label": "resultat = 3.5"},
                {"id": "s2", "label": "resultat = 3.0"},
                {"id": "s3", "label": "resultat = 4.0"},
                {"id": "s4", "label": "resultat = 0.0"},
            ],
            "correct_answer": "s2",
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 13-14  —  Expert (difficulty 3,3)
    # ──────────────────────────────────────────────

    "z01_r13": {
        "challenge_id": "z01_r13",
        "zone": 1,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Donjon du scanf",
        "concept_tags": ["scanf", "adresse", "operateur_&"],
        "difficulty": 3,
        "question_prompt": (
            "Un aventurier imprudent a écrit ce programme, mais il crashe à l'exécution ! "
            "Le compilateur n'a rien dit, pourtant quelque chose de dangereux se cache. "
            "Trouve la ligne fautive."
        ),
        "hint": (
            "scanf a besoin de l'adresse de la variable pour y écrire. "
            "L'opérateur & donne l'adresse d'une variable."
        ),
        "explanation": (
            "La ligne 5 oublie le & devant 'age' dans scanf. "
            "Sans &, scanf reçoit la valeur de age (non initialisée) au lieu de son adresse, "
            "provoquant un comportement indéfini (crash probable)."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "int main() {\n"
                "    int age;\n"
                '    printf("Votre age : ");\n'
                '    scanf("%d", age);\n'
                '    printf("Vous avez %d ans\\n", age);\n'
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "#include <stdio.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": "    int age;"},
                {"id": "4", "text": '    printf("Votre age : ");'},
                {"id": "5", "text": '    scanf("%d", age);'},
                {"id": "6", "text": '    printf("Vous avez %d ans\\n", age);'},
                {"id": "7", "text": "    return 0;"},
                {"id": "8", "text": "}"},
            ],
            "correct_answer": 5,
        },
    },

    "z01_r14": {
        "challenge_id": "z01_r14",
        "zone": 1,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "L'Épreuve des Opérateurs",
        "concept_tags": ["operateurs", "priorite", "cast", "arithmetique"],
        "difficulty": 3,
        "question_prompt": (
            "Un piège complexe se dresse devant toi. "
            "Ce code mélange opérateurs et conversions de type. "
            "Quelle valeur est affichée par le printf ?"
        ),
        "hint": (
            "Attention à la priorité des opérateurs : * et / avant + et -. "
            "Et attention au cast : (float) force la conversion AVANT l'opération."
        ),
        "explanation": (
            "Étape par étape : a = 10, b = 3. "
            "c = (float)a / b = 10.0 / 3 = 3.333... "
            "d = a % b = 10 % 3 = 1. "
            "e = (int)c + d = (int)3.333 + 1 = 3 + 1 = 4. "
            "Le printf affiche 4."
        ),
        "payload": {
            "code": (
                "int a = 10, b = 3;\n"
                "float c = (float)a / b;\n"
                "int d = a % b;\n"
                "int e = (int)c + d;\n"
                'printf("%d", e);'
            ),
            "correct_answer": "4",
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 15  —  BOSS FINAL (difficulty 3)
    # ──────────────────────────────────────────────

    "z01_r15": {
        "challenge_id": "z01_r15",
        "zone": 1,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "BOSS : Le Golem des Types",
        "concept_tags": [
            "types", "variables", "printf", "scanf",
            "operateurs", "compilation", "binaire",
        ],
        "difficulty": 3,
        "question_prompt": (
            "Le Golem des Types garde la sortie de Stack Village ! "
            "Pour le vaincre, remets dans l'ordre ce programme complet "
            "qui lit deux entiers, calcule leur moyenne flottante, et l'affiche. "
            "Chaque carte est une ligne — une seule erreur et le Golem t'écrase !"
        ),
        "hint": (
            "Un programme C suit toujours la même structure : "
            "includes, main, déclarations, saisies, calcul, affichage, return. "
            "Pour une moyenne flottante de deux entiers, il faut un cast en (float)."
        ),
        "explanation": (
            "Le programme complet : "
            "1) #include pour printf/scanf, "
            "2) main, "
            "3) déclarer les variables (a, b, et la moyenne), "
            "4) lire les deux entiers, "
            "5) calculer la moyenne avec un cast float pour garder les décimales, "
            "6) afficher le résultat, "
            "7) return et accolade fermante. "
            "Ce programme combine TOUS les concepts de la Zone 1 !"
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "#include <stdio.h>"},
                {"id": "c2", "text": "int main() {"},
                {"id": "c3", "text": "    int a, b;"},
                {"id": "c4", "text": '    scanf("%d %d", &a, &b);'},
                {"id": "c5", "text": "    float moy = (float)(a + b) / 2;"},
                {"id": "c6", "text": '    printf("Moyenne : %f\\n", moy);'},
                {"id": "c7", "text": "    return 0;\n}"},
            ],
            "display_order": ["c5", "c3", "c7", "c1", "c6", "c4", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4", "c5", "c6", "c7"],
        },
    },
}
