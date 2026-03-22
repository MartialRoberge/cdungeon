"""
Zone 8 — File Sanctum
Cours 9 : fichiers en C (fopen, fclose, modes, fprintf, fscanf, fgets,
fputs, fread, fwrite, fseek, ftell, binaire, serialisation).
15 salles : intro (1-4) → consolidation (5-7) → mini-boss (8) →
maîtrise (9-11) → mini-boss (12) → expert (13-14) → boss (15).
"""

from app.content.challenge_types import ChallengeData

ZONE_8_CHALLENGES: dict[str, ChallengeData] = {

    # ===================================================================
    # ROOM 1 — Intro — difficulté 2
    # ===================================================================
    "z08_r01": {
        "challenge_id": "z08_r01",
        "zone": 8,
        "room": 1,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Les Portes du Sanctuaire",
        "concept_tags": ["fopen", "modes"],
        "difficulty": 2,
        "question_prompt": (
            "Chaque porte du Sanctuaire s'ouvre avec le bon mode. "
            "Associe chaque action à son mode d'ouverture de fichier."
        ),
        "hint": (
            "\"r\" = lecture seule, \"w\" = écriture (efface le contenu), "
            "\"a\" = ajout en fin de fichier, \"rb\" = lecture binaire."
        ),
        "explanation": (
            "fopen utilise un mode en 2e argument : \"r\" pour lire, \"w\" pour "
            "écrire (écrase), \"a\" pour ajouter, et le suffixe \"b\" indique "
            "le mode binaire."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "Lire un fichier texte"},
                {"id": "v2", "display": "Écrire en écrasant tout"},
                {"id": "v3", "display": "Ajouter à la fin"},
                {"id": "v4", "display": "Lire un fichier binaire"},
            ],
            "types": [
                {"id": "t1", "label": "\"r\""},
                {"id": "t2", "label": "\"w\""},
                {"id": "t3", "label": "\"a\""},
                {"id": "t4", "label": "\"rb\""},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    # ===================================================================
    # ROOM 2 — Intro — difficulté 3
    # ===================================================================
    "z08_r02": {
        "challenge_id": "z08_r02",
        "zone": 8,
        "room": 2,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "La Clé de Lecture",
        "concept_tags": ["fopen", "fclose"],
        "difficulty": 3,
        "question_prompt": (
            "Un parchemin est resté ouvert trop longtemps et les runes "
            "s'effacent ! Complète le code pour ouvrir correctement le fichier."
        ),
        "hint": (
            "fopen prend le chemin du fichier et le mode en arguments. "
            "N'oublie pas de vérifier si le fichier est bien ouvert."
        ),
        "explanation": (
            "fopen(\"chemin\", \"mode\") retourne un FILE* ou NULL si le "
            "fichier n'existe pas. Il faut TOUJOURS tester le retour de fopen."
        ),
        "payload": {
            "code_before": 'FILE *f = ',
            "blank_label": "???",
            "code_after": (
                ';\nif (f == NULL) {\n'
                '    printf("Erreur ouverture\\n");\n'
                '    return 1;\n'
                '}\n// lecture...\nfclose(f);'
            ),
            "options": [
                'fopen("data.txt", "r")',
                'fopen("data.txt")',
                'open("data.txt", "r")',
                'fread("data.txt", "r")',
            ],
            "correct_answer": 'fopen("data.txt", "r")',
        },
    },

    # ===================================================================
    # ROOM 3 — Intro — difficulté 3
    # ===================================================================
    "z08_r03": {
        "challenge_id": "z08_r03",
        "zone": 8,
        "room": 3,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Parchemin Corrompu",
        "concept_tags": ["fclose", "fopen", "fuite_ressource"],
        "difficulty": 3,
        "question_prompt": (
            "Ce code compile mais provoque une fuite de ressource. "
            "Trouve la ligne qui pose problème !"
        ),
        "hint": (
            "Chaque fopen doit avoir son fclose correspondant. "
            "Regarde bien si le fichier est fermé."
        ),
        "explanation": (
            "La ligne 6 fait un return sans fermer le fichier. "
            "Il faut appeler fclose(f) avant tout return pour "
            "éviter les fuites de ressources."
        ),
        "payload": {
            "code": (
                'FILE *f = fopen("log.txt", "w");\n'
                'if (f == NULL) return 1;\n'
                'fprintf(f, "Hello");\n'
                'int x = 42;\n'
                'if (x > 0) {\n'
                '    return 0;  // Bug ici\n'
                '}\n'
                'fclose(f);'
            ),
            "lines": [
                {"id": "1", "text": 'FILE *f = fopen("log.txt", "w");'},
                {"id": "2", "text": "if (f == NULL) return 1;"},
                {"id": "3", "text": 'fprintf(f, "Hello");'},
                {"id": "4", "text": "int x = 42;"},
                {"id": "5", "text": "if (x > 0) {"},
                {"id": "6", "text": "    return 0;"},
                {"id": "7", "text": "}"},
                {"id": "8", "text": "fclose(f);"},
            ],
            "correct_answer": 6,
        },
    },

    # ===================================================================
    # ROOM 4 — Intro — difficulté 3
    # ===================================================================
    "z08_r04": {
        "challenge_id": "z08_r04",
        "zone": 8,
        "room": 4,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "L'Encre Magique",
        "concept_tags": ["fprintf", "fichier_ecriture"],
        "difficulty": 3,
        "question_prompt": (
            "Le scribe enchante son parchemin avec fprintf. "
            "Que contient le fichier après exécution ?"
        ),
        "hint": (
            "fprintf fonctionne exactement comme printf, mais écrit "
            "dans un fichier au lieu de la console."
        ),
        "explanation": (
            "fprintf(f, ...) écrit dans le fichier f. Avec le mode \"w\", "
            "le fichier est créé (ou vidé), puis on écrit \"Score: 100\\n\" "
            "suivi de \"Niveau: 5\\n\"."
        ),
        "payload": {
            "code": (
                'FILE *f = fopen("save.txt", "w");\n'
                'int score = 100;\n'
                'int niveau = 5;\n'
                'fprintf(f, "Score: %d\\n", score);\n'
                'fprintf(f, "Niveau: %d\\n", niveau);\n'
                'fclose(f);'
            ),
            "correct_answer": "Score: 100\\nNiveau: 5\\n",
        },
    },

    # ===================================================================
    # ROOM 5 — Consolidation — difficulté 3
    # ===================================================================
    "z08_r05": {
        "challenge_id": "z08_r05",
        "zone": 8,
        "room": 5,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "sort_order",
        "title": "Le Rituel de Sauvegarde",
        "concept_tags": ["fopen", "fprintf", "fclose", "workflow"],
        "difficulty": 3,
        "question_prompt": (
            "Pour sauvegarder dans un fichier, il faut suivre le rituel "
            "dans le bon ordre. Remets les étapes en ordre !"
        ),
        "hint": (
            "On ouvre d'abord, on vérifie que ça a marché, on écrit, "
            "puis on ferme. Toujours."
        ),
        "explanation": (
            "Le workflow fichier en C est : 1) fopen pour ouvrir, "
            "2) vérifier le retour (NULL = erreur), 3) écrire avec "
            "fprintf/fputs, 4) fclose pour fermer proprement."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": 'FILE *f = fopen("data.txt", "w");'},
                {"id": "c2", "text": "if (f == NULL) { return 1; }"},
                {"id": "c3", "text": 'fprintf(f, "Hello %d", 42);'},
                {"id": "c4", "text": "fclose(f);"},
            ],
            "display_order": ["c3", "c4", "c1", "c2"],
            "correct_answer": ["c1", "c2", "c3", "c4"],
        },
    },

    # ===================================================================
    # ROOM 6 — Consolidation — difficulté 3
    # ===================================================================
    "z08_r06": {
        "challenge_id": "z08_r06",
        "zone": 8,
        "room": 6,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "La Lecture des Runes",
        "concept_tags": ["fscanf", "fgets", "lecture"],
        "difficulty": 3,
        "question_prompt": (
            "Le mage veut lire une ligne entière depuis un parchemin. "
            "Quelle fonction utiliser ?"
        ),
        "hint": (
            "fscanf lit mot par mot (s'arrête aux espaces). "
            "fgets lit une ligne complète (avec les espaces)."
        ),
        "explanation": (
            "fgets(buf, taille, f) lit au plus taille-1 caractères "
            "ou jusqu'au \\n. Contrairement à fscanf, fgets conserve "
            "les espaces et est plus sûr (pas de dépassement de buffer)."
        ),
        "payload": {
            "code_before": (
                'char ligne[256];\n'
                'FILE *f = fopen("grimoire.txt", "r");\n'
            ),
            "blank_label": "???",
            "code_after": (
                '\nprintf("Lu: %s", ligne);\n'
                'fclose(f);'
            ),
            "options": [
                "fgets(ligne, 256, f);",
                "fscanf(f, \"%s\", ligne);",
                "fread(ligne, 256, f);",
                "fputs(ligne, f);",
            ],
            "correct_answer": "fgets(ligne, 256, f);",
        },
    },

    # ===================================================================
    # ROOM 7 — Consolidation — difficulté 4
    # ===================================================================
    "z08_r07": {
        "challenge_id": "z08_r07",
        "zone": 8,
        "room": 7,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "La Carte des Flux",
        "concept_tags": ["fopen", "modes", "fichier"],
        "difficulty": 3,
        "question_prompt": (
            "Le Sanctuaire possède plusieurs coffres. Chaque coffre "
            "représente un flux ouvert. Clique sur le coffre qui "
            "correspond à un fichier ouvert en mode AJOUT."
        ),
        "hint": (
            "Le mode \"a\" (append) ouvre un fichier en écriture "
            "sans effacer le contenu existant — on écrit à la fin."
        ),
        "explanation": (
            "Le mode \"a\" permet d'ajouter du contenu à la fin du "
            "fichier sans l'écraser. C'est le mode idéal pour les "
            "fichiers de log."
        ),
        "payload": {
            "scenario": (
                "Trois fichiers sont ouverts :\n"
                "  Coffre A → fopen(\"scores.txt\", \"r\")\n"
                "  Coffre B → fopen(\"log.txt\", \"a\")\n"
                "  Coffre C → fopen(\"config.txt\", \"w\")"
            ),
            "slots": [
                {"id": "s1", "label": "Coffre A — mode lecture (\"r\")"},
                {"id": "s2", "label": "Coffre B — mode ajout (\"a\")"},
                {"id": "s3", "label": "Coffre C — mode écriture (\"w\")"},
            ],
            "correct_answer": "s2",
        },
    },

    # ===================================================================
    # ROOM 8 — MINI-BOSS 1 — difficulté 4
    # ===================================================================
    "z08_r08": {
        "challenge_id": "z08_r08",
        "zone": 8,
        "room": 8,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "find_bug",
        "title": "MINI-BOSS : Le Gardien des Modes",
        "concept_tags": ["fopen", "modes", "fprintf", "fclose"],
        "difficulty": 4,
        "question_prompt": (
            "Le Gardien des Modes a piégé ce code ! Il tente d'écrire "
            "dans un fichier, mais le mode est mauvais. Trouve le bug !"
        ),
        "hint": (
            "Pour écrire dans un fichier, il faut un mode d'écriture : "
            "\"w\" ou \"a\". Le mode \"r\" ne permet que la lecture."
        ),
        "explanation": (
            "Le fichier est ouvert en mode \"r\" (lecture seule) mais "
            "le code essaie d'écrire avec fprintf. Il faut utiliser "
            "\"w\" ou \"a\" pour pouvoir écrire."
        ),
        "payload": {
            "code": (
                '#include <stdio.h>\n'
                'int main() {\n'
                '    FILE *f = fopen("resultat.txt", "r");\n'
                '    if (f == NULL) return 1;\n'
                '    fprintf(f, "Score: %d\\n", 42);\n'
                '    fclose(f);\n'
                '    return 0;\n'
                '}'
            ),
            "lines": [
                {"id": "1", "text": "#include <stdio.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": '    FILE *f = fopen("resultat.txt", "r");'},
                {"id": "4", "text": "    if (f == NULL) return 1;"},
                {"id": "5", "text": '    fprintf(f, "Score: %d\\n", 42);'},
                {"id": "6", "text": "    fclose(f);"},
                {"id": "7", "text": "    return 0;"},
                {"id": "8", "text": "}"},
            ],
            "correct_answer": 3,
        },
    },

    # ===================================================================
    # ROOM 9 — Maîtrise — difficulté 4
    # ===================================================================
    "z08_r09": {
        "challenge_id": "z08_r09",
        "zone": 8,
        "room": 9,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Curseur Enchanté",
        "concept_tags": ["fseek", "ftell", "position"],
        "difficulty": 4,
        "question_prompt": (
            "Un curseur magique se déplace dans le fichier. "
            "Après ces opérations, quelle est la position retournée "
            "par ftell ?"
        ),
        "hint": (
            "fseek(f, offset, SEEK_SET) place le curseur à 'offset' "
            "octets depuis le début du fichier. ftell retourne la "
            "position courante."
        ),
        "explanation": (
            "Le fichier contient \"ABCDEFGHIJ\" (10 octets). "
            "fseek(f, 5, SEEK_SET) place le curseur à la position 5 "
            "(après 'E'). ftell retourne donc 5."
        ),
        "payload": {
            "code": (
                '// Fichier contient : "ABCDEFGHIJ"\n'
                'FILE *f = fopen("runes.txt", "r");\n'
                'fseek(f, 5, SEEK_SET);\n'
                'long pos = ftell(f);\n'
                'printf("%ld", pos);\n'
                'fclose(f);'
            ),
            "correct_answer": "5",
        },
    },

    # ===================================================================
    # ROOM 10 — Maîtrise — difficulté 4
    # ===================================================================
    "z08_r10": {
        "challenge_id": "z08_r10",
        "zone": 8,
        "room": 10,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "match_types",
        "title": "Le Bestiaire des Fonctions",
        "concept_tags": ["fprintf", "fscanf", "fgets", "fputs", "fread", "fwrite"],
        "difficulty": 4,
        "question_prompt": (
            "Le Bestiaire contient les descriptions des créatures-fonctions. "
            "Associe chaque fonction à son rôle."
        ),
        "hint": (
            "fprintf = écriture formatée, fscanf = lecture formatée, "
            "fgets = lire une ligne, fwrite = écriture binaire."
        ),
        "explanation": (
            "fprintf et fscanf sont les équivalents fichier de printf/scanf. "
            "fgets lit une ligne entière. fwrite écrit des blocs binaires "
            "bruts (structures, tableaux)."
        ),
        "payload": {
            "values": [
                {"id": "v1", "display": "fprintf"},
                {"id": "v2", "display": "fscanf"},
                {"id": "v3", "display": "fgets"},
                {"id": "v4", "display": "fwrite"},
            ],
            "types": [
                {"id": "t1", "label": "Écriture formatée dans un fichier"},
                {"id": "t2", "label": "Lecture formatée depuis un fichier"},
                {"id": "t3", "label": "Lire une ligne complète"},
                {"id": "t4", "label": "Écriture binaire brute"},
            ],
            "correct_answer": {"v1": "t1", "v2": "t2", "v3": "t3", "v4": "t4"},
        },
    },

    # ===================================================================
    # ROOM 11 — Maîtrise — difficulté 4
    # ===================================================================
    "z08_r11": {
        "challenge_id": "z08_r11",
        "zone": 8,
        "room": 11,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "fill_blank",
        "title": "L'Archive Binaire",
        "concept_tags": ["fwrite", "binaire", "struct"],
        "difficulty": 4,
        "question_prompt": (
            "Le gardien veut sauvegarder une structure en binaire. "
            "Complète l'appel à fwrite pour écrire le joueur dans le fichier."
        ),
        "hint": (
            "fwrite prend 4 arguments : pointeur sur les données, "
            "taille d'un élément, nombre d'éléments, flux fichier."
        ),
        "explanation": (
            "fwrite(&player, sizeof(Player), 1, f) écrit 1 élément "
            "de taille sizeof(Player) depuis l'adresse &player dans "
            "le fichier f. C'est la sérialisation binaire."
        ),
        "payload": {
            "code_before": (
                "typedef struct { char nom[50]; int score; } Player;\n"
                "Player player = {\"Gandalf\", 9001};\n"
                'FILE *f = fopen("save.bin", "wb");\n'
            ),
            "blank_label": "???",
            "code_after": (
                "\nfclose(f);"
            ),
            "options": [
                "fwrite(&player, sizeof(Player), 1, f);",
                "fprintf(f, \"%s %d\", player.nom, player.score);",
                "fwrite(player, sizeof(Player), 1, f);",
                "fwrite(&player, 1, sizeof(Player), stdout);",
            ],
            "correct_answer": "fwrite(&player, sizeof(Player), 1, f);",
        },
    },

    # ===================================================================
    # ROOM 12 — MINI-BOSS 2 — difficulté 4
    # ===================================================================
    "z08_r12": {
        "challenge_id": "z08_r12",
        "zone": 8,
        "room": 12,
        "is_boss": False,
        "is_mini_boss": True,
        "challenge_type": "sort_order",
        "title": "MINI-BOSS : Le Spectre Binaire",
        "concept_tags": ["fwrite", "fread", "fseek", "binaire", "serialisation"],
        "difficulty": 4,
        "question_prompt": (
            "Le Spectre Binaire te met au défi ! Remets dans l'ordre "
            "les étapes pour sauvegarder une structure en binaire "
            "puis la relire."
        ),
        "hint": (
            "On écrit d'abord : ouvrir en \"wb\", fwrite, fermer. "
            "Puis on relit : ouvrir en \"rb\", fread, fermer."
        ),
        "explanation": (
            "Sérialisation binaire : 1) ouvrir en \"wb\", "
            "2) fwrite la structure, 3) fclose. "
            "Désérialisation : 4) ouvrir en \"rb\", "
            "5) fread dans une variable, 6) fclose. "
            "C'est le cycle complet de persistance binaire."
        ),
        "payload": {
            "cards": [
                {"id": "c1", "text": 'FILE *fw = fopen("save.bin", "wb");'},
                {"id": "c2", "text": "fwrite(&data, sizeof(Data), 1, fw);"},
                {"id": "c3", "text": "fclose(fw);"},
                {"id": "c4", "text": 'FILE *fr = fopen("save.bin", "rb");'},
                {"id": "c5", "text": "fread(&copie, sizeof(Data), 1, fr);"},
                {"id": "c6", "text": "fclose(fr);"},
            ],
            "display_order": ["c4", "c2", "c6", "c1", "c5", "c3"],
            "correct_answer": ["c1", "c2", "c3", "c4", "c5", "c6"],
        },
    },

    # ===================================================================
    # ROOM 13 — Expert — difficulté 5
    # ===================================================================
    "z08_r13": {
        "challenge_id": "z08_r13",
        "zone": 8,
        "room": 13,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "trace_value",
        "title": "Le Parchemin à Rebours",
        "concept_tags": ["fseek", "ftell", "SEEK_END", "SEEK_CUR"],
        "difficulty": 5,
        "question_prompt": (
            "Le curseur magique se déplace dans un fichier de 20 octets. "
            "Après ces opérations de fseek, quelle position affiche ftell ?"
        ),
        "hint": (
            "SEEK_END place le curseur par rapport à la fin du fichier. "
            "SEEK_CUR déplace par rapport à la position courante. "
            "Un offset négatif recule."
        ),
        "explanation": (
            "Le fichier fait 20 octets. fseek(f, -5, SEEK_END) place "
            "le curseur à 20-5 = position 15. Puis fseek(f, -3, SEEK_CUR) "
            "recule de 3 : 15-3 = position 12. ftell retourne donc 12."
        ),
        "payload": {
            "code": (
                '// Fichier de 20 octets\n'
                'FILE *f = fopen("map.bin", "rb");\n'
                'fseek(f, -5, SEEK_END);\n'
                'fseek(f, -3, SEEK_CUR);\n'
                'long pos = ftell(f);\n'
                'printf("%ld", pos);\n'
                'fclose(f);'
            ),
            "correct_answer": "12",
        },
    },

    # ===================================================================
    # ROOM 14 — Expert — difficulté 5
    # ===================================================================
    "z08_r14": {
        "challenge_id": "z08_r14",
        "zone": 8,
        "room": 14,
        "is_boss": False,
        "is_mini_boss": False,
        "challenge_type": "find_bug",
        "title": "Le Grimoire Piégé",
        "concept_tags": ["fread", "fwrite", "sizeof", "binaire"],
        "difficulty": 5,
        "question_prompt": (
            "Ce code sauvegarde un tableau de 5 entiers en binaire "
            "puis le relit, mais le résultat est faux. Trouve le bug !"
        ),
        "hint": (
            "fread et fwrite prennent : pointeur, taille d'un élément, "
            "nombre d'éléments, flux. Vérifie que la taille et le "
            "nombre correspondent."
        ),
        "explanation": (
            "À la ligne 7, fread utilise sizeof(int*) au lieu de "
            "sizeof(int). sizeof(int*) est la taille d'un pointeur "
            "(8 octets sur 64 bits), pas d'un int (4 octets). "
            "Il faut sizeof(int) pour relire correctement."
        ),
        "payload": {
            "code": (
                '#include <stdio.h>\n'
                'int main() {\n'
                '    int tab[5] = {10, 20, 30, 40, 50};\n'
                '    FILE *f = fopen("tab.bin", "wb");\n'
                '    fwrite(tab, sizeof(int), 5, f);\n'
                '    fclose(f);\n'
                '    int lu[5];\n'
                '    f = fopen("tab.bin", "rb");\n'
                '    fread(lu, sizeof(int*), 5, f);  // Bug\n'
                '    fclose(f);\n'
                '    return 0;\n'
                '}'
            ),
            "lines": [
                {"id": "1", "text": "#include <stdio.h>"},
                {"id": "2", "text": "int main() {"},
                {"id": "3", "text": "    int tab[5] = {10, 20, 30, 40, 50};"},
                {"id": "4", "text": '    FILE *f = fopen("tab.bin", "wb");'},
                {"id": "5", "text": "    fwrite(tab, sizeof(int), 5, f);"},
                {"id": "6", "text": "    fclose(f);"},
                {"id": "7", "text": "    int lu[5];"},
                {"id": "8", "text": '    f = fopen("tab.bin", "rb");'},
                {"id": "9", "text": "    fread(lu, sizeof(int*), 5, f);"},
                {"id": "10", "text": "    fclose(f);"},
                {"id": "11", "text": "    return 0;"},
                {"id": "12", "text": "}"},
            ],
            "correct_answer": 9,
        },
    },

    # ===================================================================
    # ROOM 15 — BOSS — difficulté 5
    # ===================================================================
    "z08_r15": {
        "challenge_id": "z08_r15",
        "zone": 8,
        "room": 15,
        "is_boss": True,
        "is_mini_boss": False,
        "challenge_type": "memory_map",
        "title": "BOSS : Le Gardien du Sanctuaire",
        "concept_tags": [
            "fopen", "fclose", "fseek", "ftell", "fwrite",
            "fread", "binaire", "serialisation",
        ],
        "difficulty": 5,
        "question_prompt": (
            "Le Gardien du Sanctuaire protège l'archive ultime. "
            "Un programme sérialise 3 structures Player (chacune de 64 octets) "
            "dans un fichier binaire. On veut relire UNIQUEMENT le 2e joueur. "
            "Quel fseek est correct pour positionner le curseur avant le fread ?"
        ),
        "hint": (
            "Le 1er joueur est à l'offset 0, le 2e à l'offset 1×64 = 64, "
            "le 3e à 2×64 = 128. On part du début avec SEEK_SET."
        ),
        "explanation": (
            "Chaque Player fait 64 octets. Le 2e joueur commence à "
            "l'offset 64 (= 1 × sizeof(Player)). Il faut donc "
            "fseek(f, 64, SEEK_SET) — ou de manière plus propre "
            "fseek(f, 1 * sizeof(Player), SEEK_SET) — puis fread "
            "pour lire exactement un Player."
        ),
        "payload": {
            "scenario": (
                "Fichier binaire \"hall_of_fame.bin\" contenant 3 structures "
                "Player de 64 octets chacune.\n"
                "Joueur 1 : offset 0–63\n"
                "Joueur 2 : offset 64–127\n"
                "Joueur 3 : offset 128–191\n\n"
                "On veut lire le joueur 2 uniquement. "
                "Quel appel fseek utiliser ?"
            ),
            "slots": [
                {"id": "s1", "label": "fseek(f, 0, SEEK_SET)      → début du joueur 1"},
                {"id": "s2", "label": "fseek(f, 64, SEEK_SET)     → début du joueur 2"},
                {"id": "s3", "label": "fseek(f, 128, SEEK_SET)    → début du joueur 3"},
                {"id": "s4", "label": "fseek(f, -64, SEEK_END)    → 64 avant la fin"},
            ],
            "correct_answer": "s2",
        },
    },
}
