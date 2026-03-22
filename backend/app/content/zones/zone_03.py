"""
Zone 3 — Function Factory
Cours 4 : Fonctions, prototypes, parametres, return, scope,
           passage par copie, headers, multi-fichiers, recursivite.
15 salles (rooms 1-15) dont 2 mini-boss et 1 boss final.
"""

from app.content.challenge_types import ChallengeData

ZONE_3_CHALLENGES: dict[str, ChallengeData] = {

    # ─────────────────────────────────────────────────────────
    # ROOMS 1-4 : INTRODUCTION  (difficultés 1, 2, 2, 2)
    # ─────────────────────────────────────────────────────────

    "z03_r01": {
        "challenge_id": "z03_r01",
        "zone": 3,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "Premier Engrenage",
        "concept_tags": ["fonction", "declaration", "prototype"],
        "difficulty": 1,
        "question_prompt": (
            "L'Usine a besoin d'un premier engrenage pour démarrer. "
            "Complète la déclaration de cette fonction qui affiche un message de bienvenue."
        ),
        "hint": "Une fonction qui ne renvoie rien utilise le type de retour void.",
        "explanation": (
            "void indique que la fonction ne retourne aucune valeur. "
            "C'est le type de retour le plus simple : la fonction fait une action sans rien renvoyer."
        ),
        "payload": {
            "code_before": "",
            "blank_label": "???",
            "code_after": (
                " bienvenue() {\n"
                '    printf("Bienvenue dans l\'Usine !\\n");\n'
                "}"
            ),
            "options": ["void", "int", "return", "main"],
            "correct_answer": "void",
        },
    },

    "z03_r02": {
        "challenge_id": "z03_r02",
        "zone": 3,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "La Chaîne de Montage",
        "concept_tags": ["fonction", "return", "appel"],
        "difficulty": 2,
        "question_prompt": (
            "La chaîne de montage exécute cette fonction. "
            "Quelle valeur est affichée par printf ?"
        ),
        "hint": "La fonction doubler() renvoie son paramètre multiplié par 2. Remplace l'appel par sa valeur de retour.",
        "explanation": (
            "doubler(7) renvoie 14. La valeur retournée par la fonction est "
            "directement utilisée dans le printf, qui affiche donc 14."
        ),
        "payload": {
            "code": (
                "int doubler(int x) {\n"
                "    return x * 2;\n"
                "}\n\n"
                "int main() {\n"
                "    int r = doubler(7);\n"
                '    printf("%d", r);\n'
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "14",
        },
    },

    "z03_r03": {
        "challenge_id": "z03_r03",
        "zone": 3,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Tri des Pièces",
        "concept_tags": ["types_retour", "prototype", "parametres"],
        "difficulty": 2,
        "question_prompt": (
            "Chaque prototype de fonction doit être associé au bon type de retour. "
            "Trie les pièces détachées de l'Usine !"
        ),
        "hint": "Regarde le mot-clé tout à gauche du prototype : c'est le type de retour de la fonction.",
        "explanation": (
            "Le type de retour est le premier mot du prototype : "
            "int → entier, float → flottant, void → rien, char → caractère."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "int somme(int a, int b);"},
                {"id": "v2", "display": "void afficher(char c);"},
                {"id": "v3", "display": "float moyenne(float a, float b);"},
                {"id": "v4", "display": "char initiale(char* nom);"},
            ],
            "types": [
                {"id": "t1", "label": "Retourne un entier"},
                {"id": "t2", "label": "Ne retourne rien"},
                {"id": "t3", "label": "Retourne un flottant"},
                {"id": "t4", "label": "Retourne un caractère"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    "z03_r04": {
        "challenge_id": "z03_r04",
        "zone": 3,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "L'Engrenage Grippé",
        "concept_tags": ["prototype", "declaration", "erreur_compilation"],
        "difficulty": 2,
        "question_prompt": (
            "Un engrenage de l'Usine est grippé ! "
            "Ce code ne compile pas. Trouve la ligne fautive."
        ),
        "hint": "En C, si tu appelles une fonction avant de l'avoir déclarée, le compilateur ne la connaît pas encore.",
        "explanation": (
            "La fonction carre() est appelée dans main() (ligne 2) avant d'être "
            "définie (ligne 6). Il faut soit ajouter un prototype avant main, "
            "soit déplacer la définition de carre() avant main()."
        ),
        "payload": {
            "code": (
                "int main() {\n"
                "    int r = carre(5);\n"
                '    printf("%d", r);\n'
                "    return 0;\n"
                "}\n"
                "int carre(int n) {\n"
                "    return n * n;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "int main() {"},
                {"id": "2", "text": "    int r = carre(5);"},
                {"id": "3", "text": '    printf("%d", r);'},
                {"id": "4", "text": "    return 0;"},
                {"id": "5", "text": "}"},
                {"id": "6", "text": "int carre(int n) {"},
                {"id": "7", "text": "    return n * n;"},
                {"id": "8", "text": "}"},
            ],
            "correct_answer": 2,
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOMS 5-7 : CONSOLIDATION  (difficultés 2, 3, 3)
    # ─────────────────────────────────────────────────────────

    "z03_r05": {
        "challenge_id": "z03_r05",
        "zone": 3,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Salle des Copies",
        "concept_tags": ["passage_par_copie", "parametres", "scope"],
        "difficulty": 2,
        "question_prompt": (
            "En C, les paramètres sont passés par copie. "
            "Après l'appel de modifier(x), quelle case mémoire contient "
            "la bonne valeur de x dans main ?"
        ),
        "hint": (
            "Le passage par copie signifie que la fonction travaille sur "
            "une copie du paramètre. La variable originale n'est pas modifiée."
        ),
        "explanation": (
            "En C, les arguments sont passés par copie. modifier(x) reçoit une copie de x : "
            "la modification de n dans la fonction n'affecte pas x dans main. "
            "x reste à 10."
        ),
        "payload": {
            "scenario": (
                "void modifier(int n) {\n"
                "    n = n + 100;\n"
                "}\n\n"
                "int main() {\n"
                "    int x = 10;\n"
                "    modifier(x);\n"
                '    printf("%d", x);\n'
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "x = 110 (modifié par la fonction)"},
                {"id": "s2", "label": "x = 10 (inchangé, passage par copie)"},
                {"id": "s3", "label": "x = 100 (remplacé par n)"},
                {"id": "s4", "label": "x = 0 (réinitialisé après l'appel)"},
            ],
            "correct_answer": "s2",
        },
    },

    "z03_r06": {
        "challenge_id": "z03_r06",
        "zone": 3,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Convoyeur à Prototypes",
        "concept_tags": ["prototype", "multi_fichiers", "headers", "include"],
        "difficulty": 3,
        "question_prompt": (
            "Pour compiler un programme multi-fichiers, les étapes "
            "doivent être dans le bon ordre. Remets le convoyeur en marche !"
        ),
        "hint": (
            "D'abord on déclare (prototype), puis on inclut le header, "
            "puis on implémente, puis on appelle."
        ),
        "explanation": (
            "En multi-fichiers : 1) on écrit le prototype dans le .h, "
            "2) on inclut le .h avec #include, "
            "3) on implémente la fonction dans le .c correspondant, "
            "4) on appelle la fonction depuis main()."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "Écrire le prototype dans calcul.h"},
                {"id": "c2", "text": "Implémenter la fonction dans calcul.c"},
                {"id": "c3", "text": '#include "calcul.h" dans main.c'},
                {"id": "c4", "text": "Appeler la fonction dans main()"},
            ],
            "display_order": ["c3", "c4", "c1", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    "z03_r07": {
        "challenge_id": "z03_r07",
        "zone": 3,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Les Rouages Imbriqués",
        "concept_tags": ["appel_fonction", "return", "composition"],
        "difficulty": 3,
        "question_prompt": (
            "Deux fonctions s'appellent en cascade. "
            "Quelle valeur est affichée à la fin ?"
        ),
        "hint": "Résous d'abord l'appel le plus interne (ajouter), puis utilise ce résultat pour l'appel externe (multiplier).",
        "explanation": (
            "ajouter(3, 2) renvoie 5. Puis multiplier(5, 4) renvoie 20. "
            "Les fonctions se composent : le résultat de l'une sert d'argument à l'autre."
        ),
        "payload": {
            "code": (
                "int ajouter(int a, int b) {\n"
                "    return a + b;\n"
                "}\n\n"
                "int multiplier(int a, int b) {\n"
                "    return a * b;\n"
                "}\n\n"
                "int main() {\n"
                "    int r = multiplier(ajouter(3, 2), 4);\n"
                '    printf("%d", r);\n'
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "20",
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOM 8 : MINI-BOSS #1  (difficulté 3)
    # ─────────────────────────────────────────────────────────

    "z03_r08": {
        "challenge_id": "z03_r08",
        "zone": 3,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "fill_blank",
        "title": "MINI-BOSS : Le Gardien des Prototypes",
        "concept_tags": ["prototype", "declaration", "headers", "compilation"],
        "difficulty": 3,
        "question_prompt": (
            "Le Gardien des Prototypes bloque le passage ! "
            "Il manque le prototype de la fonction pour que ce programme compile. "
            "Complète la ligne manquante."
        ),
        "hint": (
            "Un prototype, c'est la signature de la fonction suivie d'un point-virgule. "
            "Il doit apparaître avant tout appel."
        ),
        "explanation": (
            "Le prototype int puissance(int base, int exp); déclare la fonction "
            "avant son utilisation dans main(). Sans prototype, le compilateur "
            "ne connaît pas la fonction au moment de l'appel."
        ),
        "payload": {
            "code_before": "#include <stdio.h>\n\n",
            "blank_label": "???",
            "code_after": (
                "\n\n"
                "int main() {\n"
                '    printf("%d", puissance(2, 8));\n'
                "    return 0;\n"
                "}\n\n"
                "int puissance(int base, int exp) {\n"
                "    int r = 1;\n"
                "    for (int i = 0; i < exp; i++)\n"
                "        r *= base;\n"
                "    return r;\n"
                "}"
            ),
            "options": [
                "int puissance(int base, int exp);",
                "void puissance(int, int);",
                "int puissance(base, exp);",
                "puissance(int base, int exp);",
            ],
            "correct_answer": "int puissance(int base, int exp);",
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOMS 9-11 : MAÎTRISE  (difficultés 3, 3, 3)
    # ─────────────────────────────────────────────────────────

    "z03_r09": {
        "challenge_id": "z03_r09",
        "zone": 3,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "La Fuite dans le Tuyau",
        "concept_tags": ["scope", "variable_locale", "erreur"],
        "difficulty": 3,
        "question_prompt": (
            "Une fuite s'est déclarée dans la tuyauterie de l'Usine ! "
            "Ce code compile mais produit un comportement inattendu. "
            "Quelle ligne contient le bug ?"
        ),
        "hint": (
            "Attention au scope : une variable déclarée dans une fonction "
            "n'existe pas en dehors de cette fonction."
        ),
        "explanation": (
            "À la ligne 3, la variable resultat est locale à calculer(). "
            "À la ligne 8, main() essaie d'utiliser resultat qui n'existe "
            "pas dans son scope. Le compilateur signalerait une erreur "
            "« undeclared identifier »."
        ),
        "payload": {
            "code": (
                "void calculer() {\n"
                "    int a = 5, b = 3;\n"
                "    int resultat = a + b;\n"
                "}\n\n"
                "int main() {\n"
                "    calculer();\n"
                '    printf("%d", resultat);\n'
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "void calculer() {"},
                {"id": "2", "text": "    int a = 5, b = 3;"},
                {"id": "3", "text": "    int resultat = a + b;"},
                {"id": "4", "text": "}"},
                {"id": "5", "text": ""},
                {"id": "6", "text": "int main() {"},
                {"id": "7", "text": "    calculer();"},
                {"id": "8", "text": '    printf("%d", resultat);'},
                {"id": "9", "text": "    return 0;"},
                {"id": "10", "text": "}"},
            ],
            "correct_answer": 8,
        },
    },

    "z03_r10": {
        "challenge_id": "z03_r10",
        "zone": 3,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Tableau de Contrôle",
        "concept_tags": ["scope", "variable_locale", "variable_globale", "parametre"],
        "difficulty": 3,
        "question_prompt": (
            "Sur le tableau de contrôle de l'Usine, chaque variable "
            "a une portée différente. Associe chaque variable à son scope !"
        ),
        "hint": (
            "Global = déclaré hors de toute fonction, local = dans une fonction, "
            "paramètre = entre les parenthèses de la fonction."
        ),
        "explanation": (
            "compteur est global (déclaré hors fonction), x est un paramètre "
            "(dans la signature), temp est local (déclaré dans le corps), "
            "et i est local au bloc for."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "int compteur = 0;  // avant main()"},
                {"id": "v2", "display": "void f(int x) { ... }"},
                {"id": "v3", "display": "int temp = a + b;  // dans f()"},
                {"id": "v4", "display": "for (int i = 0; ...) // dans f()"},
            ],
            "types": [
                {"id": "t1", "label": "Variable globale"},
                {"id": "t2", "label": "Paramètre de fonction"},
                {"id": "t3", "label": "Variable locale à la fonction"},
                {"id": "t4", "label": "Variable locale au bloc for"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    "z03_r11": {
        "challenge_id": "z03_r11",
        "zone": 3,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Pipeline d'Assemblage",
        "concept_tags": ["multi_fichiers", "compilation", "headers", "include"],
        "difficulty": 3,
        "question_prompt": (
            "Le pipeline d'assemblage est en panne. "
            "Remets les commandes de compilation multi-fichiers dans le bon ordre !"
        ),
        "hint": (
            "On compile d'abord chaque .c en .o (objet), puis on lie "
            "les .o ensemble pour créer l'exécutable."
        ),
        "explanation": (
            "En compilation séparée : 1) gcc -c utils.c → utils.o, "
            "2) gcc -c main.c → main.o, "
            "3) gcc utils.o main.o -o programme → édition des liens. "
            "Chaque fichier est compilé indépendamment, puis on les lie."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": "gcc -c utils.c  →  utils.o"},
                {"id": "c2", "text": "gcc -c main.c  →  main.o"},
                {"id": "c3", "text": "gcc utils.o main.o -o programme"},
                {"id": "c4", "text": "./programme"},
            ],
            "display_order": ["c4", "c3", "c1", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOM 12 : MINI-BOSS #2  (difficulté 3)
    # ─────────────────────────────────────────────────────────

    "z03_r12": {
        "challenge_id": "z03_r12",
        "zone": 3,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "memory_map",
        "title": "MINI-BOSS : Le Spectre du Scope",
        "concept_tags": ["scope", "variable_locale", "passage_par_copie", "masquage"],
        "difficulty": 3,
        "question_prompt": (
            "Le Spectre du Scope hante l'Usine ! "
            "Une variable globale x vaut 100. La fonction modifie un paramètre "
            "qui s'appelle aussi x. Après l'appel, que vaut le x global ?"
        ),
        "hint": (
            "Quand un paramètre a le même nom qu'une variable globale, "
            "il la masque à l'intérieur de la fonction. "
            "Mais le passage se fait par copie..."
        ),
        "explanation": (
            "Le paramètre x de changer() masque la variable globale x dans le corps "
            "de la fonction. De plus, le passage par copie fait que la modification "
            "de x dans changer() n'affecte que la copie locale. "
            "Le x global reste à 100."
        ),
        "payload": {
            "scenario": (
                "int x = 100;  // variable globale\n\n"
                "void changer(int x) {\n"
                "    x = x + 50;\n"
                "}\n\n"
                "int main() {\n"
                "    changer(x);\n"
                '    printf("%d", x);\n'
                "}"
            ),
            "slots": [
                {"id": "s1", "label": "x = 150 (modifié par changer)"},
                {"id": "s2", "label": "x = 100 (inchangé : copie + masquage)"},
                {"id": "s3", "label": "x = 50 (la fonction a soustrait)"},
                {"id": "s4", "label": "x = 0 (le masquage réinitialise)"},
            ],
            "correct_answer": "s2",
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOMS 13-14 : EXPERT  (difficultés 4, 4)
    # ─────────────────────────────────────────────────────────

    "z03_r13": {
        "challenge_id": "z03_r13",
        "zone": 3,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "La Spirale Récursive",
        "concept_tags": ["recursivite", "return", "appel_fonction"],
        "difficulty": 4,
        "question_prompt": (
            "La Spirale Récursive tourne sur elle-même... "
            "Quelle valeur renvoie factorielle(5) ?"
        ),
        "hint": (
            "Déroule les appels : fact(5) = 5 * fact(4) = 5 * 4 * fact(3) = ... "
            "jusqu'au cas de base fact(0) = 1."
        ),
        "explanation": (
            "factorielle(5) = 5 × 4 × 3 × 2 × 1 × 1 = 120. "
            "La récursivité fonctionne en empilant les appels jusqu'au cas "
            "de base (n == 0 → return 1), puis en les dépilant en multipliant."
        ),
        "payload": {
            "code": (
                "int factorielle(int n) {\n"
                "    if (n == 0)\n"
                "        return 1;\n"
                "    return n * factorielle(n - 1);\n"
                "}\n\n"
                "int main() {\n"
                '    printf("%d", factorielle(5));\n'
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "120",
        },
    },

    "z03_r14": {
        "challenge_id": "z03_r14",
        "zone": 3,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "L'Engrenage Infini",
        "concept_tags": ["recursivite", "cas_de_base", "stack_overflow"],
        "difficulty": 4,
        "question_prompt": (
            "L'Engrenage tourne sans jamais s'arrêter ! "
            "Cette fonction récursive provoque un stack overflow. "
            "Trouve la ligne qui contient le bug."
        ),
        "hint": (
            "Toute fonction récursive doit avoir un cas de base qui arrête "
            "la récursion. Vérifie la condition d'arrêt..."
        ),
        "explanation": (
            "À la ligne 2, la condition est n == 0, mais la fonction est "
            "appelée avec un argument négatif possible via n - 2. "
            "Si n est impair, n ne vaudra jamais exactement 0 (il passera "
            "de 1 à -1), causant une récursion infinie. "
            "Il faudrait tester n <= 0."
        ),
        "payload": {
            "code": (
                "int mystere(int n) {\n"
                "    if (n == 0)\n"
                "        return 0;\n"
                "    return n + mystere(n - 2);\n"
                "}\n\n"
                "int main() {\n"
                '    printf("%d", mystere(7));\n'
                "    return 0;\n"
                "}"
            ),
            "lines": [
                {"id": "1", "text": "int mystere(int n) {"},
                {"id": "2", "text": "    if (n == 0)"},
                {"id": "3", "text": "        return 0;"},
                {"id": "4", "text": "    return n + mystere(n - 2);"},
                {"id": "5", "text": "}"},
                {"id": "6", "text": ""},
                {"id": "7", "text": "int main() {"},
                {"id": "8", "text": '    printf("%d", mystere(7));'},
                {"id": "9", "text": "    return 0;"},
                {"id": "10", "text": "}"},
            ],
            "correct_answer": 2,
        },
    },

    # ─────────────────────────────────────────────────────────
    # ROOM 15 : BOSS FINAL  (difficulté 4)
    # ─────────────────────────────────────────────────────────

    "z03_r15": {
        "challenge_id": "z03_r15",
        "zone": 3,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "BOSS : L'Usine Récursive",
        "concept_tags": ["recursivite", "appel_fonction", "return", "scope"],
        "difficulty": 4,
        "question_prompt": (
            "L'Usine Récursive est le coeur du donjon ! "
            "Cette fonction récursive calcule une suite mystérieuse. "
            "Quelle valeur affiche le programme ?"
        ),
        "hint": (
            "C'est la suite de Fibonacci ! fib(n) = fib(n-1) + fib(n-2). "
            "Dessine l'arbre des appels en partant de fib(6)."
        ),
        "explanation": (
            "fib(6) = fib(5) + fib(4) = 5 + 3 = 8. "
            "L'arbre se déploie : fib(5)=5, fib(4)=3, fib(3)=2, fib(2)=1, "
            "fib(1)=1, fib(0)=0. C'est la célèbre suite de Fibonacci, "
            "un classique de la récursivité."
        ),
        "payload": {
            "code": (
                "int fib(int n) {\n"
                "    if (n <= 0)\n"
                "        return 0;\n"
                "    if (n == 1)\n"
                "        return 1;\n"
                "    return fib(n - 1) + fib(n - 2);\n"
                "}\n\n"
                "int main() {\n"
                '    printf("%d", fib(6));\n'
                "    return 0;\n"
                "}"
            ),
            "correct_answer": "8",
        },
    },
}
