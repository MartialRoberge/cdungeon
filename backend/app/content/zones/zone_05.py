"""
Zone 5 — Pointer Abyss (L'Abysse des Pointeurs)
Cours 6 : Adresses, &, pointeurs, *, passage par adresse,
           pointeurs et tableaux, arithmétique de pointeurs, ->, NULL

15 challenges : rooms 1-4 intro, 5-7 consolidation, 8 mini-boss,
                9-11 maîtrise, 12 mini-boss, 13-14 expert, 15 boss
Difficulté : 2,2,2,3 | 3,3,3 | 3 | 3,3,4 | 4 | 4,4 | 5
"""

from app.content.challenge_types import ChallengeData

ZONE_5_CHALLENGES: dict[str, ChallengeData] = {

    # ================================================================
    # ROOMS 1-4 — INTRODUCTION (difficulté 2, 2, 2, 3)
    # ================================================================

    "z05_r01": {
        "challenge_id": "z05_r01",
        "zone": 5,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "Première Descente dans l'Abysse",
        "concept_tags": ["adresses", "&"],
        "difficulty": 2,
        "question_prompt": (
            "L'aventurier déclare `int x = 42;` dans le gouffre. "
            "L'opérateur & révèle l'adresse d'une variable. "
            "Où se cache la valeur 42 en mémoire ?"
        ),
        "hint": "L'opérateur & (« adresse de ») renvoie l'emplacement mémoire d'une variable.",
        "explanation": (
            "Quand on écrit int x = 42;, le compilateur réserve un emplacement mémoire "
            "(par ex. 0x1000). &x donne cette adresse. La valeur 42 est stockée à cet endroit."
        ),
        "payload": {
            "scenario": (
                "int x = 42;\n"
                "printf(\"%p\", &x);\n"
                "// La mémoire ressemble à :\n"
                "// [0x0FF8] = ???\n"
                "// [0x1000] = 42   ← &x\n"
                "// [0x1008] = ???"
            ),
            "slots": [
                {"id": "s1", "label": "0x0FF8 — zone inconnue"},
                {"id": "s2", "label": "0x1000 — adresse de x"},
                {"id": "s3", "label": "0x1008 — zone inconnue"},
            ],
            "correct_answer": "s2",
        },
    },

    "z05_r02": {
        "challenge_id": "z05_r02",
        "zone": 5,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Coffre des Symboles",
        "concept_tags": ["pointeurs", "&", "*"],
        "difficulty": 2,
        "question_prompt": (
            "Associe chaque expression C à ce qu'elle représente. "
            "Les symboles * et & sont les clés de l'abysse !"
        ),
        "hint": "& donne l'adresse, * suit le pointeur pour lire la valeur pointée.",
        "explanation": (
            "int x = 5; int *p = &x; → p contient l'adresse de x. "
            "*p vaut 5 (la valeur pointée). &x est l'adresse de x. &p est l'adresse du pointeur lui-même."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "x"},
                {"id": "v2", "display": "&x"},
                {"id": "v3", "display": "p"},
                {"id": "v4", "display": "*p"},
            ],
            "types": [
                {"id": "t1", "label": "La valeur 5"},
                {"id": "t2", "label": "L'adresse de x"},
                {"id": "t3", "label": "Un pointeur contenant l'adresse de x"},
                {"id": "t4", "label": "La valeur pointée par p (= 5)"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    "z05_r03": {
        "challenge_id": "z05_r03",
        "zone": 5,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "La Formule du Pointeur",
        "concept_tags": ["pointeurs", "declaration"],
        "difficulty": 2,
        "question_prompt": (
            "Complète le code pour déclarer un pointeur vers l'entier n. "
            "Le gouffre n'attend pas !"
        ),
        "hint": "Pour déclarer un pointeur sur int, on écrit int *nom = &variable;",
        "explanation": (
            "int *p déclare un pointeur sur int. On l'initialise avec &n "
            "pour qu'il pointe vers n. Le * dans la déclaration indique que p est un pointeur."
        ),
        "payload": {
            "code_before": "int n = 10;",
            "blank_label": "???",
            "code_after": " = &n;\nprintf(\"%d\", *ptr);  // Affiche 10",
            "options": ["int ptr", "int *ptr", "int &ptr", "*int ptr"],
            "correct_answer": "int *ptr",
        },
    },

    "z05_r04": {
        "challenge_id": "z05_r04",
        "zone": 5,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Miroir Déréférencé",
        "concept_tags": ["pointeurs", "*", "dereferencement"],
        "difficulty": 3,
        "question_prompt": (
            "Suis l'exécution du code pas à pas. "
            "Que vaut x à la fin, après que le pointeur a modifié sa valeur ?"
        ),
        "hint": "*p = valeur modifie la variable pointée par p, pas p lui-même.",
        "explanation": (
            "p pointe vers x. Quand on écrit *p = 20, on modifie x à travers le pointeur. "
            "Puis *p += 5 ajoute 5 à x. Donc x vaut 25."
        ),
        "payload": {
            "code": (
                "int x = 10;\n"
                "int *p = &x;\n"
                "*p = 20;\n"
                "*p += 5;\n"
                "printf(\"%d\", x);"
            ),
            "correct_answer": "25",
        },
    },

    # ================================================================
    # ROOMS 5-7 — CONSOLIDATION (difficulté 3, 3, 3)
    # ================================================================

    "z05_r05": {
        "challenge_id": "z05_r05",
        "zone": 5,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "Le Passage par Adresse",
        "concept_tags": ["passage_par_adresse", "pointeurs", "fonctions"],
        "difficulty": 3,
        "question_prompt": (
            "La fonction doubler(int *p) multiplie par 2 la valeur pointée. "
            "On appelle doubler(&val). "
            "Dans quel slot mémoire se trouve la valeur après l'appel ?"
        ),
        "hint": (
            "Passage par adresse = on envoie &val à la fonction. "
            "La fonction modifie directement la case mémoire de val."
        ),
        "explanation": (
            "Quand on passe &val, la fonction reçoit l'adresse de val. "
            "*p *= 2 modifie val directement en mémoire. "
            "val passe de 7 à 14 et reste à son emplacement d'origine."
        ),
        "payload": {
            "scenario": (
                "void doubler(int *p) { *p *= 2; }\n"
                "int main() {\n"
                "    int val = 7;\n"
                "    doubler(&val);\n"
                "    // Mémoire après l'appel :\n"
                "    // [0x2000] val = 14\n"
                "    // [0x2008] copie locale (détruite)\n"
                "    // [0x2010] autre zone\n"
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "0x2000 — val = 14 (modifiée par la fonction)"},
                {"id": "s2", "label": "0x2008 — copie locale de p (détruite après l'appel)"},
                {"id": "s3", "label": "0x2010 — zone mémoire non concernée"},
            ],
            "correct_answer": "s1",
        },
    },

    "z05_r06": {
        "challenge_id": "z05_r06",
        "zone": 5,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Piège du Pointeur Sauvage",
        "concept_tags": ["pointeurs", "NULL", "initialisation"],
        "difficulty": 3,
        "question_prompt": (
            "Ce code provoque un crash à l'exécution. "
            "Trouve la ligne maudite qui déréférence un pointeur non initialisé !"
        ),
        "hint": "Un pointeur déclaré sans initialisation contient une adresse aléatoire (garbage).",
        "explanation": (
            "La ligne 2 déclare int *p; sans l'initialiser. "
            "À la ligne 3, *p = 42 tente d'écrire à une adresse aléatoire → crash (segfault). "
            "Il faudrait écrire int *p = &x; ou int *p = NULL; d'abord."
        ),
        "payload": {
            "code": (
                "int x = 0;\n"
                "int *p;\n"
                "*p = 42;\n"
                "printf(\"%d\", *p);"
            ),
            "lines": [
                {"id": "1", "text": "int x = 0;"},
                {"id": "2", "text": "int *p;"},
                {"id": "3", "text": "*p = 42;"},
                {"id": "4", "text": "printf(\"%d\", *p);"},
            ],
            "correct_answer": 3,
        },
    },

    "z05_r07": {
        "challenge_id": "z05_r07",
        "zone": 5,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "L'Escalier des Pointeurs",
        "concept_tags": ["pointeurs", "&", "*", "declaration"],
        "difficulty": 3,
        "question_prompt": (
            "Remets les étapes dans l'ordre pour créer un pointeur, "
            "l'initialiser et modifier la variable pointée."
        ),
        "hint": "D'abord on déclare la variable, puis le pointeur, puis on l'affecte, puis on déréférence.",
        "explanation": (
            "1) Déclarer la variable cible. 2) Déclarer le pointeur. "
            "3) Affecter l'adresse de la variable au pointeur. 4) Utiliser *p pour modifier la valeur."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "int x = 5;"},
                {"id": "c2", "text": "int *p;"},
                {"id": "c3", "text": "p = &x;"},
                {"id": "c4", "text": "*p = 10;"},
            ],
            "display_order": ["c3", "c1", "c4", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    # ================================================================
    # ROOM 8 — MINI-BOSS 1 (difficulté 3)
    # ================================================================

    "z05_r08": {
        "challenge_id": "z05_r08",
        "zone": 5,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "memory_map",
        "title": "MINI-BOSS : Le Fantôme de l'Adresse",
        "concept_tags": ["pointeurs", "passage_par_adresse", "&", "*"],
        "difficulty": 3,
        "question_prompt": (
            "Le Fantôme de l'Adresse a jeté un sort sur la mémoire ! "
            "La fonction echanger(int *a, int *b) échange les valeurs de deux variables. "
            "Après echanger(&x, &y), x vaut 20 et y vaut 10. "
            "Quel slot montre l'état correct de la mémoire APRÈS l'échange ?"
        ),
        "hint": (
            "La fonction reçoit les adresses de x et y. "
            "Elle peut modifier les valeurs originales via *a et *b."
        ),
        "explanation": (
            "echanger reçoit &x et &y. Avec int tmp = *a; *a = *b; *b = tmp; "
            "les valeurs sont échangées en mémoire. x passe de 10 à 20, y de 20 à 10. "
            "C'est LE cas d'usage classique du passage par adresse."
        ),
        "payload": {
            "scenario": (
                "void echanger(int *a, int *b) {\n"
                "    int tmp = *a;\n"
                "    *a = *b;\n"
                "    *b = tmp;\n"
                "}\n"
                "int main() {\n"
                "    int x = 10, y = 20;\n"
                "    echanger(&x, &y);\n"
                "    // État mémoire après l'appel ?\n"
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "x = 10, y = 20 (rien n'a changé)"},
                {"id": "s2", "label": "x = 20, y = 10 (valeurs échangées)"},
                {"id": "s3", "label": "x = 20, y = 20 (copie partielle)"},
            ],
            "correct_answer": "s2",
        },
    },

    # ================================================================
    # ROOMS 9-11 — MAÎTRISE (difficulté 3, 3, 4)
    # ================================================================

    "z05_r09": {
        "challenge_id": "z05_r09",
        "zone": 5,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Tableau et son Ombre",
        "concept_tags": ["pointeurs", "tableaux", "pointeurs_et_tableaux"],
        "difficulty": 3,
        "question_prompt": (
            "En C, le nom d'un tableau est un pointeur vers son premier élément. "
            "Que vaut *(tab + 2) ?"
        ),
        "hint": "tab + 2 avance de 2 éléments. *(tab + 2) est équivalent à tab[2].",
        "explanation": (
            "tab pointe vers tab[0] = 10. tab + 1 → tab[1] = 20. tab + 2 → tab[2] = 30. "
            "*(tab + 2) déréférence cette adresse et donne 30. "
            "C'est exactement la même chose que tab[2]."
        ),
        "payload": {
            "code": (
                "int tab[] = {10, 20, 30, 40, 50};\n"
                "printf(\"%d\", *(tab + 2));"
            ),
            "correct_answer": "30",
        },
    },

    "z05_r10": {
        "challenge_id": "z05_r10",
        "zone": 5,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "L'Incantation Arithmétique",
        "concept_tags": ["arithmetique_pointeurs", "pointeurs", "tableaux"],
        "difficulty": 3,
        "question_prompt": (
            "Complète le code pour afficher le 4ème élément du tableau "
            "en utilisant l'arithmétique de pointeurs."
        ),
        "hint": "Pour accéder au 4ème élément (index 3), on avance le pointeur de 3 positions.",
        "explanation": (
            "p + 3 pointe vers le 4ème élément (index 3). "
            "*(p + 3) déréférence cette adresse et donne la valeur 40. "
            "En C, tab[i] est strictement équivalent à *(tab + i)."
        ),
        "payload": {
            "code_before": "int tab[] = {10, 20, 30, 40, 50};\nint *p = tab;\nprintf(\"%d\", ",
            "blank_label": "???",
            "code_after": ");  // Affiche 40",
            "options": ["*(p + 3)", "*(p + 4)", "*p + 3", "p[4]"],
            "correct_answer": "*(p + 3)",
        },
    },

    "z05_r11": {
        "challenge_id": "z05_r11",
        "zone": 5,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Carte des Adresses",
        "concept_tags": ["arithmetique_pointeurs", "pointeurs", "sizeof"],
        "difficulty": 4,
        "question_prompt": (
            "Un int occupe 4 octets. Si tab est à l'adresse 0x3000, "
            "à quelle adresse se trouve tab[3] ?"
        ),
        "hint": (
            "L'arithmétique de pointeurs avance de sizeof(type) octets par incrément. "
            "Pour int, chaque +1 avance de 4 octets."
        ),
        "explanation": (
            "tab est à 0x3000. Chaque int fait 4 octets. "
            "tab[1] → 0x3004, tab[2] → 0x3008, tab[3] → 0x300C. "
            "L'arithmétique de pointeurs gère automatiquement la taille du type."
        ),
        "payload": {
            "scenario": (
                "int tab[5] = {10, 20, 30, 40, 50};\n"
                "// sizeof(int) = 4 octets\n"
                "// tab est à l'adresse 0x3000\n"
                "// Quelle est l'adresse de tab[3] ?"
            ),
            "slots": [
                {"id": "s1", "label": "0x3003 (base + 3 octets)"},
                {"id": "s2", "label": "0x300C (base + 12 octets = 3 × 4)"},
                {"id": "s3", "label": "0x3010 (base + 16 octets = 4 × 4)"},
                {"id": "s4", "label": "0x3030 (base + 48 octets)"},
            ],
            "correct_answer": "s2",
        },
    },

    # ================================================================
    # ROOM 12 — MINI-BOSS 2 (difficulté 4)
    # ================================================================

    "z05_r12": {
        "challenge_id": "z05_r12",
        "zone": 5,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "trace_value",
        "title": "MINI-BOSS : L'Arithméticien des Pointeurs",
        "concept_tags": ["arithmetique_pointeurs", "pointeurs", "tableaux", "boucle"],
        "difficulty": 4,
        "question_prompt": (
            "L'Arithméticien parcourt un tableau avec un pointeur. "
            "Que vaut sum à la fin de la boucle ?"
        ),
        "hint": (
            "Le pointeur p avance d'un élément à chaque itération. "
            "La boucle additionne toutes les valeurs pointées."
        ),
        "explanation": (
            "p démarre à tab[0]. La boucle : *p=1 → sum=1, *p=2 → sum=3, "
            "*p=3 → sum=6, *p=4 → sum=10, *p=5 → sum=15. "
            "p avance avec p++ (équivalent à p = p + 1), ce qui saute de sizeof(int) octets."
        ),
        "payload": {
            "code": (
                "int tab[] = {1, 2, 3, 4, 5};\n"
                "int *p = tab;\n"
                "int sum = 0;\n"
                "for (int i = 0; i < 5; i++) {\n"
                "    sum += *p;\n"
                "    p++;\n"
                "}\n"
                "printf(\"%d\", sum);"
            ),
            "correct_answer": "15",
        },
    },

    # ================================================================
    # ROOMS 13-14 — EXPERT (difficulté 4, 4)
    # ================================================================

    "z05_r13": {
        "challenge_id": "z05_r13",
        "zone": 5,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "La Flèche Maudite (->)",
        "concept_tags": ["pointeurs", "structures", "->"],
        "difficulty": 4,
        "question_prompt": (
            "On a un pointeur vers une structure Guerrier. "
            "Complète le code pour accéder au champ 'pv' via le pointeur."
        ),
        "hint": (
            "L'opérateur -> permet d'accéder à un champ de structure via un pointeur. "
            "ptr->champ est équivalent à (*ptr).champ."
        ),
        "explanation": (
            "ptr->pv est la syntaxe pour accéder au champ pv via un pointeur. "
            "C'est un raccourci pour (*ptr).pv. L'opérateur -> combine "
            "le déréférencement * et l'accès au champ . en une seule opération."
        ),
        "payload": {
            "code_before": (
                "typedef struct { int pv; int atk; } Guerrier;\n"
                "Guerrier hero = {100, 25};\n"
                "Guerrier *ptr = &hero;"
            ),
            "blank_label": "???",
            "code_after": " = 80;\nprintf(\"%d\", hero.pv);  // Affiche 80",
            "options": ["ptr.pv", "ptr->pv", "*ptr.pv", "ptr*pv"],
            "correct_answer": "ptr->pv",
        },
    },

    "z05_r14": {
        "challenge_id": "z05_r14",
        "zone": 5,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Sanctuaire de NULL",
        "concept_tags": ["pointeurs", "NULL", "segfault"],
        "difficulty": 4,
        "question_prompt": (
            "Ce code crashe à l'exécution avec un segfault. "
            "Trouve la ligne fatale qui déréférence un pointeur NULL !"
        ),
        "hint": "Un pointeur NULL ne pointe vers rien. Le déréférencer (avec *) provoque un crash.",
        "explanation": (
            "À la ligne 3, p est NULL (il ne pointe vers rien). "
            "La ligne 4 tente *p = 42, ce qui déréférence NULL → segfault. "
            "Il faut toujours vérifier if (p != NULL) avant de déréférencer."
        ),
        "payload": {
            "code": (
                "int x = 10;\n"
                "int *p = &x;\n"
                "p = NULL;\n"
                "*p = 42;\n"
                "printf(\"%d\", x);"
            ),
            "lines": [
                {"id": "1", "text": "int x = 10;"},
                {"id": "2", "text": "int *p = &x;"},
                {"id": "3", "text": "p = NULL;"},
                {"id": "4", "text": "*p = 42;"},
                {"id": "5", "text": "printf(\"%d\", x);"},
            ],
            "correct_answer": 4,
        },
    },

    # ================================================================
    # ROOM 15 — BOSS (difficulté 5)
    # ================================================================

    "z05_r15": {
        "challenge_id": "z05_r15",
        "zone": 5,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "BOSS : Le Dragon Segfault",
        "concept_tags": [
            "pointeurs", "passage_par_adresse", "arithmetique_pointeurs",
            "NULL", "->", "tableaux",
        ],
        "difficulty": 5,
        "question_prompt": (
            "Le Dragon Segfault te lance un défi ultime ! "
            "Analyse ce code complexe : une fonction reçoit un pointeur vers un tableau "
            "et modifie ses éléments via l'arithmétique de pointeurs. "
            "Quel slot montre l'état FINAL correct du tableau en mémoire ?"
        ),
        "hint": (
            "La fonction reçoit l'adresse du tableau. "
            "*(arr + i) *= 2 double chaque élément. "
            "Trace chaque itération : 1→2, 2→4, 3→6, 4→8."
        ),
        "explanation": (
            "La fonction modifier reçoit le pointeur arr (= adresse du tableau). "
            "La boucle parcourt les 4 éléments avec *(arr + i) *= 2, "
            "ce qui double chaque valeur : {1,2,3,4} → {2,4,6,8}. "
            "Le passage par pointeur modifie le tableau original en mémoire. "
            "Le Dragon Segfault est vaincu — tu maîtrises les pointeurs !"
        ),
        "payload": {
            "scenario": (
                "void modifier(int *arr, int n) {\n"
                "    for (int i = 0; i < n; i++)\n"
                "        *(arr + i) *= 2;\n"
                "}\n"
                "int main() {\n"
                "    int tab[] = {1, 2, 3, 4};\n"
                "    modifier(tab, 4);\n"
                "    // État du tableau après l'appel ?\n"
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "tab = {1, 2, 3, 4} — inchangé (passage par valeur)"},
                {"id": "s2", "label": "tab = {2, 4, 6, 8} — chaque élément doublé"},
                {"id": "s3", "label": "tab = {2, 2, 3, 4} — seul le premier doublé"},
                {"id": "s4", "label": "tab = {1, 4, 9, 16} — chaque élément au carré"},
            ],
            "correct_answer": "s2",
        },
    },
}
