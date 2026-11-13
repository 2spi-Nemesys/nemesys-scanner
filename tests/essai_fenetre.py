import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import webview

import app

dossier = sys.argv[1]
capture = sys.argv[2] if len(sys.argv) > 2 else None
pont = app.Pont(dossier)
fenetre = webview.create_window("Nemesys Scanner (test)", str(app.dossier_ressources() / "index.html"),
                                js_api=pont, width=1360, height=860)
pont._fenetre = fenetre
resultat = {}


def scenario():
    debut = time.time()
    while time.time() - debut < 180:
        time.sleep(1)
        ecran = fenetre.evaluate_js("document.getElementById('app').dataset.ecran")
        if ecran == "resultats":
            break
    time.sleep(1.5)
    resultat["ecran"] = fenetre.evaluate_js("document.getElementById('app').dataset.ecran")
    resultat["verdict"] = fenetre.evaluate_js("document.getElementById('verdict-titre').textContent")
    resultat["note"] = fenetre.evaluate_js("document.getElementById('note-valeur').textContent")
    resultat["cases"] = fenetre.evaluate_js("document.querySelectorAll('#radio-resultats .case').length")
    resultat["problemes_affiches"] = fenetre.evaluate_js("document.querySelectorAll('.probleme').length")
    fenetre.evaluate_js("document.querySelector('.probleme') && document.querySelector('.probleme').click()")
    time.sleep(0.5)
    resultat["detail"] = fenetre.evaluate_js("(document.querySelector('.detail h2')||{}).textContent")
    resultat["duree_totale"] = round(time.time() - debut, 1)
    if capture:
        try:
            from PIL import ImageGrab
            x, y = fenetre.x, fenetre.y
            ImageGrab.grab(bbox=(x, y, x + fenetre.width, y + fenetre.height)).save(capture)
            resultat["capture"] = capture
        except Exception as e:
            resultat["capture"] = f"impossible : {e}"
    fenetre.destroy()


webview.start(scenario)
print(json.dumps(resultat, ensure_ascii=False, indent=1))
