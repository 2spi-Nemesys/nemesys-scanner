import sys
import unittest
from pathlib import Path

ICI = Path(__file__).parent
sys.path.insert(0, str(ICI.parent))

from nemesys_scanner import analyser
from nemesys_scanner import lua

import generer_piege


class Syntaxe(unittest.TestCase):
    def test_extensions_cfx_acceptees(self):
        src = b"local a = 0\na += 1\nlocal h = `adder`\nlocal x = t?.champ\nlocal c <const> = 2 // 1\n"
        self.assertIsNone(lua.verifier_syntaxe(src))

    def test_commentaires_c_acceptes(self):
        src = b"return {\n  a = 1,\n  /*\n  * commentaire\n  */\n  b = 'data/*.lua',\n}\n"
        self.assertIsNone(lua.verifier_syntaxe(src))
        ligne, _, _ = lua.verifier_syntaxe(b"local p = 'x/*.lua'\nlocal = 2\n")
        self.assertEqual(ligne, 2)

    def test_erreur_traduite(self):
        ligne, message, _ = lua.verifier_syntaxe(b"if x then\n  print(1)\n")
        self.assertEqual(ligne, 3)
        self.assertIn("« end » manquant", message)

    def test_manifeste_bac_a_sable(self):
        paires, err = lua.lire_manifeste(b"os.execute('calc')")
        self.assertIsNone(paires)
        paires, err = lua.lire_manifeste(b"while true do end")
        self.assertIsNone(paires)


class ServeurPiege(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = analyser(ICI / "serveur-piege")
        cls.regles = {(p["regle"], p["niveau"]) for p in cls.r["problemes"]}

    def attendu(self, regle, niveau):
        self.assertIn((regle, niveau), self.regles)

    def test_backdoors(self):
        for regle in ("domaine-backdoor", "telecharge-execute", "code-cache-espaces",
                      "texte-echappe", "string-char", "vol-secret", "droits-admin",
                      "auto-propagation", "js-eval"):
            with self.subTest(regle=regle):
                self.attendu(regle, "critique")

    def test_texte_decode(self):
        p = next(p for p in self.r["problemes"] if p["regle"] == "texte-echappe")
        self.assertIn("PerformHttpRequest", p["decode"])

    def test_syntaxe_et_manifestes(self):
        self.attendu("syntaxe-lua", "eleve")
        self.attendu("syntaxe-json", "moyen")
        self.attendu("fichier-manquant", "eleve")
        self.attendu("ensure-absent", "moyen")

    def test_ressource_saine_sans_faux_positif(self):
        client = [p for p in self.r["problemes"] if p["fichier"].endswith("hud_propre/client.lua")]
        self.assertEqual(client, [])

    def test_note(self):
        self.assertLess(self.r["score"], 30)


if __name__ == "__main__":
    unittest.main()
