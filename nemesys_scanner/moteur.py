import json
import os
import re
import time
from pathlib import Path

from . import lua as moteur_lua
from .lexique import Lignes, decouper_js, decouper_lua
from .textes import INDICE_CASSE, rediger
from .regles import (NIVEAUX, regles_communes, regles_html, regles_js,
                     regles_lua)

VERSION = "1.0.0"
TAILLE_MAX = 8 * 1024 * 1024
DOSSIERS_IGNORES = {".git", ".svn", ".vs", ".idea", "__pycache__", "cache"}
EXTENSIONS = {".lua", ".js", ".mjs", ".cjs", ".json", ".html", ".htm"}
DOSSIERS_NUI = {"html", "ui", "web", "nui", "dist", "build", "public", "client-ui"}
CLES_FICHIERS = {
    "client_script": "client", "client_scripts": "client",
    "server_script": "server", "server_scripts": "server",
    "shared_script": "shared", "shared_scripts": "shared",
    "file": "fichier", "files": "fichier", "ui_page": "fichier", "loadscreen": "fichier",
}
PENALITES = {"critique": 30, "eleve": 8, "moyen": 2, "info": 0}


class Contexte:
    def __init__(self, src, code, chaines, cote, escrow, ressource=None):
        self.ressource = ressource
        self.src = src
        self.code = code
        self.chaines = chaines
        self.cote = cote
        self.escrow = escrow
        self.lignes = Lignes(src)


class Ressource:
    def __init__(self, nom, dossier):
        self.nom = nom
        self.dossier = dossier
        self.cotes = {}
        self.lua54 = False
        self.escrow = False
        self.fichiers = 0
        self.manifeste = None

    def cote_de(self, relatif):
        return self.cotes.get(relatif)


def _calculer_score(compte, erreurs_syntaxe):
    if compte.get("critique"):
        return max(0, 30 - 6 * (compte["critique"] - 1))
    score = 100
    score -= min(35, 7 * compte.get("eleve", 0))
    score -= min(15, compte.get("moyen", 0))
    score -= min(15, 3 * erreurs_syntaxe)
    if compte.get("eleve"):
        score = min(score, 80)
    return max(35, score)


def _extrait(lignes_texte, ligne, autour=3):
    if not ligne:
        return []
    debut = max(1, ligne - autour)
    fin = min(len(lignes_texte), ligne + autour)
    sortie = []
    for n in range(debut, fin + 1):
        texte = lignes_texte[n - 1].rstrip("\r")
        if len(texte) > 320:
            texte = texte[:320] + " …"
        sortie.append({"n": n, "t": texte})
    return sortie


class Analyse:
    def __init__(self, racine, progression=None, inclure_node_modules=False,
                 arret=None):
        self.racine = Path(racine).resolve()
        self.progression = progression or (lambda *a: None)
        self.inclure_node_modules = inclure_node_modules
        self.arret = arret or (lambda: False)
        self.problemes = []
        self.ressources = {}
        self.stats = {"fichiers": 0, "lua": 0, "js": 0, "json": 0, "html": 0,
                      "lignes": 0, "ressources": 0, "octets": 0}
        self._vus = set()
        self._groupes = {}

    def _ajouter(self, categorie, niveau, regle, cle_message, params,
                 chemin, ressource, ligne=None, lignes_texte=None, decode=None,
                 brut=None):
        textes = rediger(cle_message, **(params or {}))
        relatif = chemin.relative_to(self.racine).as_posix() if chemin else ""
        cle = (regle, relatif, ligne)
        if cle in self._vus:
            return
        self._vus.add(cle)
        groupe = (regle, relatif, niveau)
        deja = self._groupes.get(groupe)
        if deja is not None and deja["repetitions"] >= 3:
            deja["autres"] += 1
            return
        if deja is not None:
            deja["repetitions"] += 1
        else:
            self._groupes[groupe] = {"repetitions": 1, "autres": 0}
        self.problemes.append({
            "groupe": self._groupes[groupe],
            "id": len(self.problemes) + 1,
            "categorie": categorie,
            "niveau": niveau,
            "regle": regle,
            "titre": textes["fr"]["titre"],
            "explication": textes["fr"]["explication"],
            "conseil": textes["fr"]["conseil"],
            "en": textes["en"],
            "fichier": relatif,
            "chemin": str(chemin) if chemin else "",
            "ressource": ressource.nom if ressource else "(hors ressource)",
            "ligne": ligne,
            "extrait": _extrait(lignes_texte, ligne) if lignes_texte else [],
            "decode": decode,
            "brut": brut,
        })

    def _lister(self):
        fichiers = []
        manifestes = []
        for dossier, sous, noms in os.walk(self.racine):
            if self.arret():
                break
            sous[:] = [s for s in sous if s.lower() not in DOSSIERS_IGNORES and
                       (self.inclure_node_modules or s != "node_modules")]
            for nom in noms:
                bas = nom.lower()
                if bas in ("fxmanifest.lua", "__resource.lua"):
                    manifestes.append(Path(dossier) / nom)
                if bas.endswith(".fxap"):
                    manifestes.append(Path(dossier) / nom)
                if os.path.splitext(bas)[1] in EXTENSIONS:
                    fichiers.append(Path(dossier) / nom)
        return fichiers, manifestes

    def _charger_ressources(self, manifestes):
        escrows = {p.parent for p in manifestes if p.suffix.lower() == ".fxap"}
        vrais = [p for p in manifestes if p.suffix.lower() != ".fxap"]
        par_dossier = {}
        for p in vrais:
            if p.parent not in par_dossier or p.name.lower() == "fxmanifest.lua":
                par_dossier[p.parent] = p
        noms = {}
        for dossier, manifeste in sorted(par_dossier.items()):
            res = Ressource(dossier.name, dossier)
            res.manifeste = manifeste
            res.escrow = any(e == dossier or dossier in e.parents for e in escrows)
            self.ressources[dossier] = res
            noms.setdefault(dossier.name.lower(), []).append(dossier)
        self.stats["ressources"] = len(self.ressources)
        for nom, dossiers in noms.items():
            if len(dossiers) > 1:
                chemins = ", ".join(d.relative_to(self.racine).as_posix() for d in dossiers)
                for d in dossiers:
                    self._ajouter(
                        "manifeste", "moyen", "ressource-double", "ressource-double",
                        {"nom": d.name, "nb": len(dossiers), "chemins": chemins},
                        self.ressources[d].manifeste, self.ressources[d])

    def _lire_manifeste(self, res):
        octets = res.manifeste.read_bytes()
        texte = octets.decode("utf-8", "replace")
        lignes_texte = texte.split("\n")
        erreur = moteur_lua.verifier_syntaxe(octets)
        if erreur:
            ligne, message, brut = erreur
            self._ajouter("syntaxe", "eleve", "syntaxe-lua", "syntaxe-lua.manifeste",
                          {"message": {"fr": message, "en": brut}},
                          res.manifeste, res, ligne or None, lignes_texte, brut=brut)
            return
        paires, err = moteur_lua.lire_manifeste(octets)
        if paires is None:
            self._ajouter("manifeste", "info", "manifeste-dynamique", "manifeste-dynamique",
                          {"err": err}, res.manifeste, res)
            return
        a_version = False
        for cle, valeur in paires:
            if cle == "fx_version":
                a_version = True
            if cle == "lua54" and str(valeur).lower() == "yes":
                res.lua54 = True
            cote = CLES_FICHIERS.get(cle)
            if not cote:
                continue
            for entree in (valeur if isinstance(valeur, list) else [valeur]):
                if not isinstance(entree, str) or not entree:
                    continue
                self._resoudre_entree(res, cle, cote, entree, lignes_texte)
        if not a_version and res.manifeste.name.lower() == "fxmanifest.lua":
            self._ajouter("manifeste", "moyen", "fx-version", "fx-version", None,
                          res.manifeste, res, 1, lignes_texte)

    def _ligne_de(self, lignes_texte, texte):
        for i, l in enumerate(lignes_texte, 1):
            if texte in l:
                return i
        return None

    def _resoudre_entree(self, res, cle, cote, entree, lignes_texte):
        if re.match(r"^(?:https?:)?//", entree) or entree.startswith("nui://"):
            return
        entree_propre = entree.split("?")[0].split("#")[0]
        if entree_propre.startswith("@"):
            nom_autre, _, chemin_autre = entree_propre[1:].partition("/")
            autres = [d for d in self.ressources if d.name.lower() == nom_autre.lower()]
            if not autres or not chemin_autre:
                return
            for autre in autres:
                if (autre / chemin_autre).exists():
                    return
            self._ajouter("manifeste", "eleve", "fichier-manquant", "fichier-manquant.autre",
                          {"entree": entree, "ressource": nom_autre},
                          res.manifeste, res, self._ligne_de(lignes_texte, entree),
                          lignes_texte)
            return
        if "*" in entree_propre:
            motif = entree_propre.replace("[", "[[]").replace("?", "[?]")
            try:
                trouves = [p for p in res.dossier.glob(motif) if p.is_file()]
            except (ValueError, OSError):
                trouves = []
            for p in trouves:
                rel = p.relative_to(res.dossier).as_posix()
                res.cotes.setdefault(rel, cote)
            if not trouves and cote != "fichier":
                self._ajouter("manifeste", "moyen", "motif-vide", "motif-vide",
                              {"entree": entree, "cle": cle}, res.manifeste, res, self._ligne_de(lignes_texte, entree),
                              lignes_texte)
            return
        cible = res.dossier / entree_propre
        if cible.exists():
            res.cotes.setdefault(entree_propre.replace("\\", "/").lstrip("./"), cote)
            return
        indice = {"fr": "", "en": ""}
        parent = cible.parent
        if parent.exists():
            for voisin in parent.iterdir():
                if voisin.name.lower() == cible.name.lower():
                    indice = {l: INDICE_CASSE[l].format(voisin=voisin.name) for l in INDICE_CASSE}
                    break
        self._ajouter("manifeste", "eleve" if cote != "fichier" else "moyen",
                      "fichier-manquant", "fichier-manquant",
                      {"entree": entree, "cle": cle, "indice": indice},
                      res.manifeste, res, self._ligne_de(lignes_texte, entree),
                      lignes_texte)

    def _ressource_de(self, chemin):
        for parent in chemin.parents:
            if parent in self.ressources:
                return self.ressources[parent]
            if parent == self.racine:
                break
        return None

    def _cote(self, res, chemin, ext):
        if res:
            rel = chemin.relative_to(res.dossier).as_posix()
            cote = res.cote_de(rel)
            if cote in ("client", "server", "shared"):
                return cote
            parties = {p.lower() for p in Path(rel).parts[:-1]}
            if cote == "fichier" or parties & DOSSIERS_NUI:
                return "nui" if ext != ".lua" else "client"
        if ext == ".lua":
            return "inconnu"
        parties = {p.lower() for p in chemin.relative_to(self.racine).parts[:-1]}
        if ext in (".cjs", ".mjs") or not parties & DOSSIERS_NUI:
            return "server"
        return "nui"

    def _analyser_fichier(self, chemin):
        try:
            taille = chemin.stat().st_size
        except OSError:
            return
        if taille > TAILLE_MAX or taille == 0:
            return
        try:
            octets = chemin.read_bytes()
        except OSError:
            return
        ext = chemin.suffix.lower()
        res = self._ressource_de(chemin)
        if res:
            res.fichiers += 1
        self.stats["fichiers"] += 1
        self.stats["octets"] += taille
        if res and res.manifeste == chemin:
            self.stats["lua"] += 1
            return
        texte = octets.decode("utf-8", "replace")
        lignes_texte = texte.split("\n")
        self.stats["lignes"] += len(lignes_texte)
        escrow = bool(res and res.escrow)

        def ajouter_constats(constats, ctx):
            for c in constats:
                ligne = c.ligne or (ctx.lignes.de(c.position) if c.position is not None else None)
                self._ajouter("backdoor", c.niveau, c.regle, c.cle, c.params,
                              chemin, res, ligne, lignes_texte, c.decode)

        if ext == ".lua":
            self.stats["lua"] += 1
            if octets.startswith(b"\x1bLua"):
                self._ajouter("backdoor", "eleve", "bytecode", "bytecode", None, chemin, res)
                return
            if escrow and not _ressemble_texte(octets):
                return
            erreur = moteur_lua.verifier_syntaxe(octets)
            if erreur:
                ligne, message, brut = erreur
                charge = res and self._cote(res, chemin, ext) != "inconnu"
                self._ajouter("syntaxe", "eleve" if charge else "moyen", "syntaxe-lua",
                              "syntaxe-lua.charge" if charge else "syntaxe-lua.non-charge",
                              {"message": {"fr": message, "en": _premiere_majuscule(brut)}},
                              chemin, res, ligne or None, lignes_texte, brut=brut)
            code, chaines = decouper_lua(texte)
            ctx = Contexte(texte, code, chaines, self._cote(res, chemin, ext), escrow,
                           res.nom if res else None)
            constats = []
            regles_communes(ctx, constats.append)
            regles_lua(ctx, constats.append)
            ajouter_constats(constats, ctx)
        elif ext in (".js", ".mjs", ".cjs"):
            self.stats["js"] += 1
            code, chaines = decouper_js(texte)
            ctx = Contexte(texte, code, chaines, self._cote(res, chemin, ext), escrow)
            constats = []
            regles_communes(ctx, constats.append)
            regles_js(ctx, constats.append)
            ajouter_constats(constats, ctx)
        elif ext == ".json":
            self.stats["json"] += 1
            try:
                json.loads(octets.decode("utf-8-sig"))
            except UnicodeDecodeError:
                pass
            except json.JSONDecodeError as e:
                self._ajouter("syntaxe", "moyen", "syntaxe-json", "syntaxe-json",
                              {"message": {"fr": _traduire_json(e),
                                           "en": f"{e.msg} (line {e.lineno}, column {e.colno})"}},
                              chemin, res, e.lineno,
                              lignes_texte, brut=e.msg)
        elif ext in (".html", ".htm"):
            self.stats["html"] += 1
            ctx = Contexte(texte, texte, [], "nui", escrow)
            constats = []
            regles_html(ctx, constats.append)
            ajouter_constats(constats, ctx)

    def _verifier_cfg(self):
        candidats = [self.racine / "server.cfg", self.racine.parent / "server.cfg"]
        cfg = next((c for c in candidats if c.is_file()), None)
        if not cfg:
            return
        noms = {d.name.lower() for d in self.ressources}
        categories = set()
        for d in self.ressources:
            for p in d.parents:
                if p.name.startswith("[") and p.name.endswith("]"):
                    categories.add(p.name.lower())
        deja = set()
        file_cfg = [cfg]
        while file_cfg:
            courant = file_cfg.pop()
            if courant in deja or not courant.is_file():
                continue
            deja.add(courant)
            texte = courant.read_text("utf-8", "replace")
            lignes_texte = texte.split("\n")
            for n, ligne in enumerate(lignes_texte, 1):
                propre = ligne.split("#")[0].strip()
                m = re.match(r"^(ensure|start|restart)\s+(\S+)", propre, re.I)
                if m:
                    nom = m.group(2).strip("\"'")
                    if nom.lower() not in noms and nom.lower() not in categories:
                        self._ajouter("config", "moyen", "ensure-absent", "ensure-absent",
                                      {"commande": m.group(1), "nom": nom,
                                       "fichier": courant.name},
                                      courant, None, n, lignes_texte)
                    continue
                m = re.match(r"^exec\s+(\S+)", propre, re.I)
                if m:
                    file_cfg.append((courant.parent / m.group(1).strip("\"'")).resolve())
                    continue
                m = re.match(r"^add_principal\s+(identifier\.\S+)\s+(group\.\S+)", propre, re.I)
                if m:
                    self._ajouter("config", "info", "admin-cfg", "admin-cfg",
                                  {"groupe": m.group(2), "identifiant": m.group(1)[:60],
                                   "fichier": courant.name},
                                  courant, None, n, lignes_texte)

    def lancer(self):
        debut = time.time()
        self.progression("liste", 0, 0, "")
        fichiers, manifestes = self._lister()
        self._charger_ressources(manifestes)
        total = len(self.ressources) + len(fichiers)
        self.progression("ressources", 0, total,
                         [{"nom": r.nom, "chemin": r.dossier.relative_to(self.racine).as_posix()}
                          for r in self.ressources.values()])
        fait = 0
        for res in list(self.ressources.values()):
            if self.arret():
                break
            self._lire_manifeste(res)
            fait += 1
            self.progression("analyse", fait, total, res.manifeste.relative_to(self.racine).as_posix())
        for chemin in fichiers:
            if self.arret():
                break
            self._analyser_fichier(chemin)
            fait += 1
            if fait % 7 == 0 or fait == total:
                self.progression("analyse", fait, total,
                                 chemin.relative_to(self.racine).as_posix())
        self._verifier_cfg()
        return self._rapport(time.time() - debut)

    def _rapport(self, duree):
        ordre = {n: i for i, n in enumerate(NIVEAUX)}
        self.problemes.sort(key=lambda p: (ordre[p["niveau"]], p["ressource"].lower(),
                                           p["fichier"], p["ligne"] or 0))
        groupes_vus = set()
        for i, p in enumerate(self.problemes, 1):
            p["id"] = i
            groupe = p.pop("groupe")
            p["autres"] = 0
            if id(groupe) not in groupes_vus:
                groupes_vus.add(id(groupe))
                p["autres"] = groupe["autres"]
        compte = {n: 0 for n in NIVEAUX}
        syntaxe = 0
        par_res = {}
        for p in self.problemes:
            if p["categorie"] == "syntaxe":
                syntaxe += 1
            else:
                compte[p["niveau"]] += 1
            r = par_res.setdefault(p["ressource"], {"compte": {n: 0 for n in NIVEAUX},
                                                    "syntaxe": 0})
            if p["categorie"] == "syntaxe":
                r["syntaxe"] += 1
            else:
                r["compte"][p["niveau"]] += 1
        ressources = []
        for res in self.ressources.values():
            info = par_res.get(res.nom, {"compte": {n: 0 for n in NIVEAUX}, "syntaxe": 0})
            ressources.append({
                "nom": res.nom,
                "chemin": res.dossier.relative_to(self.racine).as_posix(),
                "fichiers": res.fichiers,
                "escrow": res.escrow,
                "lua54": res.lua54,
                "compte": info["compte"],
                "syntaxe": info["syntaxe"],
                "score": _calculer_score(info["compte"], info["syntaxe"]),
            })
        ressources.sort(key=lambda r: (r["score"], r["nom"].lower()))
        return {
            "outil": "Nemesys Scanner",
            "version": VERSION,
            "racine": str(self.racine),
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "duree": round(duree, 2),
            "stats": self.stats,
            "compte": compte,
            "syntaxe": syntaxe,
            "score": _calculer_score(compte, syntaxe),
            "problemes": self.problemes,
            "ressources": ressources,
            "interrompu": bool(self.arret()),
        }


def _premiere_majuscule(texte):
    return texte[:1].upper() + texte[1:] if texte else texte


def _ressemble_texte(octets):
    echantillon = octets[:2048]
    if not echantillon:
        return True
    binaires = sum(1 for b in echantillon if b < 9 or 13 < b < 32)
    return binaires / len(echantillon) < 0.05


_JSON_FR = {
    "Expecting ',' delimiter": "virgule « , » attendue",
    "Expecting ':' delimiter": "deux-points « : » attendus",
    "Expecting value": "valeur attendue (virgule en trop ou valeur manquante ?)",
    "Expecting property name enclosed in double quotes":
        "nom entre guillemets attendu (virgule en trop avant « } » ?)",
    "Unterminated string starting at": "texte non fermé (guillemet manquant)",
    "Extra data": "contenu en trop après la fin du JSON",
    "Illegal trailing comma before end of object": "virgule en trop avant « } »",
    "Illegal trailing comma before end of array": "virgule en trop avant « ] »",
    "Invalid control character at": "caractère interdit dans un texte",
    "Invalid \\escape": "échappement « \\ » invalide",
}


def _traduire_json(e):
    msg = _JSON_FR.get(e.msg, e.msg)
    return f"{msg} (ligne {e.lineno}, colonne {e.colno})"


def analyser(racine, **options):
    return Analyse(racine, **options).lancer()
