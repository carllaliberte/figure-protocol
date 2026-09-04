#!/usr/bin/env python3
"""International lock: expired FIGURE silences the agent. Pack = BCP 47. No new slug."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import figure  # noqa: E402

EXAMPLE = ROOT / "examples" / "expiree-silence.figure.json"
WALK = ROOT / "examples" / "world-silence.md"


class ExpiredFigureSilencesAgent(unittest.TestCase):
    def test_example_is_adult_expired_fictive(self):
        carte = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        self.assertEqual(carte["format"], "figure.v0")
        self.assertIs(carte["majeur"], True)
        self.assertIsNone(carte["identite_sha256"])
        self.assertEqual(carte["langue"], "fr-CA")
        self.assertEqual(carte["fin"], "2026-01-01")

    def test_juger_expired_silence_keeps_pack(self):
        jugement = figure.juger(json.loads(EXAMPLE.read_text(encoding="utf-8")))
        self.assertEqual(jugement["decision"], "deny")
        self.assertIs(jugement["silence"], True)
        self.assertEqual(jugement["pack"], "fr-CA")
        self.assertEqual(jugement["spoken"], figure.SILENCE_EN)
        self.assertNotIn("quantique", json.dumps(jugement))

    def test_unknown_langue_falls_back_to_fr_ca(self):
        carte = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        carte["langue"] = "xx-ZZ"
        self.assertEqual(figure.juger(carte)["pack"], "fr-CA")

    def test_es_mx_pack_is_kept(self):
        carte = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        carte["langue"] = "es-MX"
        self.assertEqual(figure.juger(carte)["pack"], "es-MX")
        self.assertEqual(figure.juger(carte)["spoken"], figure.SILENCE_EN)

    def test_cli_juger_example_silence(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "figure.py"), "juger", str(EXAMPLE)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        out = json.loads(proc.stdout)
        self.assertEqual(out["decision"], "deny")
        self.assertIs(out["silence"], True)
        self.assertEqual(out["spoken"], figure.SILENCE_EN)
        self.assertNotIn("QUANTUM", proc.stdout)

    def test_walk_names_host_and_forbids_second_slug(self):
        text = WALK.read_text(encoding="utf-8")
        self.assertIn("acorn-royal-dune-blend.grok.me", text)
        self.assertIn("licence expired. the agent stays silent.", text)
        self.assertIn("Preview is not a receipt", text)
        self.assertIn("Unforge does not sign", text)
        self.assertNotIn("Imagine", text)
