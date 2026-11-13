import re

import lupa.lua54 as _lua54

from .lexique import decouper_lua

_LUA = _lua54.LuaRuntime(unpack_returned_tuples=True, register_eval=False,
                         register_builtins=False)

_COMPILER = _LUA.eval("""
function(src, nom)
  local f, err = load(src, '=' .. nom, 't', {})
  if f then return true end
  return false, err
end
""")

_MANIFESTE = _LUA.eval("""
function(src)
  local data = {}
  local function cle(k)
    local function chaine(v)
      data[#data + 1] = { k, v }
      return chaine
    end
    return chaine
  end
  local env = setmetatable({}, { __index = function(_, k) return cle(k) end })
  local f, err = load(src, '=fxmanifest', 't', env)
  if not f then return nil, err end
  local co = coroutine.create(f)
  debug.sethook(co, function() error('trop long', 0) end, '', 2000000)
  local ok, e = coroutine.resume(co)
  if not ok then return nil, tostring(e) end
  return data
end
""")

_BACKTICK = re.compile(r"`[^`\n]*`")
_COMPOSE = re.compile(r"(?<![=<>~\-])(//|<<|>>|[+\-*/%^&|])=(?!=)")
_NAV_SURE = re.compile(r"\?(?=[.\[:])")


def _neutraliser_cfx(src):
    if "/*" in src:
        src = decouper_lua(src, seulement_commentaires_c=True)[0]
    src = _BACKTICK.sub("0", src)
    src = _COMPOSE.sub("=", src)
    src = _NAV_SURE.sub("", src)
    return src


_TRADUCTIONS = [
    (r"'(.+?)' expected \(to close '(.+?)' at line (\d+)\)",
     lambda m: f"« {m[1]} » manquant (pour fermer le « {m[2]} » de la ligne {m[3]})"),
    (r"'(.+?)' expected", lambda m: f"« {m[1]} » attendu"),
    (r"unexpected symbol", lambda m: "symbole inattendu"),
    (r"unfinished string", lambda m: "chaîne de texte non fermée"),
    (r"unfinished long string", lambda m: "chaîne longue [[ ]] non fermée"),
    (r"unfinished long comment", lambda m: "commentaire --[[ ]] non fermé"),
    (r"malformed number", lambda m: "nombre mal écrit"),
    (r"invalid escape sequence", lambda m: "séquence d'échappement invalide"),
    (r"<name> expected", lambda m: "nom attendu"),
    (r"no visible label '(\w+)' for goto", lambda m: f"étiquette « {m[1]} » introuvable pour goto"),
    (r"label '(\w+)' already defined", lambda m: f"étiquette « {m[1]} » déjà définie"),
    (r"break outside a loop", lambda m: "« break » en dehors d'une boucle"),
    (r"attempt to assign to const variable '(\w+)'",
     lambda m: f"modification de la constante « {m[1]} »"),
    (r"too many local variables", lambda m: "plus de 200 variables locales dans une même fonction"),
    (r"function or expression needs too many registers",
     lambda m: "fonction trop grosse (trop de registres)"),
    (r"control structure too long", lambda m: "structure de contrôle trop longue"),
    (r"chunk has too many syntax levels", lambda m: "trop d'imbrications"),
    (r"near <eof>", lambda m: "en fin de fichier"),
    (r"near '(.+?)'", lambda m: f"près de « {m[1]} »"),
]


def traduire(message):
    resultat = message
    for motif, rempl in _TRADUCTIONS:
        resultat = re.sub(motif, rempl, resultat)
    return resultat


_ERREUR = re.compile(r"^src:(\d+): (.*)$", re.S)


def verifier_syntaxe(octets):
    if octets.startswith(b"\xef\xbb\xbf"):
        octets = octets[3:]
    if octets.startswith(b"#"):
        fin = octets.find(b"\n")
        octets = b"--" + octets[2:] if fin < 0 else b"--" + octets[1:]
    texte = octets.decode("latin-1")
    texte = _neutraliser_cfx(texte)
    resultat = _COMPILER(texte.encode("latin-1"), "src")
    if resultat is True:
        return None
    err = resultat[1]
    err = err.decode("utf-8", "replace") if isinstance(err, bytes) else str(err)
    m = _ERREUR.match(err)
    if not m:
        return 0, traduire(err), err
    return int(m[1]), traduire(m[2]), m[2]


def _ordre(kv):
    return (0, kv[0], "") if isinstance(kv[0], int) else (1, 0, str(kv[0]))


def _vers_python(valeur):
    if lupa_table(valeur):
        return [_vers_python(v) for _, v in sorted(valeur.items(), key=_ordre)]
    if isinstance(valeur, bytes):
        return valeur.decode("utf-8", "replace")
    return valeur


def lupa_table(v):
    return _lua54.lua_type(v) == "table"


def lire_manifeste(octets):
    if octets.startswith(b"\xef\xbb\xbf"):
        octets = octets[3:]
    resultat = _MANIFESTE(octets)
    if isinstance(resultat, tuple):
        donnees, err = resultat
    else:
        donnees, err = resultat, None
    if donnees is None:
        err = err.decode("utf-8", "replace") if isinstance(err, bytes) else str(err)
        return None, err
    paires = []
    for _, paire in sorted(donnees.items()):
        cle = paire[1]
        cle = cle.decode("utf-8", "replace") if isinstance(cle, bytes) else str(cle)
        paires.append((cle, _vers_python(paire[2])))
    return paires, None
