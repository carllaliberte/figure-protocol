# FIGURE Protocol

**Une servitude pour une personne.**

FIGURE est un registre de droits sur un nom, une voix, un visage ou un mandat : un agent n'emprunte X **que** s'il existe une figure active. This rail names who. It does not collapse MODE. This rail does not mint `quantique`.

This repository is version 0. Phone + Python. MIT. See [INTERDIT.md](INTERDIT.md).

Ce n'est pas SITUS (un lieu n'a pas de gorge).
Ce n'est pas UNFORGE (un fichier n'est pas une personne).
Ce n'est pas QUELLE (l'origine d'un bit n'est pas un visage).
Ce n'est pas TÉMOIN (la force d'un aléa n'est pas un nom).
Ce n'est pas BRUIT (un canal n'est pas un consentement).
Ce n'est pas HORIZON (une date de ressellage n'est pas une personne).
Ce n'est pas un sceau QUANTUM.
A public name is not consent. Do not invent consent because a name is public.

## Primitive

```
figure active  →  parler comme X
figure absente →  parler de X, jamais comme X
```

Quatre usages, séparés. This rail does not collapse them.

| Code | Droit |
|---|---|
| `nom` | Signer / se présenter sous ce nom |
| `voix` | Synthèse ou imitation vocale |
| `visage` | Image, deepfake, avatar |
| `mandat` | Agir en son nom auprès d'un tiers |

## Physics locks (this rail)

- FIGURE is a servitude on a person: name, voice, face, or mandate. Active figure → speak as X. Absent figure → speak of X, never as X.
- Four usages, kept separate: `nom` | `voix` | `visage` | `mandat`.
- Missing `fin` (`YYYY-MM-DD`): refuse. Past or today at write: refuse. The date is a UTC calendar day. The named day is already too late.
- Expire is a judge decision, not a parse error. `lire` of an expired card succeeds — it is still a figure.v0 card.
- `juger` deny when `fin` is today or past: servitude ended. Person is not fake. Speak of, not as.
- Minor: refuse. `majeur` must be true. `lire` refuses `majeur ≠ true`. Never write a minor figure.
- Usage `mandat` without an end date: refuse.
- Never put a biometric file (voice / face / ID) in Git — hash only. `identite_sha256` stays null in v0 examples.
- JSON card is not a QUANTUM seal. QUANTUM signs later. Keys off Git.
- `juger` names who. It does not collapse MODE. Do not mint `quantique`.
- Not SITUS, UNFORGE, QUELLE, TÉMOIN, BRUIT, or HORIZON. No token, L1, voice-cloud, face marketplace, or legal opinion.

Judgment = Carl: `python3 figure.py ecrire|lire|juger`.

## How to run

```bash
python3 figure.py ecrire --nom-public "Alex Moreau" --usages nom,voix --fin 2027-08-31
python3 figure.py lire examples/fictive-adulte.figure.json
python3 figure.py juger examples/fictive-adulte.figure.json
```

Sans date de fin : refus. Mineur : refus. Fichier biométrique dans Git : refus.
The calendar day is UTC. Named day already too late at write.
A judge `deny` does not say the person is fake. It says: servitude ended. Person is not fake. Speak of, not as.

Physics locks (stdlib, no extra packages):

```bash
python3 -m unittest discover -s tests -v
```

## Verified vs assumed

Tests lock the rows below. Nothing in this repository is a theorem. Nothing here is a QUANTUM seal. A merge is not a seal.

| Claim | Status |
|---|---|
| missing `fin` is refused | **verified** by tests on this rail |
| past or today `fin` at write is refused | **verified** |
| `lire` of an expired card succeeds | **verified** |
| `juger` expired / named UTC day is deny + not fake | **verified** |
| `majeur` false is refused | **verified** |
| `lire` refuses `majeur ≠ true` | **verified** |
| unknown usage is refused | **verified** |
| empty name is refused | **verified** |
| default `ecrire` is adult + future `fin` | **verified** |
| `mandat` without an end date is refused | **verified** |
| JSON card is not a QUANTUM seal | **verified** |
| example stays adult fictive; `identite_sha256` is null | **verified** |
| `juger` names who, not `quantique` | **verified** |
| QUANTUM signature | **later** — keys off Git, not in this repo |
| EasyCrypt / formal-layer | **not here** |
| mint `quantique` / collapse MODE | **refused** |
| minor figure / biometric file in Git | **refused** |
| consent because a name is public | **refused** |

## What v0 refuses

See [INTERDIT.md](INTERDIT.md). In short:

- figure d'un mineur
- `fin` manquante à l'écriture ; passée ou aujourd'hui (UTC) à l'écriture
- usage `mandat` sans date de fin
- usage inconnu, nom vide
- fichier voix / visage / pièce d'identité dans Git
- inventer le consentement parce que le nom est public
- un token, un L1, un cloud de voix, un marketplace de visages
- un avis juridique
- un sceau QUANTUM
- frapper `quantique` sur cette rail
- collapser MODE depuis FIGURE

Une `fin` expirée n'est pas une personne fausse. `juger` deny : servitude ended. Person is not fake. Speak of, not as.

Parler *de* quelqu'un reste libre. Parler *comme* quelqu'un exige une figure.

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [BRUIT](https://github.com/carllaliberte/bruit-protocol) | ce que le score a vu |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |
| [EPSILON](https://github.com/carllaliberte/epsilon-protocol) | avec quel ε |
| [MODE](https://github.com/carllaliberte/mode-protocol) | le collapse des quatre |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe **plus tard**. Les clés restent hors Git. Ce dépôt n'est pas un sceau QUANTUM.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`JUGE.md`](JUGE.md) — cette rail nomme qui, ne frappe pas `quantique`
- [`schema/figure.v0.json`](schema/figure.v0.json)
- [`figure.py`](figure.py) — `python3 figure.py ecrire` / `lire` / `juger`
- [`examples/fictive-adulte.figure.json`](examples/fictive-adulte.figure.json) — adulte fictif, hash null
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
