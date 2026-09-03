#!/usr/bin/env python3
"""FIGURE v0 — écrire / lire / juger une carte. Pas de mineur. Pas de fichier biométrique."""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import date, datetime, timezone
from pathlib import Path

USAGES = ("nom", "voix", "visage", "mandat")
FORMAT = "figure.v0"


def _aujourd_hui() -> date:
    return datetime.now(timezone.utc).date()


def _parse_jour(s: str) -> date:
    return date.fromisoformat(s)


def _exiger_fin(fin, usages=()) -> date:
    if fin is None or not str(fin).strip():
        if "mandat" in (usages or ()):
            raise SystemExit("refus : mandat sans fin")
        raise SystemExit("refus : fin manquante")
    try:
        return _parse_jour(str(fin).strip())
    except ValueError:
        raise SystemExit("fin : YYYY-MM-DD") from None


def ecrire(nom_public, usages, fin, debut=None, juridiction="QC", langue="fr-CA", majeur=True, temoin_id=None, transcript_sha256=None):
    if not majeur:
        raise SystemExit("refus : figure d'un mineur")
    if not nom_public or not nom_public.strip():
        raise SystemExit("nom-public requis")
    mauvais = [u for u in usages if u not in USAGES]
    if mauvais:
        raise SystemExit("usages : nom | voix | visage | mandat")
    if not usages:
        raise SystemExit("au moins un usage")
    jour_fin = _exiger_fin(fin, usages)
    if jour_fin <= _aujourd_hui():
        raise SystemExit("fin doit être après aujourd'hui")
    jour_debut = _parse_jour(debut) if debut else _aujourd_hui()
    return {
        "format": FORMAT,
        "figure_id": "FG-" + uuid.uuid4().hex[:12],
        "nom_public": nom_public.strip(),
        "majeur": True,
        "juridiction": juridiction,
        "langue": langue,
        "usages": usages,
        "interdits": ["mineur", "mandat sans fin", "fichier biométrique dans Git"],
        "identite_sha256": None,
        "temoin_id": temoin_id or None,
        "transcript_sha256": transcript_sha256 or None,
        "debut": jour_debut.isoformat(),
        "fin": jour_fin.isoformat(),
        "revocable": True,
        "note": "v0 non signée. Hash seulement dans Git.",
    }


def _garde(carte: dict) -> date:
    if carte.get("format") != FORMAT:
        raise SystemExit("pas une carte figure.v0")
    if carte.get("majeur") is not True:
        raise SystemExit("carte refusée : majeur ≠ true")
    if not carte.get("usages"):
        raise SystemExit("carte refusée : pas d'usage")
    mauvais = [u for u in carte["usages"] if u not in USAGES]
    if mauvais:
        raise SystemExit("usages : nom | voix | visage | mandat")
    if not carte.get("fin"):
        if "mandat" in carte["usages"]:
            raise SystemExit("refus : mandat sans fin")
        raise SystemExit("carte refusée : pas de fin")
    try:
        return _parse_jour(carte["fin"])
    except (TypeError, ValueError):
        raise SystemExit("fin illisible") from None


def lire(chemin: str) -> dict:
    carte = json.loads(Path(chemin).expanduser().read_text(encoding="utf-8"))
    _garde(carte)
    return carte


def juger(carte: dict, aujourd: date | None = None) -> dict:
    jour_fin = _garde(carte)
    here = aujourd or _aujourd_hui()
    if jour_fin <= here:
        return {
            "decision": "deny",
            "flag": "figure",
            "nom_public": carte.get("nom_public"),
            "usages": carte.get("usages"),
            "fin": carte.get("fin"),
            "note": "servitude ended. Person is not fake. Speak of, not as.",
        }
    return {
        "decision": "allow",
        "flag": "figure",
        "nom_public": carte.get("nom_public"),
        "usages": carte.get("usages"),
        "fin": carte.get("fin"),
        "note": "figure active. parler comme X. cette rail nomme qui.",
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="figure")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("ecrire")
    pe.add_argument("--nom-public", required=True)
    pe.add_argument("--usages", required=True)
    pe.add_argument("--fin", required=True)
    pe.add_argument("--debut", default=None)
    pe.add_argument("--temoin-id", default=None)
    pe.add_argument("--transcript-sha256", default=None)
    pe.add_argument("--juridiction", default="QC")
    pe.add_argument("--langue", default="fr-CA")
    pe.add_argument("--vers", default="carte.figure.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    pj = sub.add_parser("juger")
    pj.add_argument("fichier")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        usages = [u.strip() for u in args.usages.split(",") if u.strip()]
        carte = ecrire(args.nom_public, usages, args.fin, args.debut, args.juridiction, args.langue, True, args.temoin_id, args.transcript_sha256)
        Path(args.vers).write_text(json.dumps(carte, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        out = dict(carte); out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif args.cmd == "lire":
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(juger(lire(args.fichier)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
