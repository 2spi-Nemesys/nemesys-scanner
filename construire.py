import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ICI = Path(__file__).parent
ICONE = ICI / "icone.ico"


def dessiner_icone():
    taille = 256
    img = Image.new("RGBA", (taille, taille), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, taille - 8, taille - 8), radius=52, fill=(18, 13, 31, 255),
                        outline=(70, 58, 115, 255), width=6)
    m = [(62, 194), (62, 62), (128, 138), (194, 62), (194, 194)]
    d.line(m, fill=(196, 166, 255, 255), width=24, joint="curve")
    for x, y in (m[0], m[-1]):
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=(196, 166, 255, 255))
    img.save(ICONE, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


def construire(nom, fenetre):
    commande = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--onefile",
        "--name", nom, "--icon", str(ICONE),
        "--add-data", f"{ICI / 'ui'};ui",
        "--hidden-import", "lupa.lua54",
        "--collect-submodules", "lupa",
        "--distpath", str(ICI / "dist"), "--workpath", str(ICI / "build"),
        "--specpath", str(ICI / "build"),
    ]
    if fenetre:
        commande += ["--windowed", "--collect-all", "webview"]
    else:
        commande += ["--console", "--exclude-module", "webview", "--exclude-module", "PIL"]
    commande.append(str(ICI / "app.py"))
    subprocess.run(commande, check=True)


if __name__ == "__main__":
    dessiner_icone()
    construire("NemesysScanner", fenetre=True)
    construire("nemesys-scan", fenetre=False)
    shutil.rmtree(ICI / "build", ignore_errors=True)
    for exe in (ICI / "dist").glob("*.exe"):
        print(f"{exe.name} : {exe.stat().st_size / 1e6:.1f} Mo")
