import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path

from nemesys_scanner import VERSION, Analyse
from nemesys_scanner.regles import NIVEAUX


def langue_systeme():
    try:
        import ctypes
        code = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return "fr" if (code & 0x3FF) == 0x0C else "en"
    except Exception:
        import locale
        return "fr" if (locale.getlocale()[0] or "").lower().startswith(("fr", "french")) else "en"


def dossier_ressources():
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return base / "ui"


def rapport_html(rapport, langue="fr"):
    ui = dossier_ressources()
    page = (ui / "index.html").read_text("utf-8")
    css = (ui / "style.css").read_text("utf-8")
    js = (ui / "app.js").read_text("utf-8")
    donnees = json.dumps(rapport, ensure_ascii=False)
    donnees = donnees.replace("<", "\\u003c").replace(">", "\\u003e") \
        .replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    page = page.replace('<link rel="stylesheet" href="style.css">', f"<style>{css}</style>")
    page = page.replace('<div class="app" id="app" data-ecran="accueil">',
                        '<div class="app" id="app" data-ecran="resultats">')
    page = page.replace('<script src="app.js"></script>',
                        f"<script>window.RAPPORT_INTEGRE = {donnees}; window.LANGUE_RAPPORT = {json.dumps(langue)};</script>\n"
                        f"<script>{js}</script>")
    page = page.replace('<html lang="fr">', f'<html lang="{langue}">')
    page = page.replace("<title>Nemesys Scanner</title>",
                        "<title>Rapport Nemesys Scanner</title>" if langue == "fr"
                        else "<title>Nemesys Scanner report</title>")
    return page


class Pont:

    def __init__(self, dossier_initial=None):
        self._langue = langue_systeme()
        self._fenetre = None
        self._dossier_initial = dossier_initial
        self._rapport = None
        self._arret = threading.Event()
        self._en_cours = False

    def _js(self, code):
        if self._fenetre:
            try:
                self._fenetre.evaluate_js(code)
            except Exception:
                pass

    def dossier_initial(self):
        d, self._dossier_initial = self._dossier_initial, None
        return d

    def choisir_dossier(self):
        import webview
        choix = self._fenetre.create_file_dialog(webview.FileDialog.FOLDER)
        if not choix:
            return None
        return choix[0] if isinstance(choix, (list, tuple)) else choix

    def _m(self, fr, en):
        return en if self._langue == "en" else fr

    def lancer(self, dossier, langue=None):
        if langue in ("fr", "en"):
            self._langue = langue
        if self._en_cours:
            return self._m("Une analyse est déjà en cours.", "A scan is already running.")
        chemin = Path(dossier)
        if not chemin.is_dir():
            return self._m("Ce dossier n'existe pas ou n'est pas accessible.",
                           "This folder doesn't exist or can't be read.")
        self._arret.clear()
        self._en_cours = True
        threading.Thread(target=self._travail, args=(chemin,), daemon=True).start()
        return True

    def _travail(self, chemin):
        dernier = [0.0]
        import time

        def progression(phase, fait, total, info):
            maintenant = time.time()
            if phase == "analyse" and fait < total and maintenant - dernier[0] < 0.05:
                return
            dernier[0] = maintenant
            self._js(f"NS.progres({json.dumps({'phase': phase, 'fait': fait, 'total': total, 'info': info})})")

        try:
            self._rapport = Analyse(chemin, progression=progression,
                                    arret=self._arret.is_set).lancer()
            self._js("NS.fini()")
        except Exception as e:
            message = self._m(f"Analyse impossible : {e}", f"Scan failed: {e}")
            self._js(f"NS.erreur({json.dumps(message)})")
        finally:
            self._en_cours = False

    def arreter(self):
        self._arret.set()

    def resultat(self):
        return self._rapport

    def ouvrir(self, chemin, ligne=1):
        if not Path(chemin).is_file():
            return self._m("Ce fichier n'existe plus.", "This file no longer exists.")
        for editeur in ("code", "codium", "cursor"):
            exe = shutil.which(editeur)
            if exe:
                subprocess.Popen([exe, "-g", f"{chemin}:{int(ligne)}"], shell=False,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
                return True
        npp = shutil.which("notepad++") or next(
            (p for p in (r"C:\Program Files\Notepad++\notepad++.exe",
                         r"C:\Program Files (x86)\Notepad++\notepad++.exe") if Path(p).is_file()), None)
        if npp:
            subprocess.Popen([npp, f"-n{int(ligne)}", chemin])
            return True
        try:
            os.startfile(chemin)
            return True
        except OSError:
            subprocess.Popen(["notepad.exe", chemin])
            return True

    def exporter(self, langue=None):
        import webview
        if langue in ("fr", "en"):
            self._langue = langue
        if not self._rapport:
            return self._m("Aucun rapport à exporter.", "No report to export.")
        nom = self._m("rapport-nemesys-scanner.html", "nemesys-scanner-report.html")
        cible = self._fenetre.create_file_dialog(
            webview.FileDialog.SAVE, save_filename=nom,
            file_types=(self._m("Page web (*.html)", "Web page (*.html)"),
                        self._m("Données JSON (*.json)", "JSON data (*.json)")))
        if not cible:
            return None
        cible = Path(cible[0] if isinstance(cible, (list, tuple)) else cible)
        if cible.suffix.lower() == ".json":
            cible.write_text(json.dumps(self._rapport, ensure_ascii=False, indent=1), "utf-8")
        else:
            if cible.suffix.lower() != ".html":
                cible = cible.with_suffix(".html")
            cible.write_text(rapport_html(self._rapport, self._langue), "utf-8")
        return self._m(f"Rapport enregistré : {cible.name}", f"Report saved: {cible.name}")


def lancer_fenetre(dossier=None):
    import webview
    pont = Pont(dossier)
    fenetre = webview.create_window(
        "Nemesys Scanner", str(dossier_ressources() / "index.html"), js_api=pont,
        width=1360, height=860, min_size=(980, 640), background_color="#120d1f",
        text_select=True)
    pont._fenetre = fenetre

    def au_demarrage():
        from webview.dom import DOMEventHandler

        def depot(evenement):
            fichiers = (evenement.get("dataTransfer") or {}).get("files") or []
            for f in fichiers:
                chemin = f.get("pywebviewFullPath")
                if chemin:
                    dossier_cible = chemin if Path(chemin).is_dir() else str(Path(chemin).parent)
                    pont._js(f"NS.deposer({json.dumps(dossier_cible)})")
                    break
        try:
            fenetre.dom.document.events.drop += DOMEventHandler(depot, True, True)
        except Exception:
            pass

    webview.start(au_demarrage, private_mode=False,
                  storage_path=str(Path(os.environ.get("APPDATA", Path.home())) / "NemesysScanner"))


COULEURS = {"critique": "\033[38;2;255;77;109m", "eleve": "\033[38;2;255;159;67m",
            "moyen": "\033[38;2;242;209;75m", "info": "\033[38;2;106;169;255m",
            "lilas": "\033[38;2;196;166;255m", "doux": "\033[38;2;167;156;194m",
            "sain": "\033[38;2;61;220;151m", "gras": "\033[1m", "fin": "\033[0m"}
NOMS = {
    "fr": {"critique": "CRITIQUE", "eleve": "ÉLEVÉ", "moyen": "MOYEN", "info": "INFO"},
    "en": {"critique": "CRITICAL", "eleve": "HIGH", "moyen": "MEDIUM", "info": "INFO"},
}
ALIAS_NIVEAUX = {"critique": "critique", "critical": "critique", "eleve": "eleve", "élevé": "eleve",
                 "high": "eleve", "moyen": "moyen", "medium": "moyen", "info": "info"}
TERMINAL = {
    "fr": {
        "par": "par Nemesys Studio", "dossier": "Dossier :", "hors": "(hors ressource)",
        "decode": "décodé :", "autres": "+ {n} autre(s) fois dans ce fichier",
        "note": "Note de sécurité :", "niveaux": ("critique", "élevé", "moyen", "info"),
        "syntaxe": "{n} erreur(s) de syntaxe",
        "stats": "{f} fichiers, {l} lignes, {r} ressources en {d} s",
        "json": "Rapport JSON :", "html": "Rapport HTML :",
        "description": "Analyse un serveur FiveM : backdoors, code caché, erreurs de syntaxe.",
        "a_dossier": "dossier du serveur (avec server.cfg) ou dossier resources",
        "a_json": "enregistrer le rapport en JSON", "a_html": "enregistrer le rapport en page HTML",
        "a_min": "niveau minimum affiché : critique, eleve, moyen ou info (par défaut : moyen)",
        "a_node": "analyser aussi les dossiers node_modules",
        "a_lang": "langue des messages : fr ou en (par défaut : celle de Windows)",
        "introuvable": "dossier introuvable : {d}", "fichier": "FICHIER",
        "niveau_ko": "niveau inconnu : {n}",
    },
    "en": {
        "par": "by Nemesys Studio", "dossier": "Folder:", "hors": "(outside resources)",
        "decode": "decoded:", "autres": "+ {n} more time(s) in this file",
        "note": "Security score:", "niveaux": ("critical", "high", "medium", "info"),
        "syntaxe": "{n} syntax error(s)",
        "stats": "{f} files, {l} lines, {r} resources in {d} s",
        "json": "JSON report:", "html": "HTML report:",
        "description": "Scan a FiveM server: backdoors, hidden code, syntax errors.",
        "a_dossier": "server folder (with server.cfg) or resources folder",
        "a_json": "save the report as JSON", "a_html": "save the report as an HTML page",
        "a_min": "lowest level shown: critical, high, medium or info (default: medium)",
        "a_node": "also scan node_modules folders",
        "a_lang": "message language: fr or en (default: Windows language)",
        "introuvable": "folder not found: {d}", "fichier": "FILE",
        "niveau_ko": "unknown level: {n}",
    },
}


def activer_couleurs():
    if os.name == "nt":
        try:
            import ctypes
            k = ctypes.windll.kernel32
            h = k.GetStdHandle(-11)
            mode = ctypes.c_uint32()
            k.GetConsoleMode(h, ctypes.byref(mode))
            k.SetConsoleMode(h, mode.value | 0x0004)
        except Exception:
            pass
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def mode_terminal(args):
    couleur = activer_couleurs()
    c = (lambda k: COULEURS[k]) if couleur else (lambda k: "")
    largeur = shutil.get_terminal_size((100, 30)).columns
    lg = args.lang
    m = TERMINAL[lg]
    texte_de = (lambda p, champ: p["en"][champ]) if lg == "en" else (lambda p, champ: p[champ])

    print(f"\n {c('lilas')}{c('gras')}NEMESYS SCANNER{c('fin')} {c('doux')}{VERSION} · {m['par']}{c('fin')}")
    print(f" {c('doux')}{m['dossier']} {Path(args.dossier).resolve()}{c('fin')}\n")

    def progression(phase, fait, total, info):
        if phase != "analyse" or not sys.stdout.isatty():
            return
        barre = 30
        plein = int(barre * fait / max(1, total))
        texte = f" [{'█' * plein}{'·' * (barre - plein)}] {fait}/{total} "
        reste = max(0, largeur - len(texte) - 2)
        info = info[-reste:] if len(info) > reste else info
        print(f"\r{texte}{c('doux')}{info.ljust(reste)}{c('fin')}", end="", flush=True)

    rapport = Analyse(args.dossier, progression=progression,
                      inclure_node_modules=args.node_modules).lancer()
    if sys.stdout.isatty():
        print("\r" + " " * (largeur - 1) + "\r", end="")

    minimum = NIVEAUX.index(args.min)
    affiches = [p for p in rapport["problemes"] if NIVEAUX.index(p["niveau"]) <= minimum]
    affiches.sort(key=lambda p: (p["ressource"] == "(hors ressource)", p["ressource"].lower(),
                                 NIVEAUX.index(p["niveau"]), p["fichier"], p["ligne"] or 0))
    ressource = None
    for p in affiches:
        if p["ressource"] != ressource:
            ressource = p["ressource"]
            nom = m["hors"] if ressource == "(hors ressource)" else ressource
            print(f"\n {c('gras')}{nom}{c('fin')}")
        lieu = f"{p['fichier']}:{p['ligne']}" if p["ligne"] else p["fichier"]
        print(f"   {c(p['niveau'])}{NOMS[lg][p['niveau']]:<8}{c('fin')} {texte_de(p, 'titre')}")
        print(f"            {c('doux')}{lieu}{c('fin')}")
        if p["categorie"] == "syntaxe":
            print(f"            {texte_de(p, 'explication')}")
        if p.get("decode"):
            print(f"            {c('critique')}{m['decode']} {p['decode'][:160]}{c('fin')}")
        if p.get("autres"):
            print(f"            {c('doux')}{m['autres'].format(n=p['autres'])}{c('fin')}")

    cpt = rapport["compte"]
    s = rapport["score"]
    teinte = "sain" if s >= 85 else "moyen" if s >= 60 else "eleve" if s >= 36 else "critique"
    st = rapport["stats"]
    n_crit, n_eleve, n_moyen, n_info = m["niveaux"]
    print(f"\n {'─' * min(70, largeur - 2)}")
    print(f" {m['note']} {c(teinte)}{c('gras')}{s}/100{c('fin')}")
    print(f" {c('critique')}{cpt['critique']} {n_crit}{c('fin')}  {c('eleve')}{cpt['eleve']} {n_eleve}{c('fin')}  "
          f"{c('moyen')}{cpt['moyen']} {n_moyen}{c('fin')}  {c('info')}{cpt['info']} {n_info}{c('fin')}  "
          f"· {m['syntaxe'].format(n=rapport['syntaxe'])}")
    print(f" {c('doux')}{m['stats'].format(f=st['fichiers'], l=st['lignes'], r=st['ressources'], d=rapport['duree'])}"
          f"{c('fin')}\n")

    if args.json:
        Path(args.json).write_text(json.dumps(rapport, ensure_ascii=False, indent=1), "utf-8")
        print(f" {m['json']} {args.json}")
    if args.html:
        Path(args.html).write_text(rapport_html(rapport, lg), "utf-8")
        print(f" {m['html']} {args.html}")
    return 2 if cpt["critique"] else (1 if cpt["eleve"] or rapport["syntaxe"] else 0)


def main():
    terminal = Path(sys.argv[0]).stem.lower().startswith("nemesys-scan") or "--cli" in sys.argv
    if not terminal:
        dossier = next((a for a in sys.argv[1:] if not a.startswith("-")), None)
        lancer_fenetre(dossier)
        return 0
    lg = langue_systeme()
    for i, a in enumerate(sys.argv):
        if a == "--lang" and i + 1 < len(sys.argv) and sys.argv[i + 1] in ("fr", "en"):
            lg = sys.argv[i + 1]
        elif a.startswith("--lang=") and a[7:] in ("fr", "en"):
            lg = a[7:]
    m = TERMINAL[lg]
    parseur = argparse.ArgumentParser(prog="nemesys-scan", description=m["description"])
    parseur.add_argument("dossier", help=m["a_dossier"])
    parseur.add_argument("--json", metavar=m["fichier"], help=m["a_json"])
    parseur.add_argument("--html", metavar=m["fichier"], help=m["a_html"])
    parseur.add_argument("--min", default="moyen", help=m["a_min"])
    parseur.add_argument("--node-modules", action="store_true", help=m["a_node"])
    parseur.add_argument("--lang", choices=("fr", "en"), default=lg, help=m["a_lang"])
    parseur.add_argument("--cli", action="store_true", help=argparse.SUPPRESS)
    args = parseur.parse_args([a for a in sys.argv[1:] if a != "--cli"])
    niveau = ALIAS_NIVEAUX.get(args.min.lower())
    if not niveau:
        parseur.error(m["niveau_ko"].format(n=args.min))
    args.min = niveau
    if not Path(args.dossier).is_dir():
        parseur.error(m["introuvable"].format(d=args.dossier))
    return mode_terminal(args)


if __name__ == "__main__":
    sys.exit(main())
