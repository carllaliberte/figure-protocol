#!/usr/bin/env python3
"""FIGURE v0 — écrire / lire une carte. Pas de mineur. Pas de fichier biométrique."""

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


def ecrire(
    nom_public: str,
    usages: list[str],
    fin: str,
    debut: str | None = None,
    juridiction: str = "QC",
    langue: str = "fr-CA",
    majeur: bool = True,
) -> dict:
    if not majeur:
        raise SystemExit("refus : figure d'un mineur")
    if not nom_public.strip():
        raise SystemExit("nom-public requis")
    mauvais = [u for u in usages if u not in USAGES]
    if mauvais:
        raise SystemExit("usages : nom | voix | visage | mandat")
    if not usages:
        raise SystemExit("au moins un usage")
    try:
        jour_fin = _parse_jour(fin)
    except ValueError:
        raise SystemExit("fin : YYYY-MM-DD") from None
    if jour_fin <= _aujourd_hui():
        raise SystemExit("fin doit être après aujourd'hui")
    jour_debut = _parse_jour(debut) if debut else _aujourd_hui()
    carte = {
        "format": FORMAT,
        "figure_id": "FG-" + uuid.uuid4().hex[:12],
        "nom_public": nom_public.strip(),
        "majeur": True,
        "juridiction": juridiction,
        "langue": langue,
        "usages": usages,
        "interdits": ["mineur", "mandat sans fin", "fichier biométrique dans Git"],
        "identite_sha256": None,
        "debut": jour_debut.isoformat(),
        "fin": jour_fin.isoformat(),
        "revocable": True,
        "note": "v0 non signée. QUANTUM signe plus tard. Hash seulement dans Git.",
    }
    return carte


def lire(chemin: str) -> dict:
    p = Path(chemin).expanduser()
    carte = json.loads(p.read_text(encoding="utf-8"))
    if carte.get("format") != FORMAT:
        raise SystemExit("pas une carte figure.v0")
    if carte.get("majeur") is not True:
        raise SystemExit("carte refusée : majeur ≠ true")
    if not carte.get("fin"):
        raise SystemExit("carte refusée : pas de fin")
    if not carte.get("usages"):
        raise SystemExit("carte refusée : pas d'usage")
    try:
        if _parse_jour(carte["fin"]) <= _aujourd_hui():
            raise SystemExit("carte expirée")
    except ValueError as e:
        if "expirée" in str(e):
            raise
        raise SystemExit("fin illisible") from None
    return carte


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="figure")
    sub = p.add_subparsers(dest="cmd", required=True)
    pe = sub.add_parser("ecrire")
    pe.add_argument("--nom-public", required=True)
    pe.add_argument("--usages", required=True, help="nom,voix,visage,mandat")
    pe.add_argument("--fin", required=True, help="YYYY-MM-DD")
    pe.add_argument("--debut", default=None)
    pe.add_argument("--juridiction", default="QC")
    pe.add_argument("--langue", default="fr-CA")
    pe.add_argument("--vers", default="carte.figure.json")
    pl = sub.add_parser("lire")
    pl.add_argument("fichier")
    args = p.parse_args(argv)
    if args.cmd == "ecrire":
        usages = [u.strip() for u in args.usages.split(",") if u.strip()]
        carte = ecrire(
            args.nom_public,
            usages,
            args.fin,
            debut=args.debut,
            juridiction=args.juridiction,
            langue=args.langue,
        )
        Path(args.vers).write_text(
            json.dumps(carte, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        out = dict(carte)
        out["fichier"] = args.vers
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(lire(args.fichier), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
