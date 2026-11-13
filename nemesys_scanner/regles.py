import base64
import binascii
import re
from bisect import bisect_right

from .lexique import (compter_echappements_codes, decoder_echappements,
                      lisible, part_imprimable)

NIVEAUX = ("critique", "eleve", "moyen", "info")


def baisser(niveau, crans=1):
    i = min(NIVEAUX.index(niveau) + crans, len(NIVEAUX) - 1)
    return NIVEAUX[i]


_MOTS_DANGEREUX = re.compile(
    r"PerformHttpRequest|loadstring|\bload\s*\(|https?://|ExecuteCommand|add_principal|"
    r"add_ace|os\.execute|io\.popen|SaveResourceFile|discord(?:app)?\.com/api/webhooks|"
    r"sv_licenseKey|rcon_password|\beval\s*\(|child_process|new\s+Function|"
    r"GetResourcePath|io\.open|_G\s*\[|require\s*\(",
    re.I)

_DOMAINES_CONNUS = re.compile(r"cipher-?panel|ciphercheats|blum-?panel", re.I)

_IP_BRUTE = re.compile(r"https?://\d{1,3}(?:\.\d{1,3}){3}(?::\d+)?")
_HEBERGEURS_CODE = re.compile(
    r"pastebin\.com/raw|hastebin\.com/raw|paste\.ee/r|ghostbin|rentry\.co/[^/\s]+/raw|"
    r"raw\.githubusercontent\.com|gist\.githubusercontent\.com|ngrok(?:-free)?\.(?:io|app)|"
    r"\.onion\b|transfer\.sh|discord(?:app)?\.com/api/webhooks", re.I)

_EXECUTE_CODE = re.compile(r"(?<![\w.:])(?:load|loadstring)\s*\(|(?<![\w.$])eval\s*\(|\bnew\s+Function\s*\(")
_BIDI = re.compile("[‪-‮⁦-⁩]")


def _ip_publique(texte):
    for m in _IP_BRUTE.finditer(texte):
        ip = m.group().split("//", 1)[1].split(":")[0]
        a, b = (int(x) for x in ip.split(".")[:2])
        privee = a in (0, 10, 127) or (a == 192 and b == 168) or (a == 172 and 16 <= b <= 31) \
            or (a == 169 and b == 254) or (a == 100 and 64 <= b <= 127)
        if not privee:
            return True
    return False


_LUA_HTTP = re.compile(r"\bPerformHttpRequest\b|\bPerformHttpRequestAwait\b")
_LUA_LOAD_APPEL = re.compile(r"(?<![\w.:])(load|loadstring)\s*\(")
_LUA_LOAD_ALIAS = re.compile(r"(?<![\w.:\"'])(load|loadstring)\b(?!\s*[(\w\"'])")
_LUA_GLOBALE_DYN = re.compile(r"(?<![\w.])(?:_G|_ENV|getfenv\s*\(\s*\d*\s*\))\s*\[")
_LUA_STRING_CHAR = re.compile(r"string\.char\s*\(\s*([\d\s,]{20,})\)")
_LISTE_NOMBRES = re.compile(r"\{\s*((?:\d{1,3}\s*[,;]\s*){30,}\d{1,3})\s*,?\s*\}")
_LUA_OS = re.compile(r"(?<![\w.])(?:os\.execute|io\.popen|os\.remove|os\.rename)\s*\(")
_LUA_ECRITURE = re.compile(r"(?<![\w.])io\.open\s*\(([^\n]{0,200})")
_LUA_SAVE = re.compile(r"\bSaveResourceFile\s*\(([^\n]{0,200})")
_LUA_PARCOURS_RES = re.compile(r"\bGetNumResources\b|\bGetResourceByFindIndex\b")
_CONVAR_SECRET = re.compile(
    r"GetConvar\w*\s*\(\s*['\"](sv_licenseKey|rcon_password|sv_tebexSecret|steam_webApiKey|"
    r"mysql_connection_string)['\"]", re.I)
_ACE = re.compile(r"\bExecuteCommand\s*\(([^\n]{0,200})")
_ACE_MOTS = re.compile(r"add_principal|add_ace|group\.admin|remove_principal", re.I)
_IDENTIFIANTS = re.compile(r"\bGetPlayerIdentifiers?\b|\bGetPlayerToken\b|\bGetPlayerEndpoint\b")
_ENDPOINT_IP = re.compile(r"\bGetPlayerEndpoint\b")
_ESPACES_CACHE = re.compile(r"(?<![ \t])[ \t]{150,}+(?=\S)")
_UNICODE_PIEGE = re.compile("[​‌‍⁠﻿‪-‮⁦-⁩]")
_NOMS_OBFUSQUES = re.compile(r"\b[Il1]{8,}\b|\b_0x[0-9a-fA-F]{4,6}\b")
_BASE64 = re.compile(r"^[A-Za-z0-9+/\s]{80,}={0,2}$")
_HEX = re.compile(r"^(?:[0-9a-fA-F]{2}){40,}$")

_JS_EVAL = re.compile(r"(?<![\w.$])eval\s*\(|\bnew\s+Function\s*\(|\bFunction\s*\(\s*['\"`]")
_JS_RESEAU = re.compile(r"\bhttps?\.(?:get|request)\s*\(|\bfetch\s*\(|\baxios\b|"
                        r"\bPerformHttpRequest\b|\brequire\s*\(\s*['\"](?:node-fetch|request|got)['\"]")
_JS_PROCESS = re.compile(r"\bchild_process\b|\bexecSync\s*\(|\bspawnSync\s*\(")
_JS_FS_ECRIT = re.compile(r"\b(?:writeFileSync|writeFile|appendFileSync|appendFile|createWriteStream)\s*\(([^\n]{0,200})")
_JS_BUFFER64 = re.compile(r"Buffer\.from\s*\([^)]{0,400}['\"]base64['\"]|\batob\s*\(")
_HTML_SCRIPT = re.compile(r"<script[^>]+src\s*=\s*['\"](https?:)?//([^/'\"]+)", re.I)
_CDN_SURS = re.compile(r"(?:^|\.)(?:cdnjs\.cloudflare\.com|cdn\.jsdelivr\.net|unpkg\.com|"
                       r"code\.jquery\.com|cfx-nui-|nui-game-internal|fonts\.googleapis\.com|"
                       r"cdn\.tailwindcss\.com|kit\.fontawesome\.com|ajax\.googleapis\.com|"
                       r"stackpath\.bootstrapcdn\.com|maxcdn\.bootstrapcdn\.com)$", re.I)


class Constat:
    __slots__ = ("regle", "niveau", "cle", "params", "position", "ligne", "decode")

    def __init__(self, regle, niveau, cle, position=None, ligne=None, decode=None, **params):
        self.regle = regle
        self.niveau = niveau
        self.cle = cle
        self.params = params
        self.position = position
        self.ligne = ligne
        self.decode = decode


def _decode_dangereux(texte):
    return bool(_MOTS_DANGEREUX.search(texte))


def _essayer_base64(contenu):
    compact = re.sub(r"\s+", "", contenu)
    if len(compact) % 4:
        compact += "=" * (4 - len(compact) % 4)
    try:
        brut = base64.b64decode(compact, validate=True)
    except (binascii.Error, ValueError):
        return None
    texte = brut.decode("latin-1")
    return texte if part_imprimable(texte) > 0.9 else None


def _essayer_hex(contenu):
    try:
        texte = bytes.fromhex(contenu).decode("latin-1")
    except ValueError:
        return None
    return texte if part_imprimable(texte) > 0.9 else None


def _nombres_vers_texte(liste):
    try:
        valeurs = [int(v) for v in re.findall(r"\d+", liste)]
    except ValueError:
        return None
    if not valeurs or any(v > 255 for v in valeurs):
        return None
    texte = "".join(chr(v) for v in valeurs)
    return texte if part_imprimable(texte) > 0.85 else None


def regles_communes(ctx, ajouter):
    for m in _ESPACES_CACHE.finditer(ctx.src):
        if m.end() >= len(ctx.code) or ctx.code[m.end()].isspace():
            continue
        ajouter(Constat(
            "code-cache-espaces", "critique", "code-cache-espaces", position=m.end()))
    vus = set()
    debuts_chaines = [c.debut for c in ctx.chaines]
    for m in _UNICODE_PIEGE.finditer(ctx.code):
        ligne = ctx.lignes.de(m.start())
        if ligne in vus or (m.start() == 0 and m.group() == "﻿"):
            continue
        i = bisect_right(debuts_chaines, m.start()) - 1
        dans_chaine = i >= 0 and ctx.chaines[i].fin > m.start()
        if dans_chaine and not _BIDI.match(m.group()):
            continue
        vus.add(ligne)
        ajouter(Constat(
            "unicode-invisible", "eleve", "unicode-invisible", position=m.start()))
        if len(vus) >= 5:
            break
    for ch in ctx.chaines:
        if _DOMAINES_CONNUS.search(ch.contenu):
            ajouter(Constat(
                "domaine-backdoor", "critique", "domaine-backdoor", position=ch.debut))
        elif _ip_publique(ch.contenu):
            ajouter(Constat(
                "ip-brute", "eleve", "ip-brute", position=ch.debut))
        elif _HEBERGEURS_CODE.search(ch.contenu):
            webhook = "webhooks" in ch.contenu.lower()
            proche_execution = _EXECUTE_CODE.search(
                ctx.code, max(0, ch.debut - 3000), ch.fin + 3000)
            if webhook or not proche_execution:
                continue
            ajouter(Constat(
                "hebergeur-code", "eleve", "hebergeur-code", position=ch.debut))
    for ch in ctx.chaines:
        if ch.type == "long" or len(ch.contenu) < 24:
            continue
        nb = compter_echappements_codes(ch.contenu)
        if nb >= 12 and nb * 4 >= len(ch.contenu) * 0.6:
            texte = decoder_echappements(ch.contenu)
            danger = _decode_dangereux(texte)
            ascii_lisible = sum(1 for c in texte if " " <= c <= "~") / max(1, len(texte))
            if not danger and ascii_lisible < 0.8:
                continue
            ajouter(Constat(
                "texte-echappe", "critique" if danger else "moyen", "texte-echappe.danger" if danger else "texte-echappe.simple", position=ch.debut, decode=lisible(texte)))
    for ch in ctx.chaines:
        contenu = ch.contenu.strip()
        if len(contenu) < 80 or contenu.startswith("data:"):
            continue
        texte = None
        if _HEX.match(contenu):
            texte = _essayer_hex(contenu)
        elif _BASE64.match(contenu):
            texte = _essayer_base64(contenu)
        if texte and _decode_dangereux(texte):
            ajouter(Constat(
                "texte-encode", "critique", "texte-encode", position=ch.debut, decode=lisible(texte)))
    for m in _LISTE_NOMBRES.finditer(ctx.code):
        texte = _nombres_vers_texte(m.group(1))
        if texte and _decode_dangereux(texte):
            ajouter(Constat(
                "octets-caches", "critique", "octets-caches", position=m.start(), decode=lisible(texte)))
    noms = _NOMS_OBFUSQUES.findall(ctx.code)
    if len(noms) >= 25 and not ctx.escrow:
        ajouter(Constat(
            "obfuscation", "moyen", "obfuscation", nb=len(noms), position=ctx.code.find(noms[0])))


def regles_lua(ctx, ajouter):
    code = ctx.code
    http = [m.start() for m in _LUA_HTTP.finditer(code)]
    a_lecture_locale = "LoadResourceFile" in code
    load_redefini = re.search(r"\blocal\s+function\s+load\b|\blocal\s+[\w\s,]*\bload\b\s*[=\n]",
                              code)

    for m in ([] if load_redefini else _LUA_LOAD_APPEL.finditer(code)):
        proche_http = any(0 <= m.start() - h <= 2500 for h in http)
        argument = code[m.end():m.end() + 120]
        if proche_http:
            ajouter(Constat(
                "telecharge-execute", "critique", "telecharge-execute", position=m.start()))
        elif a_lecture_locale or "LoadResourceFile" in argument:
            ajouter(Constat(
                "execution-dynamique", "info", "execution-dynamique.fichier", position=m.start()))
        else:
            ajouter(Constat(
                "execution-dynamique", "moyen", "execution-dynamique.dynamique", position=m.start()))

    for m in ([] if load_redefini else _LUA_LOAD_ALIAS.finditer(code)):
        avant = code[max(0, m.start() - 40):m.start()]
        apres = code[m.end():m.end() + 20]
        if re.match(r"[^\S\n]*=(?!=)", apres) or re.search(r"[.:]\s*$", avant):
            continue
        if re.search(r"(?<![=<>~])=[^\S\n]*$|\([^\S\n]*$|\([^()\n]*,[^\S\n]*$", avant) and \
                re.match(r"[^\S\n]*(?:$|[,)\n;}]|end\b)", apres):
            ajouter(Constat(
                "load-deguise", "eleve", "load-deguise", position=m.start()))

    if _LUA_STRING_CHAR.search(code) or _LUA_GLOBALE_DYN.search(code):
        for m in _LUA_STRING_CHAR.finditer(code):
            texte = _nombres_vers_texte(m.group(1))
            if not texte:
                continue
            danger = _decode_dangereux(texte)
            ajouter(Constat(
                "string-char", "critique" if danger else "moyen", "string-char.danger" if danger else "string-char.simple", position=m.start(), decode=lisible(texte)))
        for m in _LUA_GLOBALE_DYN.finditer(code):
            suite = code[m.end():m.end() + 80]
            if re.match(r"\s*(?:['\"][A-Za-z_]\w*['\"]|[A-Za-z_]\w*)\s*\]", suite) and \
                    not re.search(r"string\.char|\.\.|\\x|\\\d", suite):
                continue
            ajouter(Constat(
                "globale-dynamique", "eleve", "globale-dynamique", position=m.start()))

    if ctx.cote != "client":
        for m in _LUA_OS.finditer(code):
            contexte = code[max(0, m.start() - 300):m.end() + 120]
            if m.group().startswith("io.popen") and \
                    re.search(r"['\"](?:dir|ls)\b[^'\"]*['\"]", contexte):
                continue
            ajouter(Constat(
                "commande-systeme", "eleve", "commande-systeme", position=m.start()))

    parcours = bool(_LUA_PARCOURS_RES.search(code))
    for m in _LUA_SAVE.finditer(code):
        arg = m.group(1)
        premier = re.match(r"\s*([^,]+)", arg)
        premier = premier.group(1).strip() if premier else ""
        a_soi = re.match(r"GetCurrentResourceName\s*\(\s*\)$|(?:cache|shared|lib)\.resource$|"
                         r"[A-Z_]*RESOURCE[A-Z_]*$|resourceName$|currentResource$", premier) or \
            (ctx.ressource and premier.strip("'\"").lower() == ctx.ressource.lower())
        manifeste = re.search(r"fxmanifest|__resource", arg)
        if manifeste or (parcours and not a_soi):
            ajouter(Constat(
                "auto-propagation", "critique", "auto-propagation.save", position=m.start()))
    for m in _LUA_ECRITURE.finditer(code):
        arg = m.group(1)
        if re.search(r"['\"][wa]\+?b?['\"]", arg) and \
                (re.search(r"fxmanifest|__resource", arg) or
                 (parcours and "GetResourcePath" in code)):
            ajouter(Constat(
                "auto-propagation", "critique", "auto-propagation.io", position=m.start()))

    for m in _CONVAR_SECRET.finditer(code):
        nom = m.group(1)
        if nom.lower() == "mysql_connection_string":
            if not http:
                continue
            niveau = "critique"
        else:
            niveau = "critique" if http else "eleve"
        ajouter(Constat(
            "vol-secret", niveau, "vol-secret.reseau" if http else "vol-secret.seul", nom=nom, position=m.start()))

    for m in _ACE.finditer(code):
        if not _ACE_MOTS.search(m.group(1)):
            continue
        identifiant_fixe = re.search(r"(?:license2?|steam|discord|fivem|xbl|live|ip):[0-9a-fA-F.]{4,}",
                                     m.group(1))
        proche_http = any(abs(m.start() - h) <= 2000 for h in http)
        if identifiant_fixe or proche_http:
            ajouter(Constat(
                "droits-admin", "critique" if identifiant_fixe else "eleve", "droits-admin.identifiant" if identifiant_fixe else "droits-admin.reseau", identifiant=identifiant_fixe.group()[:40] if identifiant_fixe else '', position=m.start()))
        else:
            ajouter(Constat(
                "droits-admin", "info", "droits-admin.info", position=m.start()))

    if ctx.cote != "client" and http:
        webhook = any("webhooks" in ch.contenu.lower() for ch in ctx.chaines)
        sensible = _ENDPOINT_IP.search(code) or _CONVAR_SECRET.search(code)
        if webhook and sensible:
            ajouter(Constat(
                "exfiltration", "eleve", "exfiltration", position=_ENDPOINT_IP.search(code).start() if _ENDPOINT_IP.search(code)
                else http[0]))


def regles_js(ctx, ajouter):
    code = ctx.code
    appels_reseau = [m.start() for m in _JS_RESEAU.finditer(code)]
    reseau = bool(appels_reseau)
    serveur = ctx.cote == "server"
    decalage = 0 if serveur else 3

    def pres_du_reseau(pos, portee=3000):
        return any(abs(pos - r) <= portee for r in appels_reseau)

    for m in _JS_EVAL.finditer(code):
        argument = code[m.end():m.end() + 60]
        if re.match(r"\s*LoadResourceFile\s*\(", argument):
            continue
        if re.match(r"\s*['\"]return this['\"]\s*\)", argument):
            continue
        if re.match(r"\s*['\"]return function\*\s*\(\)\s*\{\s*\}['\"]\s*\)", argument):
            continue
        reseau_proche = pres_du_reseau(m.start())
        ajouter(Constat("js-eval", baisser("critique" if reseau_proche else "moyen", decalage),
                        "js-eval.reseau" if reseau_proche else "js-eval.simple",
                        position=m.start()))
    for m in _JS_PROCESS.finditer(code):
        ajouter(Constat(
            "js-processus", baisser("eleve" if pres_du_reseau(m.start()) else "moyen",
                                    decalage), "js-processus", position=m.start()))
    for m in _JS_FS_ECRIT.finditer(code):
        manifeste = re.search(r"fxmanifest|__resource", m.group(1))
        if manifeste or re.search(r"\.lua['\"`]|\.js['\"`]", m.group(1)):
            ajouter(Constat(
                "auto-propagation", "critique" if manifeste else "eleve", "auto-propagation.js-manifeste" if manifeste else "auto-propagation.js-code", position=m.start()))
    evals = [m.start() for m in _JS_EVAL.finditer(code)]
    for m in _JS_BUFFER64.finditer(code):
        if not any(abs(m.start() - e) <= 600 for e in evals):
            continue
        ajouter(Constat(
            "js-base64-eval", baisser("critique", decalage), "js-base64-eval", position=m.start()))


def regles_html(ctx, ajouter):
    for m in _HTML_SCRIPT.finditer(ctx.src):
        hote = m.group(2).split(":")[0]
        if _CDN_SURS.search(hote) or hote in ("localhost", "127.0.0.1") or \
                hote.lower().startswith(("cfx-nui-", "nui-")) or \
                re.search(r"(?:^|\.)(?:youtube\.com|ytimg\.com|vimeo\.com|"
                          r"player\.twitch\.tv)$", hote, re.I):
            continue
        ajouter(Constat(
            "script-distant", "moyen", "script-distant", hote=hote, position=m.start()))
