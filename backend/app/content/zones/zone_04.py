"""
Zone 4 — Data Fortress
Cours 5 : Structs, typedef, tableaux 1D, initialisation, parcours,
           recherche, tri, tableaux 2D, enum.
15 salles : 4 intro · 3 consolidation · 1 mini-boss · 3 maîtrise ·
            1 mini-boss · 2 expert · 1 boss.
"""

from app.content.challenge_types import ChallengeData

ZONE_4_CHALLENGES: dict[str, ChallengeData] = {
    # ── Room 1  (intro — difficulté 2) ─────────────────────────────
    "z04_r01": {
        "challenge_id": "z04_r01",
        "zone": 4,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Les Premières Briques de la Forteresse",
        "concept_tags": ["struct", "initialisation"],
        "difficulty": 2,
        "question_prompt": (
            "Un messager dépose un parchemin à l'entrée de la Forteresse. "
            "Quelle valeur affiche ce programme ?"
        ),
        "hint": "Chaque champ d'une struct se lit avec l'opérateur point.",
        "explanation": (
            "La struct `Soldat` possède les champs `pv` et `attaque`. "
            "On initialise `pv = 100` et `attaque = 15`, puis on affiche "
            "`s.attaque` → 15."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "typedef struct {\n"
                "    int pv;\n"
                "    int attaque;\n"
                "} Soldat;\n"
                "\n"
                "int main(void) {\n"
                "    Soldat s = {100, 15};\n"
                "    printf(\"%d\", s.attaque);\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "15",
        },
    },

    # ── Room 2  (intro — difficulté 2) ─────────────────────────────
    "z04_r02": {
        "challenge_id": "z04_r02",
        "zone": 4,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "Le Rempart du typedef",
        "concept_tags": ["typedef", "struct"],
        "difficulty": 2,
        "question_prompt": (
            "Un garde vous tend un grimoire incomplet. "
            "Complétez la déclaration pour que `Arme` soit "
            "un alias de la struct."
        ),
        "hint": "Le mot-clé typedef crée un alias : typedef <type existant> <nouveau nom>;",
        "explanation": (
            "typedef struct { ... } Arme; permet ensuite d'écrire "
            "`Arme epee;` au lieu de `struct Arme epee;`."
        ),
        "payload": {
            "code_before": (
                "typedef struct {\n"
                "    char nom[20];\n"
                "    int degats;\n"
                "}"
            ),
            "blank_label": "???",
            "code_after": (
                ";\n"
                "\n"
                "int main(void) {\n"
                "    Arme epee = {\"Excalibur\", 50};\n"
                "    return 0;\n"
                "}"
            ),
            "options": ["Arme", "struct Arme", "new Arme", "define Arme"],
            "correct_answer": "Arme",
        },
    },

    # ── Room 3  (intro — difficulté 2) ─────────────────────────────
    "z04_r03": {
        "challenge_id": "z04_r03",
        "zone": 4,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "Carte du Donjon — Tableau 1D",
        "concept_tags": ["tableau_1D", "initialisation"],
        "difficulty": 2,
        "question_prompt": (
            "Un tableau d'entiers est initialisé : "
            "`int mur[4] = {3, 7, 1, 9};` — "
            "dans quel slot se trouve la valeur 1 ?"
        ),
        "hint": "Les indices d'un tableau commencent à 0 en C.",
        "explanation": (
            "mur[0]=3, mur[1]=7, mur[2]=1, mur[3]=9. "
            "La valeur 1 est à l'index 2."
        ),
        "payload": {
            "scenario": (
                "int mur[4] = {3, 7, 1, 9};\n"
                "Chaque slot représente un indice du tableau."
            ),
            "slots": [
                {"id": "s0", "label": "mur[0] = 3"},
                {"id": "s1", "label": "mur[1] = 7"},
                {"id": "s2", "label": "mur[2] = 1"},
                {"id": "s3", "label": "mur[3] = 9"},
            ],
            "correct_answer": "s2",
        },
    },

    # ── Room 4  (intro — difficulté 2) ─────────────────────────────
    "z04_r04": {
        "challenge_id": "z04_r04",
        "zone": 4,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Registre des Declarations",
        "concept_tags": ["enum", "typedef", "struct"],
        "difficulty": 2,
        "question_prompt": (
            "Associez chaque déclaration à ce qu'elle définit. "
            "L'armurerie doit être bien rangée !"
        ),
        "hint": "enum définit des constantes nommées, typedef crée un alias, struct regroupe des champs.",
        "explanation": (
            "enum crée une liste de constantes entières, "
            "typedef donne un nom plus court à un type, "
            "et struct regroupe plusieurs variables sous un même type."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "enum Direction {NORD, SUD, EST, OUEST};"},
                {"id": "v2", "display": "typedef unsigned int uint;"},
                {"id": "v3", "display": "struct Coffre { int pieces; int gemmes; };"},
            ],
            "types": [
                {"id": "t1", "label": "Constantes entières nommées"},
                {"id": "t2", "label": "Alias de type"},
                {"id": "t3", "label": "Regroupement de champs"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3"},
        },
    },

    # ── Room 5  (consolidation — difficulté 2) ─────────────────────
    "z04_r05": {
        "challenge_id": "z04_r05",
        "zone": 4,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "La Ronde des Sentinelles",
        "concept_tags": ["tableau_1D", "parcours", "boucle_for"],
        "difficulty": 2,
        "question_prompt": (
            "Les sentinelles font leur ronde le long du rempart. "
            "Quelle est la valeur affichée ?"
        ),
        "hint": "La boucle parcourt tout le tableau et accumule chaque élément dans `somme`.",
        "explanation": (
            "Le tableau contient {2, 5, 3, 10}. La boucle additionne : "
            "2 + 5 + 3 + 10 = 20."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "int main(void) {\n"
                "    int gardes[4] = {2, 5, 3, 10};\n"
                "    int somme = 0;\n"
                "    for (int i = 0; i < 4; i++) {\n"
                "        somme += gardes[i];\n"
                "    }\n"
                "    printf(\"%d\", somme);\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "20",
        },
    },

    # ── Room 6  (consolidation — difficulté 3) ─────────────────────
    "z04_r06": {
        "challenge_id": "z04_r06",
        "zone": 4,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Piège de l'Indice Fantôme",
        "concept_tags": ["tableau_1D", "parcours", "off_by_one"],
        "difficulty": 3,
        "question_prompt": (
            "Un espion a saboté le code de la garnison. "
            "Trouvez la ligne qui contient le bug !"
        ),
        "hint": "Un tableau de taille N a des indices de 0 à N-1.",
        "explanation": (
            "Le tableau `pieges` a 5 éléments (indices 0-4). "
            "La boucle va jusqu'à `i <= 5`, donc elle lit `pieges[5]` "
            "qui dépasse la fin du tableau — c'est un accès hors bornes."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "int main(void) {\n"
                "    int pieges[5] = {1, 0, 1, 1, 0};\n"
                "    int total = 0;\n"
                "    for (int i = 0; i <= 5; i++) {\n"
                "        total += pieges[i];\n"
                "    }\n"
                "    printf(\"%d\", total);\n"
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "int pieges[5] = {1, 0, 1, 1, 0};"},
                {"id": "2", "text": "int total = 0;"},
                {"id": "3", "text": "for (int i = 0; i <= 5; i++) {"},
                {"id": "4", "text": "    total += pieges[i];"},
                {"id": "5", "text": "printf(\"%d\", total);"},
            ],
            "correct_answer": 3,
        },
    },

    # ── Room 7  (consolidation — difficulté 3) ─────────────────────
    "z04_r07": {
        "challenge_id": "z04_r07",
        "zone": 4,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "L'Escalier de la Tour Nord",
        "concept_tags": ["recherche", "tableau_1D", "algorithme"],
        "difficulty": 3,
        "question_prompt": (
            "Remettez dans l'ordre les étapes d'une recherche "
            "séquentielle d'une valeur dans un tableau."
        ),
        "hint": "On parcourt le tableau élément par élément jusqu'à trouver la cible ou atteindre la fin.",
        "explanation": (
            "Recherche séquentielle : on initialise, on boucle, "
            "on compare, on retourne l'indice si trouvé, sinon -1."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "Initialiser i = 0"},
                {"id": "c2", "text": "Tant que i < taille du tableau"},
                {"id": "c3", "text": "Comparer tab[i] avec la cible"},
                {"id": "c4", "text": "Si égal, retourner i"},
                {"id": "c5", "text": "Sinon, incrémenter i"},
                {"id": "c6", "text": "Retourner -1 (non trouvé)"},
            ],
            "display_order": ["c4", "c1", "c6", "c3", "c5", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4", "c5", "c6"],
        },
    },

    # ── Room 8  (mini-boss — difficulté 3) ─────────────────────────
    "z04_r08": {
        "challenge_id": "z04_r08",
        "zone": 4,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "trace_value",
        "title": "MINI-BOSS : La Sentinelle des Tableaux",
        "concept_tags": ["tableau_1D", "parcours", "recherche"],
        "difficulty": 3,
        "question_prompt": (
            "La Sentinelle des Tableaux vous défie ! "
            "Ce programme cherche le maximum. Quelle valeur est affichée ?"
        ),
        "hint": "La variable `max` est mise à jour chaque fois qu'on trouve un élément plus grand.",
        "explanation": (
            "Le tableau est {4, 9, 2, 7, 1}. La boucle compare chaque "
            "élément à `max` (initialisé à `tab[0]` = 4). "
            "On met à jour : 4→9, et 9 reste le max. Résultat : 9."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "int main(void) {\n"
                "    int tab[5] = {4, 9, 2, 7, 1};\n"
                "    int max = tab[0];\n"
                "    for (int i = 1; i < 5; i++) {\n"
                "        if (tab[i] > max) {\n"
                "            max = tab[i];\n"
                "        }\n"
                "    }\n"
                "    printf(\"%d\", max);\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "9",
        },
    },

    # ── Room 9  (maîtrise — difficulté 3) ──────────────────────────
    "z04_r09": {
        "challenge_id": "z04_r09",
        "zone": 4,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "Le Passage Secret du Tri",
        "concept_tags": ["tri", "tableau_1D", "tri_selection"],
        "difficulty": 3,
        "question_prompt": (
            "Le passage secret ne s'ouvre que si le tableau est trié. "
            "Complétez la condition du tri par sélection."
        ),
        "hint": "Dans le tri par sélection, on cherche le minimum et on l'échange avec l'élément courant.",
        "explanation": (
            "Le tri par sélection compare `tab[j] < tab[min_idx]` "
            "pour trouver l'indice du plus petit élément dans la "
            "partie non triée."
        ),
        "payload": {
            "code_before": (
                "void tri_selection(int tab[], int n) {\n"
                "    for (int i = 0; i < n - 1; i++) {\n"
                "        int min_idx = i;\n"
                "        for (int j = i + 1; j < n; j++) {\n"
                "            if ("
            ),
            "blank_label": "???",
            "code_after": (
                ") {\n"
                "                min_idx = j;\n"
                "            }\n"
                "        }\n"
                "        int tmp = tab[i];\n"
                "        tab[i] = tab[min_idx];\n"
                "        tab[min_idx] = tmp;\n"
                "    }\n"
                "}"
            ),
            "options": [
                "tab[j] < tab[min_idx]",
                "tab[j] > tab[min_idx]",
                "tab[i] < tab[j]",
                "j < min_idx",
            ],
            "correct_answer": "tab[j] < tab[min_idx]",
        },
    },

    # ── Room 10  (maîtrise — difficulté 3) ─────────────────────────
    "z04_r10": {
        "challenge_id": "z04_r10",
        "zone": 4,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "Le Damier de la Forteresse",
        "concept_tags": ["tableau_2D", "initialisation", "indice"],
        "difficulty": 3,
        "question_prompt": (
            "La salle du trône est pavée d'un damier 3x3. "
            "Le tableau est :\n"
            "`int damier[3][3] = {{1,2,3},{4,5,6},{7,8,9}};`\n"
            "Dans quel slot se trouve la valeur `damier[1][2]` ?"
        ),
        "hint": "damier[ligne][colonne] — les indices commencent à 0.",
        "explanation": (
            "damier[1][2] correspond à la 2e ligne (indice 1), "
            "3e colonne (indice 2), soit la valeur 6."
        ),
        "payload": {
            "scenario": (
                "int damier[3][3] = {{1,2,3},{4,5,6},{7,8,9}};\n"
                "On cherche la case damier[1][2]."
            ),
            "slots": [
                {"id": "s1", "label": "Valeur 3 — damier[0][2]"},
                {"id": "s2", "label": "Valeur 5 — damier[1][1]"},
                {"id": "s3", "label": "Valeur 6 — damier[1][2]"},
                {"id": "s4", "label": "Valeur 8 — damier[2][1]"},
            ],
            "correct_answer": "s3",
        },
    },

    # ── Room 11  (maîtrise — difficulté 3) ─────────────────────────
    "z04_r11": {
        "challenge_id": "z04_r11",
        "zone": 4,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "L'Énigme de l'Enum",
        "concept_tags": ["enum", "switch", "struct"],
        "difficulty": 3,
        "question_prompt": (
            "Le gardien pose une énigme. "
            "Quelle valeur affiche ce programme utilisant un enum ?"
        ),
        "hint": "Par défaut, les valeurs d'un enum commencent à 0 et s'incrémentent de 1.",
        "explanation": (
            "enum Rang { SOLDAT, CAPITAINE, GENERAL } donne "
            "SOLDAT=0, CAPITAINE=1, GENERAL=2. "
            "On affiche `r` qui vaut GENERAL, soit 2."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "enum Rang { SOLDAT, CAPITAINE, GENERAL };\n"
                "\n"
                "int main(void) {\n"
                "    enum Rang r = GENERAL;\n"
                "    printf(\"%d\", r);\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "2",
        },
    },

    # ── Room 12  (mini-boss — difficulté 4) ────────────────────────
    "z04_r12": {
        "challenge_id": "z04_r12",
        "zone": 4,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "sort_order",
        "title": "MINI-BOSS : Le Titan du Tri",
        "concept_tags": ["tri", "tri_bulle", "tableau_1D"],
        "difficulty": 4,
        "question_prompt": (
            "Le Titan du Tri exige que vous remettiez dans l'ordre "
            "les étapes d'un tri à bulles sur le tableau {5, 1, 3}."
        ),
        "hint": "Le tri à bulles compare les éléments adjacents et les échange si nécessaire, en plusieurs passes.",
        "explanation": (
            "Passe 1 : on compare (5,1)→échange→{1,5,3}, "
            "puis (5,3)→échange→{1,3,5}. "
            "Passe 2 : (1,3) ok, (3,5) ok → terminé. "
            "Résultat : {1, 3, 5}."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "Comparer tab[0] et tab[1] : 5 > 1 → échanger → {1, 5, 3}"},
                {"id": "c2", "text": "Comparer tab[1] et tab[2] : 5 > 3 → échanger → {1, 3, 5}"},
                {"id": "c3", "text": "Nouvelle passe : comparer tab[0] et tab[1] : 1 < 3 → pas d'échange"},
                {"id": "c4", "text": "Comparer tab[1] et tab[2] : 3 < 5 → pas d'échange"},
                {"id": "c5", "text": "Aucun échange lors de cette passe → tableau trié"},
            ],
            "display_order": ["c3", "c5", "c1", "c4", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4", "c5"],
        },
    },

    # ── Room 13  (expert — difficulté 4) ───────────────────────────
    "z04_r13": {
        "challenge_id": "z04_r13",
        "zone": 4,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Sortilège Corrompu",
        "concept_tags": ["struct", "tableau_1D", "initialisation"],
        "difficulty": 4,
        "question_prompt": (
            "Un sorcier a corrompu le code de l'inventaire. "
            "Trouvez la ligne défectueuse !"
        ),
        "hint": "Quand on accède à un champ de struct via un tableau, c'est `tab[i].champ`, pas `tab.champ[i]`.",
        "explanation": (
            "La ligne `inv.nom[0]` est incorrecte. `inv` est un tableau "
            "de structs : il faut écrire `inv[0].nom` pour accéder au "
            "champ `nom` du premier élément."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "typedef struct {\n"
                "    char nom[20];\n"
                "    int quantite;\n"
                "} Objet;\n"
                "\n"
                "int main(void) {\n"
                "    Objet inv[3] = {{\"Potion\", 5}, {\"Cle\", 1}, {\"Bouclier\", 2}};\n"
                "    printf(\"%s\", inv.nom[0]);\n"
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "typedef struct {"},
                {"id": "2", "text": "    char nom[20];"},
                {"id": "3", "text": "Objet inv[3] = {{\"Potion\", 5}, {\"Cle\", 1}, {\"Bouclier\", 2}};"},
                {"id": "4", "text": "printf(\"%s\", inv.nom[0]);"},
                {"id": "5", "text": "return 0;"},
            ],
            "correct_answer": 4,
        },
    },

    # ── Room 14  (expert — difficulté 4) ───────────────────────────
    "z04_r14": {
        "challenge_id": "z04_r14",
        "zone": 4,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Grimoire des Matrices",
        "concept_tags": ["tableau_2D", "parcours", "struct", "enum"],
        "difficulty": 4,
        "question_prompt": (
            "Associez chaque fragment de code à sa description. "
            "Le grimoire ne tolère aucune erreur !"
        ),
        "hint": "Lisez chaque fragment et identifiez ce qu'il fait : déclarer, parcourir, ou accéder.",
        "explanation": (
            "int m[2][3] déclare une matrice 2 lignes × 3 colonnes. "
            "La double boucle for parcourt toutes les cases. "
            "m[i][j] = i + j remplit chaque case avec la somme des indices. "
            "L'enum avec valeur initiale BRONZE=10 donne ARGENT=11, OR=12."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "int m[2][3];"},
                {"id": "v2", "display": "for (int i=0; i<2; i++) for (int j=0; j<3; j++) m[i][j] = i+j;"},
                {"id": "v3", "display": "enum Medal { BRONZE=10, ARGENT, OR };"},
                {"id": "v4", "display": "printf(\"%d\", m[1][2]);"},
            ],
            "types": [
                {"id": "t1", "label": "Déclare une matrice 2×3"},
                {"id": "t2", "label": "Remplit la matrice avec i+j"},
                {"id": "t3", "label": "Définit un enum à partir de 10"},
                {"id": "t4", "label": "Affiche la case ligne 1, colonne 2"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    # ── Room 15  (boss — difficulté 4) ─────────────────────────────
    "z04_r15": {
        "challenge_id": "z04_r15",
        "zone": 4,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "BOSS : La Forteresse des Données",
        "concept_tags": [
            "struct", "typedef", "tableau_1D", "tri", "enum", "tableau_2D",
        ],
        "difficulty": 4,
        "question_prompt": (
            "La Forteresse des Données vous lance son ultime défi ! "
            "Ce programme combine struct, enum et tableau. "
            "Quelle valeur est affichée ?"
        ),
        "hint": (
            "Suivez pas à pas : créez le tableau de structs, "
            "puis appliquez le tri et lisez le champ demandé."
        ),
        "explanation": (
            "On crée 3 Guerriers : {GENERAL, 90}, {SOLDAT, 40}, {CAPITAINE, 65}. "
            "Le tri par sélection trie par `force` croissante : "
            "{SOLDAT,40}, {CAPITAINE,65}, {GENERAL,90}. "
            "Après le tri, `armee[2].force` est la plus grande valeur, "
            "soit 90."
        ),
        "payload": {
            "code": (
                "#include <stdio.h>\n"
                "\n"
                "enum Rang { SOLDAT, CAPITAINE, GENERAL };\n"
                "\n"
                "typedef struct {\n"
                "    enum Rang rang;\n"
                "    int force;\n"
                "} Guerrier;\n"
                "\n"
                "int main(void) {\n"
                "    Guerrier armee[3] = {\n"
                "        {GENERAL, 90},\n"
                "        {SOLDAT, 40},\n"
                "        {CAPITAINE, 65}\n"
                "    };\n"
                "    // Tri par selection sur force\n"
                "    for (int i = 0; i < 2; i++) {\n"
                "        int min = i;\n"
                "        for (int j = i + 1; j < 3; j++) {\n"
                "            if (armee[j].force < armee[min].force)\n"
                "                min = j;\n"
                "        }\n"
                "        Guerrier tmp = armee[i];\n"
                "        armee[i] = armee[min];\n"
                "        armee[min] = tmp;\n"
                "    }\n"
                "    printf(\"%d\", armee[2].force);\n"
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "90",
        },
    },
}
