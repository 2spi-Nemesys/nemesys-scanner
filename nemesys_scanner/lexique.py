import re
from bisect import bisect_right

_LUA_JETON = re.compile(r"--|/\*|[\"'`]|\[=*\[")
_LUA_LONG = re.compile(r"\[(=*)\[")
_LUA_CHAINE = {
    '"': re.compile(r'"(?:[^"\\\n]|\\[\s\S])*"?'),
    "'": re.compile(r"'(?:[^'\\\n]|\\[\s\S])*'?"),
    "`": re.compile(r"`[^`\n]*`?"),
}

_JS_JETON = re.compile(r"//|/\*|/|[\"'`]")
_JS_AVANT_REGEX = re.compile(r"(?:^|[(,=:\[!&|?{};+\-*%<>~^]|\breturn|\btypeof|\bcase|\bdo|"
                             r"\belse|\bin|\bof|\bvoid|\bdelete|\bnew|\bthrow|\byield|\bawait)\s*$")
_JS_REGEX = re.compile(r"/(?:[^/\\\[\n]|\\.|\[(?:[^\]\\\n]|\\.)*\])+/[a-z]*")
_JS_CHAINE = {
    '"': re.compile(r'"(?:[^"\\\n]|\\[\s\S])*"?'),
    "'": re.compile(r"'(?:[^'\\\n]|\\[\s\S])*'?"),
    "`": re.compile(r"`(?:[^`\\]|\\[\s\S])*`?"),
}

_PAS_SAUT = re.compile(r"[^\n]")


def _blanc(segment):
    return _PAS_SAUT.sub(" ", segment)


class Chaine:
    __slots__ = ("debut", "fin", "contenu", "type")

    def __init__(self, debut, fin, contenu, type_):
        self.debut = debut
        self.fin = fin
        self.contenu = contenu
        self.type = type_


def decouper_lua(src, seulement_commentaires_c=False):
    sortie, chaines = [], []
    i, n = 0, len(src)
    while True:
        m = _LUA_JETON.search(src, i)
        if not m:
            sortie.append(src[i:])
            break
        d = m.start()
        sortie.append(src[i:d])
        jeton = m.group()
        if jeton == "/*":
            f = src.find("*/", d + 2)
            f = n if f < 0 else f + 2
            sortie.append(_blanc(src[d:f]))
            i = f
        elif jeton == "--" and seulement_commentaires_c:
            lg = _LUA_LONG.match(src, d + 2)
            if lg:
                fermeture = "]" + lg.group(1) + "]"
                f = src.find(fermeture, lg.end())
                f = n if f < 0 else f + len(fermeture)
            else:
                f = src.find("\n", d)
                f = n if f < 0 else f
            sortie.append(src[d:f])
            i = f
        elif jeton == "--":
            lg = _LUA_LONG.match(src, d + 2)
            if lg:
                fermeture = "]" + lg.group(1) + "]"
                f = src.find(fermeture, lg.end())
                f = n if f < 0 else f + len(fermeture)
            else:
                f = src.find("\n", d)
                f = n if f < 0 else f
            sortie.append(_blanc(src[d:f]))
            i = f
        elif jeton in ('"', "'", "`"):
            ms = _LUA_CHAINE[jeton].match(src, d)
            f = ms.end()
            fin_contenu = f - 1 if f - d >= 2 and src[f - 1] == jeton else f
            chaines.append(Chaine(d, f, src[d + 1:fin_contenu], jeton))
            sortie.append(src[d:f])
            i = f
        else:
            niveau = len(jeton) - 2
            fermeture = "]" + "=" * niveau + "]"
            f = src.find(fermeture, m.end())
            fin_contenu = n if f < 0 else f
            f = n if f < 0 else f + len(fermeture)
            chaines.append(Chaine(d, f, src[m.end():fin_contenu], "long"))
            sortie.append(src[d:f])
            i = f
    return "".join(sortie), chaines


def decouper_js(src):
    sortie, chaines = [], []
    i, n = 0, len(src)
    while True:
        m = _JS_JETON.search(src, i)
        if not m:
            sortie.append(src[i:])
            break
        d = m.start()
        sortie.append(src[i:d])
        jeton = m.group()
        if jeton == "//":
            f = src.find("\n", d)
            f = n if f < 0 else f
            sortie.append(_blanc(src[d:f]))
            i = f
        elif jeton == "/*":
            f = src.find("*/", d + 2)
            f = n if f < 0 else f + 2
            sortie.append(_blanc(src[d:f]))
            i = f
        elif jeton == "/":
            if _JS_AVANT_REGEX.search(src, max(0, d - 12), d):
                mr = _JS_REGEX.match(src, d)
                if mr:
                    sortie.append(mr.group())
                    i = mr.end()
                    continue
            sortie.append("/")
            i = d + 1
        else:
            ms = _JS_CHAINE[jeton].match(src, d)
            f = ms.end()
            fin_contenu = f - 1 if f - d >= 2 and src[f - 1] == jeton else f
            chaines.append(Chaine(d, f, src[d + 1:fin_contenu], jeton))
            sortie.append(src[d:f])
            i = f
    return "".join(sortie), chaines


class Lignes:

    def __init__(self, src):
        self.debuts = [0]
        pos = src.find("\n")
        while pos >= 0:
            self.debuts.append(pos + 1)
            pos = src.find("\n", pos + 1)

    def de(self, position):
        return bisect_right(self.debuts, position)


_ECHAP_SIMPLE = {"n": "\n", "t": "\t", "r": "\r", "a": "\a", "b": "\b",
                 "f": "\f", "v": "\v", "\\": "\\", '"': '"', "'": "'", "\n": "\n"}
_ECHAP = re.compile(r"\\(x[0-9a-fA-F]{2}|\d{1,3}|u\{[0-9a-fA-F]+\}|u[0-9a-fA-F]{4}|z\s*|[\s\S])")


def decoder_echappements(contenu):
    def remplace(m):
        e = m.group(1)
        if e[0] == "x":
            return chr(int(e[1:], 16))
        if e[0].isdigit():
            v = int(e)
            return chr(v) if v < 256 else "?"
        if e[0] == "u" and len(e) == 5:
            return chr(int(e[1:], 16))
        if e[0] == "u" and e[1:2] == "{":
            try:
                return chr(int(e[2:-1], 16))
            except (ValueError, OverflowError):
                return "?"
        if e[0] == "z":
            return ""
        return _ECHAP_SIMPLE.get(e, e)
    return _ECHAP.sub(remplace, contenu)


def compter_echappements_codes(contenu):
    return len(re.findall(r"\\(?:x[0-9a-fA-F]{2}|\d{1,3}|u[0-9a-fA-F]{4}|u\{[0-9a-fA-F]+\})", contenu))


def lisible(texte, limite=400):
    propre = "".join(c if (c.isprintable() or c in "\n\t") else "·" for c in texte)
    propre = propre.strip()
    return propre if len(propre) <= limite else propre[:limite] + " …"


def part_imprimable(texte):
    if not texte:
        return 0.0
    ok = sum(1 for c in texte if c.isprintable() or c in "\n\t\r")
    return ok / len(texte)
