"""
Zone 7 — Heap Wastes
Cours 8 : Stack vs heap, malloc, sizeof, free, calloc, realloc,
          memory leaks, dangling pointers, double free, matrices dynamiques.

15 challenges (rooms 1-15).
  Rooms  1-4  : introduction           (diff 2,3,3,3)
  Rooms  5-7  : consolidation          (diff 3,3,3)
  Room   8    : mini-boss 1            (diff 4)
  Rooms  9-11 : maitrise               (diff 3,4,4)
  Room  12    : mini-boss 2            (diff 4)
  Rooms 13-14 : expert                 (diff 4,5)
  Room  15    : boss                   (diff 5)
"""

from app.content.challenge_types import ChallengeData

ZONE_7_CHALLENGES: dict[str, ChallengeData] = {

    # ──────────────────────────────────────────────
    # ROOMS 1-4 : INTRODUCTION
    # ──────────────────────────────────────────────

    "z07_r01": {
        "challenge_id": "z07_r01",
        "zone": 7,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Les Deux Royaumes de la Memoire",
        "concept_tags": ["stack", "heap", "memoire"],
        "difficulty": 2,
        "question_prompt": (
            "Dans les Heap Wastes, la memoire est divisee en deux royaumes. "
            "Associe chaque description a la bonne zone memoire."
        ),
        "hint": (
            "La stack est geree automatiquement (variables locales). "
            "Le heap est gere manuellement (malloc/free)."
        ),
        "explanation": (
            "La stack stocke les variables locales et les appels de fonctions — "
            "elle se libere automatiquement. Le heap est une zone ou le programmeur "
            "alloue et libere la memoire lui-meme avec malloc/free."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "Variable locale int x = 5;"},
                {"id": "v2", "display": "malloc(100 * sizeof(int))"},
                {"id": "v3", "display": "Parametres de fonction"},
                {"id": "v4", "display": "calloc(10, sizeof(double))"},
            ],
            "types": [
                {"id": "t1", "label": "Stack (pile)"},
                {"id": "t2", "label": "Heap (tas)"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t1", "v4": "t2"},
        },
    },

    "z07_r02": {
        "challenge_id": "z07_r02",
        "zone": 7,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "L'Incantation du Malloc",
        "concept_tags": ["malloc", "sizeof", "cast"],
        "difficulty": 3,
        "question_prompt": (
            "Un aventurier veut allouer de la memoire pour 5 entiers sur le heap. "
            "Complete l'incantation magique (l'appel a malloc)."
        ),
        "hint": (
            "malloc prend en parametre le nombre total d'octets. "
            "Pour 5 int : 5 * sizeof(int)."
        ),
        "explanation": (
            "malloc(5 * sizeof(int)) alloue un bloc de memoire contigu "
            "capable de stocker 5 entiers. Il renvoie un void* qu'on caste "
            "en int*."
        ),
        "payload": {
            "code_before": "int *tab = (int *)",
            "blank_label": "???",
            "code_after": ";\nif (tab == NULL) {\n    printf(\"Echec allocation\");\n    return 1;\n}",
            "options": [
                "malloc(5 * sizeof(int))",
                "malloc(5)",
                "calloc(5)",
                "malloc(sizeof(5))",
            ],
            "correct_answer": "malloc(5 * sizeof(int))",
        },
    },

    "z07_r03": {
        "challenge_id": "z07_r03",
        "zone": 7,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Coffre a Sizeof",
        "concept_tags": ["sizeof", "types", "memoire"],
        "difficulty": 3,
        "question_prompt": (
            "Sur cette machine (systeme 64 bits classique), que vaut "
            "sizeof(int) + sizeof(double) + sizeof(char) ?"
        ),
        "hint": (
            "Sur un systeme 64 bits classique : sizeof(int) = 4, "
            "sizeof(double) = 8, sizeof(char) = 1."
        ),
        "explanation": (
            "sizeof(int) = 4 octets, sizeof(double) = 8 octets, "
            "sizeof(char) = 1 octet. Total = 4 + 8 + 1 = 13."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "int main(void) {\n"
                "    printf(\"%lu\", sizeof(int) + sizeof(double) + sizeof(char));\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "13",
        },
    },

    "z07_r04": {
        "challenge_id": "z07_r04",
        "zone": 7,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Carte du Heap",
        "concept_tags": ["malloc", "free", "heap"],
        "difficulty": 3,
        "question_prompt": (
            "Apres l'execution du code ci-dessous, dans quel etat se trouve "
            "le bloc memoire pointe par 'ptr' ?\n\n"
            "int *ptr = malloc(sizeof(int));\n"
            "*ptr = 42;\n"
            "free(ptr);"
        ),
        "hint": (
            "free() libere le bloc memoire sur le heap. "
            "Le pointeur existe encore mais la memoire n'est plus valide."
        ),
        "explanation": (
            "Apres free(ptr), le bloc memoire est rendu au systeme. "
            "Le pointeur ptr contient toujours l'adresse, mais y acceder "
            "est un comportement indefini (dangling pointer)."
        ),
        "payload": {
            "scenario": (
                "int *ptr = malloc(sizeof(int));\n"
                "*ptr = 42;\n"
                "free(ptr);\n"
                "// Quel est l'etat de ptr maintenant ?"
            ),
            "slots": [
                {"id": "s1", "label": "ptr pointe vers 42 sur le heap (valide)"},
                {"id": "s2", "label": "ptr est un dangling pointer (memoire liberee)"},
                {"id": "s3", "label": "ptr vaut NULL automatiquement"},
                {"id": "s4", "label": "ptr a ete supprime de la stack"},
            ],
            "correct_answer": "s2",
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 5-7 : CONSOLIDATION
    # ──────────────────────────────────────────────

    "z07_r05": {
        "challenge_id": "z07_r05",
        "zone": 7,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Piege du Memory Leak",
        "concept_tags": ["memory_leak", "malloc", "free"],
        "difficulty": 3,
        "question_prompt": (
            "Un piege a ete pose dans ce code ! "
            "Trouve la ligne qui provoque une fuite memoire."
        ),
        "hint": (
            "Une fuite memoire se produit quand on alloue de la memoire "
            "avec malloc mais qu'on ne la libere jamais avec free."
        ),
        "explanation": (
            "La ligne 3 reaffecte le pointeur 'data' a un nouveau bloc sans "
            "liberer le premier bloc alloue a la ligne 1. Les 100 premiers "
            "octets sont perdus — c'est un memory leak."
        ),
        "payload": {
            "code": (
                "char *data = malloc(100);\n"
                "strcpy(data, \"Tresor\");\n"
                "data = malloc(200);         // nouveau bloc\n"
                "strcpy(data, \"Gros tresor\");\n"
                "free(data);"
            ),
            "lines": [
                {"id": "1", "text": "char *data = malloc(100);"},
                {"id": "2", "text": "strcpy(data, \"Tresor\");"},
                {"id": "3", "text": "data = malloc(200);"},
                {"id": "4", "text": "strcpy(data, \"Gros tresor\");"},
                {"id": "5", "text": "free(data);"},
            ],
            "correct_answer": 3,
        },
    },

    "z07_r06": {
        "challenge_id": "z07_r06",
        "zone": 7,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Rituel d'Allocation",
        "concept_tags": ["malloc", "free", "workflow"],
        "difficulty": 3,
        "question_prompt": (
            "Remets les etapes du rituel d'allocation dynamique dans le bon "
            "ordre. Un seul faux pas et le donjon s'effondre !"
        ),
        "hint": (
            "D'abord on alloue, puis on verifie que ca a marche, "
            "ensuite on utilise, et enfin on libere."
        ),
        "explanation": (
            "L'ordre correct est : 1) Allouer avec malloc, 2) Verifier que "
            "le pointeur n'est pas NULL, 3) Utiliser la memoire, "
            "4) Liberer avec free, 5) Mettre le pointeur a NULL."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "free(ptr);"},
                {"id": "c2", "text": "int *ptr = malloc(sizeof(int));"},
                {"id": "c3", "text": "ptr = NULL;"},
                {"id": "c4", "text": "*ptr = 42;"},
                {"id": "c5", "text": "if (ptr == NULL) return 1;"},
            ],
            "display_order": ["c1", "c4", "c3", "c2", "c5"],
            "correct_answer": ["c2", "c5", "c4", "c1", "c3"],
        },
    },

    "z07_r07": {
        "challenge_id": "z07_r07",
        "zone": 7,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "L'Invocation du Calloc",
        "concept_tags": ["calloc", "malloc", "initialisation"],
        "difficulty": 3,
        "question_prompt": (
            "Le mage veut allouer un tableau de 10 double, "
            "tous initialises a 0. Quelle fonction utiliser ?"
        ),
        "hint": (
            "calloc prend deux arguments (nombre d'elements, taille de chaque element) "
            "et initialise tout a zero. malloc n'initialise rien."
        ),
        "explanation": (
            "calloc(10, sizeof(double)) alloue de la memoire pour 10 double "
            "et initialise chaque octet a 0. Contrairement a malloc, "
            "la memoire est garantie a zero."
        ),
        "payload": {
            "code_before": "double *notes = (double *)",
            "blank_label": "???",
            "code_after": ";\n// Tous les elements valent 0.0",
            "options": [
                "calloc(10, sizeof(double))",
                "malloc(10 * sizeof(double))",
                "calloc(10, sizeof(int))",
                "realloc(NULL, 10)",
            ],
            "correct_answer": "calloc(10, sizeof(double))",
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 8 : MINI-BOSS 1
    # ──────────────────────────────────────────────

    "z07_r08": {
        "challenge_id": "z07_r08",
        "zone": 7,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "memory_map",
        "title": "MINI-BOSS : Le Spectre du Malloc",
        "concept_tags": ["malloc", "free", "dangling_pointer", "memory_leak"],
        "difficulty": 4,
        "question_prompt": (
            "Le Spectre du Malloc hante ce code ! Analyse l'etat de la memoire "
            "a la fin de l'execution. Quel probleme se cache ici ?\n\n"
            "int *a = malloc(sizeof(int));\n"
            "int *b = a;\n"
            "*a = 7;\n"
            "free(a);\n"
            "printf(\"%d\", *b);"
        ),
        "hint": (
            "Quand deux pointeurs pointent vers le meme bloc et qu'on "
            "libere via l'un d'eux, l'autre devient un dangling pointer."
        ),
        "explanation": (
            "a et b pointent vers le meme bloc. Apres free(a), le bloc est "
            "libere. Acceder a *b est un acces via dangling pointer — "
            "comportement indefini ! Il faudrait aussi mettre b a NULL."
        ),
        "payload": {
            "scenario": (
                "int *a = malloc(sizeof(int));\n"
                "int *b = a;    // b pointe au meme endroit que a\n"
                "*a = 7;\n"
                "free(a);       // le bloc est libere\n"
                "printf(\"%d\", *b);  // que se passe-t-il ?"
            ),
            "slots": [
                {"id": "s1", "label": "Affiche 7 — tout va bien"},
                {"id": "s2", "label": "Erreur de compilation — b non declare"},
                {"id": "s3", "label": "Acces via dangling pointer — comportement indefini"},
                {"id": "s4", "label": "Memory leak — on a oublie free(b)"},
            ],
            "correct_answer": "s3",
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 9-11 : MAITRISE
    # ──────────────────────────────────────────────

    "z07_r09": {
        "challenge_id": "z07_r09",
        "zone": 7,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Sortilege du Realloc",
        "concept_tags": ["realloc", "malloc", "redimensionnement"],
        "difficulty": 3,
        "question_prompt": (
            "Que vaut tab[2] apres l'execution de ce code ?"
        ),
        "hint": (
            "realloc agrandit (ou retrecit) un bloc existant. "
            "Les anciennes valeurs sont conservees."
        ),
        "explanation": (
            "realloc agrandit le tableau de 3 a 5 elements. "
            "Les 3 premieres valeurs (10, 20, 30) sont conservees. "
            "tab[2] vaut toujours 30."
        ),
        "payload": {
            "code": (
                "int *tab = malloc(3 * sizeof(int));\n"
                "tab[0] = 10;\n"
                "tab[1] = 20;\n"
                "tab[2] = 30;\n"
                "tab = realloc(tab, 5 * sizeof(int));\n"
                "tab[3] = 40;\n"
                "tab[4] = 50;\n"
                "printf(\"%d\", tab[2]);"
            ),
            "correct_answer": "30",
        },
    },

    "z07_r10": {
        "challenge_id": "z07_r10",
        "zone": 7,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Double Free Maudit",
        "concept_tags": ["double_free", "free", "undefined_behavior"],
        "difficulty": 4,
        "question_prompt": (
            "Un sort maudit frappe ce code ! Trouve la ligne qui provoque "
            "un double free — une erreur fatale."
        ),
        "hint": (
            "On ne peut appeler free() qu'une seule fois sur un meme bloc. "
            "Un deuxieme free sur la meme adresse est un double free."
        ),
        "explanation": (
            "La ligne 4 appelle free(ptr) une deuxieme fois sur le meme bloc. "
            "C'est un double free qui provoque un comportement indefini, "
            "souvent un crash. Apres le premier free, il faut mettre ptr = NULL."
        ),
        "payload": {
            "code": (
                "int *ptr = malloc(sizeof(int));\n"
                "*ptr = 99;\n"
                "free(ptr);\n"
                "free(ptr);    // liberation\n"
                "ptr = NULL;"
            ),
            "lines": [
                {"id": "1", "text": "int *ptr = malloc(sizeof(int));"},
                {"id": "2", "text": "*ptr = 99;"},
                {"id": "3", "text": "free(ptr);"},
                {"id": "4", "text": "free(ptr);"},
                {"id": "5", "text": "ptr = NULL;"},
            ],
            "correct_answer": 4,
        },
    },

    "z07_r11": {
        "challenge_id": "z07_r11",
        "zone": 7,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Matrice Dynamique",
        "concept_tags": ["matrice_dynamique", "malloc", "double_pointeur"],
        "difficulty": 4,
        "question_prompt": (
            "On alloue une matrice 3x4 dynamiquement. "
            "Combien d'appels a malloc faut-il au total ?\n\n"
            "int **mat = malloc(3 * sizeof(int *));\n"
            "for (int i = 0; i < 3; i++)\n"
            "    mat[i] = malloc(4 * sizeof(int));"
        ),
        "hint": (
            "Il faut un malloc pour le tableau de pointeurs (les lignes), "
            "puis un malloc par ligne pour les colonnes."
        ),
        "explanation": (
            "1 malloc pour le tableau de 3 pointeurs (int**), "
            "puis 3 mallocs (un par ligne) pour les 4 entiers de chaque ligne. "
            "Total = 1 + 3 = 4 appels a malloc."
        ),
        "payload": {
            "scenario": (
                "int **mat = malloc(3 * sizeof(int *));  // malloc #1\n"
                "for (int i = 0; i < 3; i++)\n"
                "    mat[i] = malloc(4 * sizeof(int));   // malloc #2, #3, #4\n"
                "\n// Combien de malloc au total ?"
            ),
            "slots": [
                {"id": "s1", "label": "3 appels (un par ligne)"},
                {"id": "s2", "label": "4 appels (1 pour les lignes + 3 pour les colonnes)"},
                {"id": "s3", "label": "7 appels (3 + 4)"},
                {"id": "s4", "label": "12 appels (3 x 4)"},
            ],
            "correct_answer": "s2",
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 12 : MINI-BOSS 2
    # ──────────────────────────────────────────────

    "z07_r12": {
        "challenge_id": "z07_r12",
        "zone": 7,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "sort_order",
        "title": "MINI-BOSS : Le Gardien du Free",
        "concept_tags": ["matrice_dynamique", "free", "liberation"],
        "difficulty": 4,
        "question_prompt": (
            "Le Gardien du Free exige que tu liberes cette matrice 3x4 "
            "dans le bon ordre. Un seul faux pas et c'est le crash !\n"
            "Remets les etapes dans l'ordre correct."
        ),
        "hint": (
            "Pour liberer une matrice dynamique, on libere d'abord chaque "
            "ligne, puis le tableau de pointeurs. L'inverse causerait un "
            "acces a de la memoire deja liberee."
        ),
        "explanation": (
            "Il faut liberer dans l'ordre inverse de l'allocation : "
            "d'abord chaque ligne (mat[0], mat[1], mat[2]), puis le "
            "tableau de pointeurs (mat), et enfin mettre mat a NULL."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "free(mat);"},
                {"id": "c2", "text": "free(mat[0]);"},
                {"id": "c3", "text": "free(mat[2]);"},
                {"id": "c4", "text": "free(mat[1]);"},
                {"id": "c5", "text": "mat = NULL;"},
            ],
            "display_order": ["c1", "c3", "c5", "c2", "c4"],
            "correct_answer": ["c2", "c4", "c3", "c1", "c5"],
        },
    },

    # ──────────────────────────────────────────────
    # ROOMS 13-14 : EXPERT
    # ──────────────────────────────────────────────

    "z07_r13": {
        "challenge_id": "z07_r13",
        "zone": 7,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Realloc Traitre",
        "concept_tags": ["realloc", "memory_leak", "pointeur_temporaire"],
        "difficulty": 4,
        "question_prompt": (
            "Ce code contient un piege subtil avec realloc. "
            "Trouve la ligne dangereuse !"
        ),
        "hint": (
            "Si realloc echoue, il renvoie NULL mais ne libere pas "
            "l'ancien bloc. Si on ecrase le pointeur original, "
            "on perd la reference a l'ancien bloc."
        ),
        "explanation": (
            "Ligne 3 : si realloc echoue et renvoie NULL, on ecrase "
            "tab avec NULL et on perd l'adresse de l'ancien bloc — "
            "memory leak ! Il faut utiliser un pointeur temporaire : "
            "int *tmp = realloc(tab, ...) puis verifier tmp avant "
            "d'assigner tab = tmp."
        ),
        "payload": {
            "code": (
                "int *tab = malloc(10 * sizeof(int));\n"
                "// ... remplissage de tab ...\n"
                "tab = realloc(tab, 20 * sizeof(int));\n"
                "if (tab == NULL) {\n"
                "    printf(\"Erreur realloc\");\n"
                "    return 1;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "int *tab = malloc(10 * sizeof(int));"},
                {"id": "2", "text": "// ... remplissage de tab ..."},
                {"id": "3", "text": "tab = realloc(tab, 20 * sizeof(int));"},
                {"id": "4", "text": "if (tab == NULL) {"},
                {"id": "5", "text": "    printf(\"Erreur realloc\");"},
                {"id": "6", "text": "    return 1;"},
                {"id": "7", "text": "}"},
            ],
            "correct_answer": 3,
        },
    },

    "z07_r14": {
        "challenge_id": "z07_r14",
        "zone": 7,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "L'Audit du Heap",
        "concept_tags": ["memory_leak", "free", "dangling_pointer", "audit"],
        "difficulty": 5,
        "question_prompt": (
            "Le code suivant contient un probleme memoire. "
            "Identifie le diagnostic correct.\n\n"
            "void creer_message(void) {\n"
            "    char *msg = malloc(50);\n"
            "    strcpy(msg, \"Bienvenue dans le donjon\");\n"
            "    printf(\"%s\", msg);\n"
            "}"
        ),
        "hint": (
            "Que se passe-t-il quand la fonction se termine ? "
            "Le pointeur msg (sur la stack) est detruit, mais le bloc "
            "sur le heap..."
        ),
        "explanation": (
            "Quand creer_message() se termine, le pointeur local msg "
            "disparait de la stack, mais le bloc de 50 octets alloue sur "
            "le heap n'est jamais libere. C'est un memory leak classique. "
            "Il faut ajouter free(msg) avant la fin de la fonction."
        ),
        "payload": {
            "scenario": (
                "void creer_message(void) {\n"
                "    char *msg = malloc(50);\n"
                "    strcpy(msg, \"Bienvenue dans le donjon\");\n"
                "    printf(\"%s\", msg);\n"
                "    // fin de la fonction — pas de free\n"
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "Aucun probleme — le systeme libere tout a la sortie de la fonction"},
                {"id": "s2", "label": "Dangling pointer — msg pointe vers une zone invalide"},
                {"id": "s3", "label": "Memory leak — le bloc malloc n'est jamais libere"},
                {"id": "s4", "label": "Double free — msg est libere deux fois"},
            ],
            "correct_answer": "s3",
        },
    },

    # ──────────────────────────────────────────────
    # ROOM 15 : BOSS
    # ──────────────────────────────────────────────

    "z07_r15": {
        "challenge_id": "z07_r15",
        "zone": 7,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "BOSS : L'Hydre Memory Leak",
        "concept_tags": [
            "memory_leak", "dangling_pointer", "double_free",
            "malloc", "free", "matrice_dynamique",
        ],
        "difficulty": 5,
        "question_prompt": (
            "L'Hydre Memory Leak te lance son ultime defi ! "
            "Analyse ce code complexe et identifie le vrai probleme.\n\n"
            "int **grille = malloc(3 * sizeof(int *));\n"
            "for (int i = 0; i < 3; i++)\n"
            "    grille[i] = malloc(3 * sizeof(int));\n"
            "\n"
            "// ... utilisation de la grille ...\n"
            "\n"
            "free(grille);  // liberation"
        ),
        "hint": (
            "Pour liberer une matrice, il ne suffit pas de liberer le "
            "tableau de pointeurs. Chaque ligne allouee separement doit "
            "aussi etre liberee."
        ),
        "explanation": (
            "free(grille) ne libere que le tableau de 3 pointeurs. "
            "Les 3 blocs alloues pour chaque ligne (grille[0], grille[1], "
            "grille[2]) ne sont pas liberes — 3 memory leaks ! "
            "Il faut d'abord faire free(grille[i]) pour chaque i, "
            "PUIS free(grille)."
        ),
        "payload": {
            "scenario": (
                "int **grille = malloc(3 * sizeof(int *));\n"
                "for (int i = 0; i < 3; i++)\n"
                "    grille[i] = malloc(3 * sizeof(int));\n"
                "\n"
                "// ... utilisation de la grille ...\n"
                "\n"
                "free(grille);  // liberation\n"
                "// Quel est le diagnostic ?"
            ),
            "slots": [
                {
                    "id": "s1",
                    "label": (
                        "Correct — free(grille) libere tout automatiquement"
                    ),
                },
                {
                    "id": "s2",
                    "label": (
                        "Memory leak — les 3 lignes (grille[i]) ne sont jamais liberees"
                    ),
                },
                {
                    "id": "s3",
                    "label": (
                        "Double free — grille est libere deux fois"
                    ),
                },
                {
                    "id": "s4",
                    "label": (
                        "Dangling pointer — grille est utilise apres free"
                    ),
                },
            ],
            "correct_answer": "s2",
        },
    },
}
