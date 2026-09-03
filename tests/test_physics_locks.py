#!/usr/bin/env python3
"""Physics locks for FIGURE v0. Tests, not a theorem. Not a QUANTUM seal."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import figure  # noqa: E402

FUTURE = "2028-08-31"
EXAMPLE = ROOT / "examples" / "fictive-adulte.figure.json"
COPY_FILES = (
    "README.md",
    "INTERDIT.md",
    "JUGE.md",
    "figure.py",
    "examples/fictive-adulte.figure.json",
    "NOTICE",
    "COPYRIGHT.md",
)


def _dump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False)


def _refus(fn, *args, **kwargs) -> str:
    with unittest.TestCase().assertRaises(SystemExit) as ctx:
        fn(*args, **kwargs)
    return str(ctx.exception)


def _cli(args, cwd=None):
    return subprocess.run(
        [sys.executable, str(ROOT / "figure.py"), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
    )


def _carte(**extra):
    base = dict(
        format="figure.v0",
        figure_id="FG-test",
        nom_public="Alex Moreau",
        majeur=True,
        juridiction="QC",
        langue="fr-CA",
        usages=["nom"],
        interdits=["mineur", "mandat sans fin", "fichier biométrique dans Git"],
        identite_sha256=None,
        debut="2026-08-31",
        fin=FUTURE,
        revocable=True,
        note="test",
    )
    base.update(extra)
    return base


class MissingFinIsRefused(unittest.TestCase):
    def test_ecrire_empty_fin_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["nom"], "")
        self.assertIn("fin", msg.lower())

    def test_ecrire_none_fin_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["nom"], None)
        self.assertIn("fin", msg.lower())

    def test_cli_missing_fin_is_refused(self):
        proc = _cli(["ecrire", "--nom-public", "Alex Moreau", "--usages", "nom"])
        self.assertNotEqual(proc.returncode, 0)
        combined = (proc.stderr + proc.stdout).lower()
        self.assertIn("fin", combined)

    def test_lire_missing_fin_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sans-fin.figure.json"
            carte = _carte()
            del carte["fin"]
            p.write_text(_dump(carte), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("fin", msg.lower())


class PastOrTodayFinIsRefused(unittest.TestCase):
    def test_past_fin_at_write_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["nom"], "2020-01-01")
        self.assertIn("aujourd", msg.lower())

    def test_today_utc_fin_at_write_is_refused(self):
        today = datetime.now(timezone.utc).date().isoformat()
        msg = _refus(figure.ecrire, "Alex Moreau", ["voix"], today)
        self.assertIn("aujourd", msg.lower())

    def test_cli_past_fin_is_refused(self):
        proc = _cli(
            [
                "ecrire",
                "--nom-public",
                "Alex Moreau",
                "--usages",
                "nom",
                "--fin",
                "2020-01-01",
            ]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("aujourd", (proc.stderr + proc.stdout).lower())

    def test_lire_expired_fin_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "expiree.figure.json"
            p.write_text(_dump(_carte(fin="2020-01-01")), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("expir", msg.lower())


class MajeurFalseIsRefused(unittest.TestCase):
    def test_ecrire_majeur_false_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["nom"], FUTURE, majeur=False)
        self.assertIn("mineur", msg.lower())

    def test_lire_majeur_false_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mineur.figure.json"
            p.write_text(_dump(_carte(majeur=False)), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("majeur", msg.lower())

    def test_lire_majeur_missing_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "sans-majeur.figure.json"
            carte = _carte()
            del carte["majeur"]
            p.write_text(_dump(carte), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("majeur", msg.lower())

    def test_ecrire_never_writes_majeur_false(self):
        carte = figure.ecrire("Alex Moreau", ["nom"], FUTURE)
        self.assertIs(carte["majeur"], True)


class UnknownUsageIsRefused(unittest.TestCase):
    def test_ecrire_unknown_usage_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["photon"], FUTURE)
        self.assertIn("usages", msg.lower())

    def test_ecrire_quantique_is_not_an_usage(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["quantique"], FUTURE)
        self.assertIn("usages", msg.lower())

    def test_cli_unknown_usage_is_refused(self):
        proc = _cli(
            [
                "ecrire",
                "--nom-public",
                "Alex Moreau",
                "--usages",
                "nom,cloud",
                "--fin",
                FUTURE,
            ]
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usages", (proc.stderr + proc.stdout).lower())

    def test_lire_unknown_usage_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "usage-inconnu.figure.json"
            p.write_text(_dump(_carte(usages=["nom", "token"])), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("usages", msg.lower())


class EmptyNameIsRefused(unittest.TestCase):
    def test_ecrire_empty_name_is_refused(self):
        msg = _refus(figure.ecrire, "", ["nom"], FUTURE)
        self.assertIn("nom-public", msg.lower())

    def test_ecrire_whitespace_name_is_refused(self):
        msg = _refus(figure.ecrire, "   ", ["visage"], FUTURE)
        self.assertIn("nom-public", msg.lower())

    def test_cli_empty_name_is_refused(self):
        proc = _cli(["ecrire", "--nom-public", "", "--usages", "nom", "--fin", FUTURE])
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("nom-public", (proc.stderr + proc.stdout).lower())


class MandatWithoutFinIsRefused(unittest.TestCase):
    def test_ecrire_mandat_without_fin_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["mandat"], "")
        self.assertIn("mandat", msg.lower())
        self.assertIn("fin", msg.lower())

    def test_ecrire_mandat_none_fin_is_refused(self):
        msg = _refus(figure.ecrire, "Alex Moreau", ["mandat"], None)
        self.assertIn("mandat", msg.lower())

    def test_lire_mandat_without_fin_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "mandat-sans-fin.figure.json"
            carte = _carte(usages=["mandat"])
            del carte["fin"]
            p.write_text(_dump(carte), encoding="utf-8")
            msg = _refus(figure.lire, str(p))
            self.assertIn("mandat", msg.lower())
            self.assertIn("fin", msg.lower())


class DefaultEcrireIsAdultAndFuture(unittest.TestCase):
    def test_ecrire_adult_future_fin_writes(self):
        carte = figure.ecrire("Alex Moreau", ["nom", "voix"], FUTURE)
        self.assertEqual(carte["format"], "figure.v0")
        self.assertEqual(carte["nom_public"], "Alex Moreau")
        self.assertIs(carte["majeur"], True)
        self.assertEqual(carte["usages"], ["nom", "voix"])
        self.assertEqual(carte["fin"], FUTURE)
        self.assertIsNone(carte["identite_sha256"])
        self.assertTrue(carte["figure_id"].startswith("FG-"))

    def test_four_usages_write_when_fin_is_ahead(self):
        for usage in figure.USAGES:
            with self.subTest(usage=usage):
                carte = figure.ecrire("Alex Moreau", [usage], FUTURE)
                self.assertEqual(carte["usages"], [usage])
                self.assertIs(carte["majeur"], True)
                self.assertEqual(carte["fin"], FUTURE)

    def test_cli_default_ecrire_is_adult_and_writes(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.figure.json"
            proc = _cli(
                [
                    "ecrire",
                    "--nom-public",
                    "Alex Moreau",
                    "--usages",
                    "nom,voix",
                    "--fin",
                    FUTURE,
                    "--vers",
                    str(dest),
                ],
                cwd=tmp,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            out = json.loads(proc.stdout)
            self.assertIs(out["majeur"], True)
            self.assertEqual(out["fin"], FUTURE)
            self.assertIsNone(out["identite_sha256"])
            written = json.loads(dest.read_text(encoding="utf-8"))
            self.assertIs(written["majeur"], True)
            self.assertEqual(written["fin"], FUTURE)
            self.assertIsNone(written["identite_sha256"])

    def test_calendar_day_is_utc(self):
        self.assertEqual(figure._aujourd_hui(), datetime.now(timezone.utc).date())


class ExampleStaysAdultFictive(unittest.TestCase):
    def test_example_is_adult_fictive(self):
        carte = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(carte["format"], "figure.v0")
        self.assertEqual(carte["nom_public"], "Alex Moreau")
        self.assertIs(carte["majeur"], True)
        self.assertIn("fict", carte["note"].lower())
        self.assertIsNone(carte["identite_sha256"])
        self.assertEqual(carte["usages"], ["nom", "voix"])
        self.assertTrue(carte["fin"])

    def test_example_lire_and_juger_allow(self):
        carte = figure.lire(str(EXAMPLE))
        self.assertIs(carte["majeur"], True)
        jugement = figure.juger(carte)
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "figure")
        self.assertEqual(jugement["nom_public"], "Alex Moreau")

    def test_no_biometric_file_in_examples(self):
        examples = list((ROOT / "examples").iterdir())
        self.assertTrue(examples)
        for path in examples:
            self.assertNotIn(path.suffix.lower(), {".wav", ".mp3", ".png", ".jpg", ".jpeg", ".webp", ".voix"})
            if path.suffix == ".json":
                carte = json.loads(path.read_text(encoding="utf-8"))
                self.assertIsNone(carte.get("identite_sha256"), msg=path.name)
                self.assertIs(carte.get("majeur"), True, msg=path.name)


class JugerNamesWhoNotQuantique(unittest.TestCase):
    def test_juger_active_names_who_not_quantique(self):
        jugement = figure.juger(figure.ecrire("Alex Moreau", ["nom"], FUTURE))
        self.assertEqual(jugement["decision"], "allow")
        self.assertEqual(jugement["flag"], "figure")
        self.assertEqual(jugement["nom_public"], "Alex Moreau")
        self.assertIn("qui", jugement["note"].lower())
        self.assertNotIn("quantique", jugement["note"].lower())
        self.assertNotIn("quantum", jugement["note"].lower())

    def test_cli_juger_example_names_who(self):
        proc = _cli(["juger", str(EXAMPLE)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertEqual(out["flag"], "figure")
        self.assertEqual(out["nom_public"], "Alex Moreau")
        self.assertNotIn("quantique", out["note"].lower())
        self.assertNotIn("Imagine", proc.stdout)

    def test_juger_does_not_collapse_mode(self):
        jugement = figure.juger(figure.ecrire("Alex Moreau", ["mandat"], FUTURE))
        self.assertNotIn("mode", jugement)
        self.assertNotIn("quantique", jugement)
        self.assertEqual(jugement["flag"], "figure")

    def test_juger_mineur_is_refused(self):
        msg = _refus(figure.juger, _carte(majeur=False))
        self.assertIn("majeur", msg.lower())


class NoQuantumSealInJson(unittest.TestCase):
    def test_ecrire_json_is_not_a_quantum_seal(self):
        dumped = _dump(figure.ecrire("Alex Moreau", ["nom"], FUTURE))
        self.assertNotIn("QUANTUM", dumped)
        self.assertNotIn("quantum seal", dumped.lower())
        self.assertNotIn("Quantum Mode ON", dumped)
        self.assertNotIn("quantique", dumped)

    def test_cli_ecrire_json_is_not_a_quantum_seal(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "carte.figure.json"
            proc = _cli(
                [
                    "ecrire",
                    "--nom-public",
                    "Alex Moreau",
                    "--usages",
                    "nom",
                    "--fin",
                    FUTURE,
                    "--vers",
                    str(dest),
                ],
                cwd=tmp,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertNotIn("QUANTUM", proc.stdout)
            written = dest.read_text(encoding="utf-8")
            self.assertNotIn("QUANTUM", written)
            self.assertNotIn("quantique", written)
            self.assertNotIn("Imagine", written)

    def test_cli_lire_json_is_not_a_quantum_seal(self):
        proc = _cli(["lire", str(EXAMPLE)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)

    def test_cli_juger_json_is_not_a_quantum_seal(self):
        proc = _cli(["juger", str(EXAMPLE)])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "allow")
        self.assertNotIn("QUANTUM", proc.stdout)
        self.assertNotIn("Imagine", proc.stdout)

    def test_example_json_is_not_a_quantum_seal(self):
        text = EXAMPLE.read_text(encoding="utf-8")
        self.assertNotIn("QUANTUM", text)
        self.assertNotIn("Imagine", text)
        self.assertNotIn("quantique", text)

    def test_card_does_not_mint_quantique(self):
        carte = figure.ecrire("Alex Moreau", ["nom"], FUTURE)
        self.assertNotIn("quantique", carte)
        self.assertNotIn("mode", carte)
        self.assertNotIn("quantique", carte["usages"])


class ReadmeDoorCopy(unittest.TestCase):
    def test_readme_has_no_imagine_word(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("Imagine", text)
        self.assertNotIn("imagine", text)

    def test_readme_does_not_claim_formal_verification(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("formally verified", text)
        self.assertNotIn("formally-verified", text)
        self.assertNotIn("formellement vérifié", text)

    def test_readme_names_four_usages_and_the_locks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("`nom`", text)
        self.assertIn("`voix`", text)
        self.assertIn("`visage`", text)
        self.assertIn("`mandat`", text)
        self.assertIn("python3 figure.py ecrire", text)
        self.assertIn("python3 figure.py lire", text)
        self.assertIn("python3 figure.py juger", text)
        self.assertIn("Verified vs assumed", text)
        self.assertIn("**verified**", text)
        self.assertIn("**later**", text)
        self.assertIn("How to run", text)

    def test_readme_names_utc_calendar_day(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("UTC", text)
        self.assertIn("calendar day", text)

    def test_readme_names_minor_and_biometric_locks(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("majeur", text)
        self.assertIn("identite_sha256", text)
        self.assertIn("null", text)
        self.assertIn("biometric", text.lower())

    def test_readme_does_not_mint_quantique_or_collapse_mode(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("does not mint `quantique`", text)
        self.assertIn("does not collapse MODE", text)

    def test_copy_on_this_rail_has_no_imagine_word(self):
        for rel in COPY_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("Imagine", text, msg=rel)

    def test_rail_copy_does_not_claim_formal_verification(self):
        for rel in COPY_FILES:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotIn("formally verified", text, msg=rel)
            self.assertNotIn("formally-verified", text, msg=rel)

    def test_interdit_stays(self):
        text = (ROOT / "INTERDIT.md").read_text(encoding="utf-8")
        self.assertIn("mineur", text)
        self.assertIn("mandat", text)
        self.assertIn("Hash seulement", text)
        self.assertIn("nom est public", text)

    def test_juge_does_not_collapse_mode(self):
        text = (ROOT / "JUGE.md").read_text(encoding="utf-8")
        self.assertIn("personne", text)
        self.assertIn("MODE", text)

    def test_cli_surface_stays_ecrire_lire_juger(self):
        proc = _cli(["-h"])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        self.assertIn("ecrire", proc.stdout)
        self.assertIn("lire", proc.stdout)
        self.assertIn("juger", proc.stdout)


if __name__ == "__main__":
    unittest.main()
