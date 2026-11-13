LANGUES = ("fr", "en")

M = {
    "code-cache-espaces": {
        "fr": ("Code caché hors de l'écran",
               "Cette ligne contient plus de 150 espaces avant du code. C'est l'astuce classique des "
               "backdoors : dans un éditeur, le code est poussé tout à droite et on ne le voit pas en "
               "lisant le fichier.",
               "Fais défiler la ligne vers la droite, ou supprime tout ce qui suit les espaces. Si tu "
               "n'as pas écrit ce code, la ressource est piégée."),
        "en": ("Code hidden off-screen",
               "This line has more than 150 spaces before some code. It's the classic backdoor trick: "
               "in an editor the code is pushed far to the right, so you never see it while reading "
               "the file.",
               "Scroll the line to the right, or delete everything after the spaces. If you didn't "
               "write this code, the resource is compromised."),
    },
    "unicode-invisible": {
        "fr": ("Caractère invisible dans le code",
               "Un caractère invisible (espace de largeur nulle ou inversion du sens du texte) se "
               "trouve dans le code. Il peut faire lire autre chose que ce qui s'exécute vraiment.",
               "Supprime le caractère (retape la ligne à la main)."),
        "en": ("Invisible character in the code",
               "An invisible character (zero-width space or text direction override) sits in the "
               "code. It can make the code read differently from what actually runs.",
               "Remove the character (retype the line by hand)."),
    },
    "domaine-backdoor": {
        "fr": ("Adresse d'un panel de backdoor connu",
               "Le script contacte un site connu pour piloter des serveurs FiveM infectés (prise de "
               "contrôle à distance, vol de la base, droits admin).",
               "Supprime la ressource entière, change tes mots de passe (rcon, base de données, "
               "txAdmin) et vérifie les autres ressources : ces backdoors se recopient souvent "
               "ailleurs."),
        "en": ("Known backdoor panel address",
               "The script contacts a site known for controlling infected FiveM servers (remote "
               "takeover, database theft, admin rights).",
               "Delete the whole resource, change your passwords (rcon, database, txAdmin) and check "
               "your other resources: these backdoors often copy themselves elsewhere."),
    },
    "ip-brute": {
        "fr": ("Connexion vers une adresse IP brute",
               "Le script contacte directement une adresse IP au lieu d'un nom de domaine. Les vrais "
               "services utilisent un nom de domaine ; une IP brute sert souvent à cacher un serveur "
               "pirate.",
               "Vérifie à qui appartient cette IP et à quoi sert l'envoi."),
        "en": ("Connection to a raw IP address",
               "The script talks to an IP address directly instead of a domain name. Real services "
               "use domain names; a raw IP is often used to hide an attacker's server.",
               "Check who owns this IP and what is being sent."),
    },
    "hebergeur-code": {
        "fr": ("Téléchargement depuis un hébergeur de texte",
               "Le script vise un site où n'importe qui peut déposer du texte (pastebin, GitHub brut, "
               "ngrok…). Combiné à une exécution de code, c'est une backdoor qui peut changer à tout "
               "moment.",
               "Regarde ce qui est fait de la réponse. Si elle est exécutée, supprime la ressource."),
        "en": ("Download from a paste site",
               "The script targets a site where anyone can host text (pastebin, raw GitHub, ngrok…). "
               "Combined with code execution, it's a backdoor whose payload can change at any time.",
               "Check what is done with the response. If it gets executed, delete the resource."),
    },
    "texte-echappe.danger": {
        "fr": ("Texte caché avec des codes \\x / \\nnn",
               "Cette chaîne est écrite entièrement en codes de caractères pour qu'on ne puisse pas la "
               "lire. Une fois décodée, elle contient du code dangereux (voir ci-dessous).",
               "Lis le texte décodé. Un script honnête n'a aucune raison de cacher ses textes."),
        "en": ("Text hidden with \\x / \\nnn escapes",
               "This string is written entirely as character codes so nobody can read it. Once "
               "decoded, it contains dangerous code (see below).",
               "Read the decoded text. An honest script has no reason to hide its strings."),
    },
    "texte-echappe.simple": {
        "fr": ("Texte caché avec des codes \\x / \\nnn",
               "Cette chaîne est écrite entièrement en codes de caractères pour qu'on ne puisse pas la "
               "lire. Le texte décodé est affiché ci-dessous.",
               "Lis le texte décodé. Un script honnête n'a aucune raison de cacher ses textes."),
        "en": ("Text hidden with \\x / \\nnn escapes",
               "This string is written entirely as character codes so nobody can read it. The decoded "
               "text is shown below.",
               "Read the decoded text. An honest script has no reason to hide its strings."),
    },
    "texte-encode": {
        "fr": ("Code caché en base64 / hexadécimal",
               "Une longue chaîne encodée contient, une fois décodée, du code ou une adresse "
               "dangereuse.",
               "Lis le texte décodé ci-dessous. Si tu ne sais pas pourquoi il est là, supprime la "
               "ressource."),
        "en": ("Code hidden in base64 / hex",
               "A long encoded string contains dangerous code or a dangerous address once decoded.",
               "Read the decoded text below. If you don't know why it's there, delete the resource."),
    },
    "octets-caches": {
        "fr": ("Code caché dans une liste de nombres",
               "Cette liste de nombres, transformée en lettres, donne du code dangereux. C'est la "
               "technique utilisée par plusieurs backdoors FiveM connues.",
               "Lis le texte décodé ci-dessous et supprime la ressource si tu ne l'as pas écrit."),
        "en": ("Code hidden in a list of numbers",
               "Turned into letters, this list of numbers spells dangerous code. Several known FiveM "
               "backdoors use this technique.",
               "Read the decoded text below and delete the resource if you didn't write it."),
    },
    "obfuscation": {
        "fr": ("Code volontairement illisible (obfusqué)",
               "Le fichier contient {nb} noms de variables du type « IlIlIIl » ou « _0x3f2a ». C'est la "
               "marque d'un obfuscateur : on ne peut pas savoir ce que fait le code en le lisant.",
               "Si c'est un script payant d'un créateur connu, c'est normal. Sinon, ne fais pas "
               "confiance à ce fichier."),
        "en": ("Deliberately unreadable (obfuscated) code",
               "The file has {nb} variable names like “IlIlIIl” or “_0x3f2a”. That's the mark of an "
               "obfuscator: you can't tell what the code does by reading it.",
               "Normal for a paid script from a known creator. Otherwise, don't trust this file."),
    },
    "telecharge-execute": {
        "fr": ("Code téléchargé puis exécuté",
               "Le script fait une requête internet (PerformHttpRequest) et exécute ensuite du code "
               "avec load(). C'est exactement le fonctionnement des backdoors : le pirate envoie le "
               "code qu'il veut, quand il veut, et il tourne sur ton serveur avec tous les droits.",
               "Supprime la ressource. Change le mot de passe rcon, celui de la base de données et de "
               "txAdmin, puis analyse tout le serveur."),
        "en": ("Code downloaded then executed",
               "The script makes a web request (PerformHttpRequest) and then runs code with load(). "
               "That's exactly how backdoors work: the attacker sends whatever code they want, "
               "whenever they want, and it runs on your server with full rights.",
               "Delete the resource. Change your rcon, database and txAdmin passwords, then scan the "
               "whole server."),
    },
    "execution-dynamique.fichier": {
        "fr": ("Exécution de code chargé depuis un fichier",
               "Le script exécute du code avec load(), lu depuis un fichier de la ressource. C'est "
               "courant (chargeurs de modules, ox_lib…).",
               "Rien à faire si le fichier chargé vient bien de la ressource."),
        "en": ("Runs code loaded from a file",
               "The script runs code with load(), read from a file of the resource. This is common "
               "(module loaders, ox_lib…).",
               "Nothing to do if the loaded file really belongs to the resource."),
    },
    "execution-dynamique.dynamique": {
        "fr": ("Exécution de code dynamique (load)",
               "Le script transforme un texte en code avec load() et l'exécute. Selon l'origine du "
               "texte, cela peut servir à faire tourner du code caché.",
               "Vérifie d'où vient le texte passé à load()."),
        "en": ("Dynamic code execution (load)",
               "The script turns a string into code with load() and runs it. Depending on where the "
               "string comes from, this can be used to run hidden code.",
               "Check where the string passed to load() comes from."),
    },
    "load-deguise": {
        "fr": ("load() caché dans une variable",
               "La fonction load est copiée dans une variable ou passée en paramètre. C'est une façon "
               "de cacher une exécution de code à la recherche.",
               "Regarde ce que la variable exécute ensuite."),
        "en": ("load() hidden in a variable",
               "The load function is copied into a variable or passed as an argument. It's a way to "
               "hide code execution from searches.",
               "Check what the variable runs afterwards."),
    },
    "string-char.danger": {
        "fr": ("Texte caché avec string.char",
               "Le script fabrique un texte lettre par lettre avec string.char pour qu'on ne puisse pas "
               "le chercher. Décodé, il contient du code dangereux.",
               "Lis le texte décodé ci-dessous."),
        "en": ("Text hidden with string.char",
               "The script builds a string letter by letter with string.char so it can't be searched "
               "for. Decoded, it contains dangerous code.",
               "Read the decoded text below."),
    },
    "string-char.simple": {
        "fr": ("Texte caché avec string.char",
               "Le script fabrique un texte lettre par lettre avec string.char pour qu'on ne puisse pas "
               "le chercher.",
               "Lis le texte décodé ci-dessous."),
        "en": ("Text hidden with string.char",
               "The script builds a string letter by letter with string.char so it can't be searched "
               "for.",
               "Read the decoded text below."),
    },
    "globale-dynamique": {
        "fr": ("Fonction appelée par un nom fabriqué",
               "Le script appelle une fonction globale (_G[…]) dont le nom est construit à la volée. "
               "Ça sert à cacher des appels comme load ou PerformHttpRequest.",
               "Regarde quel nom est construit entre les crochets."),
        "en": ("Function called through a built name",
               "The script calls a global function (_G[…]) whose name is built on the fly. This hides "
               "calls such as load or PerformHttpRequest.",
               "Check which name is built between the brackets."),
    },
    "commande-systeme": {
        "fr": ("Commande système Windows / Linux",
               "Le script lance des commandes sur la machine qui héberge le serveur (os.execute, "
               "io.popen) ou supprime des fichiers. Un script de jeu n'en a presque jamais besoin.",
               "Vérifie exactement quelle commande est lancée."),
        "en": ("Windows / Linux system command",
               "The script runs commands on the machine hosting the server (os.execute, io.popen) or "
               "deletes files. A game script almost never needs this.",
               "Check exactly which command is run."),
    },
    "auto-propagation.save": {
        "fr": ("Écrit dans le code d'autres ressources",
               "Le script parcourt les ressources du serveur ou modifie un fxmanifest "
               "(SaveResourceFile). C'est comme ça qu'une backdoor se recopie partout pour survivre à "
               "la suppression de la ressource d'origine.",
               "Supprime la ressource, puis analyse tout le serveur et compare chaque fxmanifest à une "
               "version propre."),
        "en": ("Writes into other resources' code",
               "The script walks through the server's resources or edits an fxmanifest "
               "(SaveResourceFile). That's how a backdoor copies itself everywhere to survive the "
               "deletion of the original resource.",
               "Delete the resource, then scan the whole server and compare each fxmanifest with a "
               "clean copy."),
    },
    "auto-propagation.io": {
        "fr": ("Modifie les fichiers Lua du serveur",
               "Le script ouvre des fichiers .lua ou des fxmanifest en écriture. Une ressource normale "
               "ne réécrit jamais le code des autres.",
               "Supprime la ressource et vérifie les fxmanifest de tout le serveur."),
        "en": ("Modifies the server's Lua files",
               "The script opens .lua files or fxmanifests for writing. A normal resource never "
               "rewrites other resources' code.",
               "Delete the resource and check the fxmanifests of the whole server."),
    },
    "vol-secret.reseau": {
        "fr": ("Lecture du secret « {nom} »",
               "Le script lit « {nom} », un secret du serveur, et fait aussi des requêtes internet : il "
               "peut l'envoyer à quelqu'un.",
               "Si ce n'est pas une ressource de confiance (oxmysql, txAdmin…), supprime-la et change "
               "ce secret."),
        "en": ("Reads the “{nom}” secret",
               "The script reads “{nom}”, a server secret, and also makes web requests: it can send "
               "it to someone.",
               "Unless it's a trusted resource (oxmysql, txAdmin…), delete it and change this secret."),
    },
    "vol-secret.seul": {
        "fr": ("Lecture du secret « {nom} »",
               "Le script lit « {nom} », un secret du serveur. Aucune ressource de jeu n'a besoin de le "
               "lire.",
               "Si ce n'est pas une ressource de confiance (oxmysql, txAdmin…), supprime-la et change "
               "ce secret."),
        "en": ("Reads the “{nom}” secret",
               "The script reads “{nom}”, a server secret. No gameplay resource needs to read it.",
               "Unless it's a trusted resource (oxmysql, txAdmin…), delete it and change this secret."),
    },
    "droits-admin.identifiant": {
        "fr": ("Donne des droits admin à quelqu'un",
               "Le script exécute add_principal / add_ace pour un identifiant écrit en dur "
               "({identifiant}). C'est la signature d'une backdoor qui donne les droits admin à son "
               "auteur.",
               "Vérifie à qui les droits sont donnés. Supprime la ligne si ce n'est pas toi."),
        "en": ("Gives admin rights to someone",
               "The script runs add_principal / add_ace for a hard-coded identifier ({identifiant}). "
               "That's the signature of a backdoor granting admin rights to its author.",
               "Check who gets the rights. Remove the line if it isn't you."),
    },
    "droits-admin.reseau": {
        "fr": ("Donne des droits admin à quelqu'un",
               "Le script exécute add_principal / add_ace et fait aussi des requêtes internet : les "
               "droits peuvent être donnés à distance.",
               "Vérifie à qui les droits sont donnés. Supprime la ligne si ce n'est pas toi."),
        "en": ("Gives admin rights to someone",
               "The script runs add_principal / add_ace and also makes web requests: rights can be "
               "granted remotely.",
               "Check who gets the rights. Remove the line if it isn't you."),
    },
    "droits-admin.info": {
        "fr": ("Gère les groupes de permissions",
               "Le script donne ou retire des groupes avec add_principal / add_ace. C'est normal pour "
               "un framework (ESX, QBCore) ou un menu admin.",
               "Rien à faire si c'est un script de confiance."),
        "en": ("Manages permission groups",
               "The script grants or removes groups with add_principal / add_ace. Normal for a "
               "framework (ESX, QBCore) or an admin menu.",
               "Nothing to do if it's a trusted script."),
    },
    "exfiltration": {
        "fr": ("Envoie des IP ou des secrets vers Discord",
               "Le script récupère l'adresse IP des joueurs ou un secret du serveur et fait des envois "
               "vers un webhook Discord.",
               "Vérifie le contenu exact envoyé. Les IP des joueurs sont des données personnelles."),
        "en": ("Sends IPs or secrets to Discord",
               "The script collects players' IP addresses or a server secret and sends data to a "
               "Discord webhook.",
               "Check exactly what is sent. Players' IP addresses are personal data."),
    },
    "js-eval.reseau": {
        "fr": ("Code téléchargé puis exécuté (eval)",
               "Le fichier fait des requêtes internet et exécute du texte comme du code (eval / new "
               "Function). Un pirate peut y faire tourner ce qu'il veut.",
               "Vérifie d'où vient le texte exécuté."),
        "en": ("Code downloaded then executed (eval)",
               "The file makes web requests and runs text as code (eval / new Function). An attacker "
               "can run anything through it.",
               "Check where the executed text comes from."),
    },
    "js-eval.simple": {
        "fr": ("Exécution de texte comme du code (eval)",
               "eval / new Function transforment un texte en code. Fréquent dans les bibliothèques "
               "compressées, dangereux dans un script serveur.",
               "Vérifie d'où vient le texte exécuté."),
        "en": ("Text executed as code (eval)",
               "eval / new Function turn a string into code. Common in minified libraries, dangerous "
               "in a server script.",
               "Check where the executed text comes from."),
    },
    "js-processus": {
        "fr": ("Lance des programmes sur la machine",
               "Le script utilise child_process pour lancer des commandes sur la machine du serveur.",
               "Un script FiveM n'en a quasiment jamais besoin : vérifie la commande lancée."),
        "en": ("Launches programs on the machine",
               "The script uses child_process to run commands on the server machine.",
               "A FiveM script almost never needs this: check the command being run."),
    },
    "auto-propagation.js-manifeste": {
        "fr": ("Réécrit des fichiers de code",
               "Le script écrit dans des fxmanifest : c'est ainsi qu'une backdoor se recopie dans les "
               "autres ressources. Certains outils de développement le font aussi.",
               "Vérifie quels fichiers sont écrits. Si tu ne connais pas ce script, supprime-le et "
               "vérifie les autres fxmanifest."),
        "en": ("Rewrites code files",
               "The script writes into fxmanifest files: that's how a backdoor copies itself into other "
               "resources. Some development tools do it too.",
               "Check which files are written. If you don't know this script, delete it and check the "
               "other fxmanifests."),
    },
    "auto-propagation.js-code": {
        "fr": ("Réécrit des fichiers de code",
               "Le script écrit dans des fichiers .lua / .js : c'est ainsi qu'une backdoor se recopie "
               "dans les autres ressources. Certains outils de développement le font aussi.",
               "Vérifie quels fichiers sont écrits. Si tu ne connais pas ce script, supprime-le et "
               "vérifie les autres fxmanifest."),
        "en": ("Rewrites code files",
               "The script writes .lua / .js files: that's how a backdoor copies itself into other "
               "resources. Some development tools do it too.",
               "Check which files are written. If you don't know this script, delete it and check the "
               "other fxmanifests."),
    },
    "js-base64-eval": {
        "fr": ("Code base64 décodé puis exécuté",
               "Le fichier décode du base64 et utilise eval / new Function : du code est caché dans "
               "une chaîne encodée.",
               "Décode la chaîne (un site de décodage base64 suffit) pour voir ce qu'elle cache."),
        "en": ("Base64 code decoded then executed",
               "The file decodes base64 and uses eval / new Function: code is hidden in an encoded "
               "string.",
               "Decode the string (any base64 decoder works) to see what it hides."),
    },
    "script-distant": {
        "fr": ("Script chargé depuis {hote}",
               "L'interface charge du JavaScript depuis un site externe. Si ce site change le fichier, "
               "il change le comportement de ton interface en jeu.",
               "Télécharge le fichier et mets-le dans la ressource, ou utilise un CDN connu."),
        "en": ("Script loaded from {hote}",
               "The interface loads JavaScript from an external site. If that site changes the file, "
               "it changes how your in-game interface behaves.",
               "Download the file into the resource, or use a well-known CDN."),
    },
    "bytecode": {
        "fr": ("Fichier Lua compilé (illisible)",
               "Ce fichier .lua est du bytecode compilé, pas du texte. On ne peut pas lire ce qu'il "
               "fait.",
               "Demande la version source ou supprime le fichier."),
        "en": ("Compiled Lua file (unreadable)",
               "This .lua file is compiled bytecode, not text. There's no way to read what it does.",
               "Ask for the source version or delete the file."),
    },
    "syntaxe-lua.charge": {
        "fr": ("Erreur de syntaxe", "{message}",
               "Corrige la ligne indiquée : tant que l'erreur est là, aucun code de ce fichier ne "
               "s'exécute."),
        "en": ("Syntax error", "{message}",
               "Fix the line shown: while the error is there, none of this file's code runs."),
    },
    "syntaxe-lua.non-charge": {
        "fr": ("Erreur de syntaxe", "{message}",
               "Ce fichier n'est pas déclaré dans un fxmanifest : c'est peut-être un fichier de données "
               "ou un brouillon. S'il est chargé par un script, corrige la ligne indiquée."),
        "en": ("Syntax error", "{message}",
               "This file isn't declared in any fxmanifest: it may be a data file or a draft. If a "
               "script loads it, fix the line shown."),
    },
    "syntaxe-lua.manifeste": {
        "fr": ("Erreur de syntaxe", "{message}",
               "Corrige la ligne indiquée : la ressource ne démarrera pas."),
        "en": ("Syntax error", "{message}",
               "Fix the line shown: the resource won't start."),
    },
    "syntaxe-json": {
        "fr": ("Erreur dans un fichier JSON", "{message}",
               "Corrige la ligne indiquée (virgule en trop ou manquante, guillemet oublié…)."),
        "en": ("Error in a JSON file", "{message}",
               "Fix the line shown (extra or missing comma, missing quote…)."),
    },
    "ressource-double": {
        "fr": ("Ressource « {nom} » présente {nb} fois",
               "Le même nom de ressource existe à plusieurs endroits ({chemins}). FiveM n'en démarre "
               "qu'une, au hasard de l'ordre de lecture : tu peux modifier l'une alors que c'est "
               "l'autre qui tourne.",
               "Supprime ou renomme les copies inutiles."),
        "en": ("Resource “{nom}” found {nb} times",
               "The same resource name exists in several places ({chemins}). FiveM starts only one, "
               "depending on read order: you may edit one while the other is the one running.",
               "Delete or rename the unneeded copies."),
    },
    "manifeste-dynamique": {
        "fr": ("fxmanifest non lu entièrement",
               "Le fxmanifest utilise des instructions que l'analyse ne simule pas ({err}). Les "
               "fichiers listés n'ont pas été vérifiés.",
               "Rien à faire si la ressource démarre."),
        "en": ("fxmanifest not fully read",
               "The fxmanifest uses instructions the scan doesn't simulate ({err}). Listed files were "
               "not checked.",
               "Nothing to do if the resource starts."),
    },
    "fx-version": {
        "fr": ("fx_version manquant",
               "Le fxmanifest ne précise pas fx_version. FiveM affiche un avertissement et peut "
               "refuser certaines fonctions.",
               "Ajoute fx_version 'cerulean' en haut du fichier."),
        "en": ("Missing fx_version",
               "The fxmanifest doesn't set fx_version. FiveM shows a warning and may refuse some "
               "features.",
               "Add fx_version 'cerulean' at the top of the file."),
    },
    "fichier-manquant.autre": {
        "fr": ("Fichier introuvable : {entree}",
               "Le fxmanifest charge « {entree} », mais ce fichier n'existe pas dans la ressource "
               "{ressource}.",
               "Corrige le chemin (attention aux majuscules sur Linux)."),
        "en": ("File not found: {entree}",
               "The fxmanifest loads “{entree}”, but this file doesn't exist in the {ressource} "
               "resource.",
               "Fix the path (mind upper/lower case on Linux)."),
    },
    "fichier-manquant": {
        "fr": ("Fichier introuvable : {entree}",
               "Le fxmanifest déclare « {entree} » ({cle}), mais ce fichier n'existe pas.{indice}",
               "Corrige le chemin ou retire la ligne."),
        "en": ("File not found: {entree}",
               "The fxmanifest declares “{entree}” ({cle}), but this file doesn't exist.{indice}",
               "Fix the path or remove the line."),
    },
    "motif-vide": {
        "fr": ("Aucun fichier pour « {entree} »",
               "Le motif « {entree} » ({cle}) ne correspond à aucun fichier.",
               "Vérifie le chemin ou retire la ligne."),
        "en": ("No file matches “{entree}”",
               "The pattern “{entree}” ({cle}) doesn't match any file.",
               "Check the path or remove the line."),
    },
    "ensure-absent": {
        "fr": ("« {commande} {nom} » : ressource introuvable",
               "{fichier} démarre « {nom} », mais aucune ressource de ce nom n'a été trouvée.",
               "Corrige le nom ou retire la ligne."),
        "en": ("“{commande} {nom}”: resource not found",
               "{fichier} starts “{nom}”, but no resource with this name was found.",
               "Fix the name or remove the line."),
    },
    "admin-cfg": {
        "fr": ("{groupe} donné à {identifiant}",
               "{fichier} donne le groupe {groupe} à cet identifiant. Vérifie que tu connais chaque "
               "personne listée : une backdoor peut ajouter son auteur ici.",
               "Retire les identifiants que tu ne reconnais pas."),
        "en": ("{groupe} given to {identifiant}",
               "{fichier} gives the {groupe} group to this identifier. Make sure you know every person "
               "listed: a backdoor can add its author here.",
               "Remove any identifier you don't recognise."),
    },
}

INDICE_CASSE = {
    "fr": " Un fichier « {voisin} » existe : seule la casse diffère, ça marche sous Windows mais "
          "pas sous Linux.",
    "en": " A file named “{voisin}” exists: only the case differs, which works on Windows but not "
          "on Linux.",
}


def rediger(cle_message, /, **params):
    sortie = {}
    for langue in LANGUES:
        valeurs = {k: (v[langue] if isinstance(v, dict) else v) for k, v in params.items()}
        titre, explication, conseil = M[cle_message][langue]
        sortie[langue] = {
            "titre": titre.format(**valeurs),
            "explication": explication.format(**valeurs),
            "conseil": conseil.format(**valeurs),
        }
    return sortie
