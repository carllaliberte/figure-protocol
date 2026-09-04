# FIGURE Protocol

**Une servitude pour une personne.**

FIGURE est un registre de droits sur un nom, une voix, un visage ou un mandat : un agent n'emprunte X **que** s'il existe une figure active. Ce rail nomme qui. Il ne collapse pas MODE. Ce rail ne frappe pas `quantique`.

Ce dépôt est la version 0. Téléphone + Python. MIT. Voir [INTERDIT.md](INTERDIT.md).

Ce n'est pas SITUS (un lieu n'a pas de gorge).
Ce n'est pas UNFORGE (un fichier n'est pas une personne).
Ce n'est pas QUELLE (l'origine d'un bit n'est pas un visage).
Ce n'est pas TÉMOIN (la force d'un aléa n'est pas un nom).
Ce n'est pas BRUIT (un canal n'est pas un consentement).
Ce n'est pas HORIZON (une date de ressellage n'est pas une personne).
Ce n'est pas un sceau QUANTUM.
Un nom public n'est pas un consentement. On n'invente pas le consentement parce que le nom est public.

## Primitive

```
figure active  →  parler comme X
figure absente →  parler de X, jamais comme X
```

Quatre usages, séparés. Ce rail ne les collapse pas.

| Code | Droit |
|---|---|
| `nom` | Signer / se présenter sous ce nom |
| `voix` | Synthèse ou imitation vocale |
| `visage` | Image, deepfake, avatar |
| `mandat` | Agir en son nom auprès d'un tiers |

## Verrous physiques (ce rail)

- FIGURE est une servitude sur une personne : nom, voix, visage ou mandat. Figure active → parler comme X. Figure absente → parler de X, jamais comme X.
- Quatre usages, tenus séparés : `nom` | `voix` | `visage` | `mandat`.
- `fin` manquante (`YYYY-MM-DD`) : refus. Passée ou aujourd'hui à l'écriture : refus. La date est un jour calendaire UTC. Le jour nommé est déjà trop tard.
- L'expiration est une décision du juge, pas une erreur de parse. `lire` d'une carte expirée réussit — c'est encore une carte figure.v0.
- `juger` deny quand `fin` est aujourd'hui ou passée : servitude terminée. La personne n'est pas fausse. Parler de, jamais comme.
- Mineur : refus. `majeur` doit être true. `lire` refuse `majeur ≠ true`. Jamais écrire une figure mineure.
- Usage `mandat` sans date de fin : refus.
- Jamais un fichier biométrique (voix / visage / pièce d'identité) dans Git — hash seulement. `identite_sha256` reste null dans les exemples v0.
- La carte JSON n'est pas un sceau QUANTUM. QUANTUM signe plus tard. Les clés restent hors Git.
- `juger` nomme qui. Il ne collapse pas MODE. On ne frappe pas `quantique`.
- Pas SITUS, UNFORGE, QUELLE, TÉMOIN, BRUIT, ni HORIZON. Pas de token, L1, cloud de voix, marketplace de visages, ni avis juridique.

Jugement = Carl : `python3 figure.py ecrire|lire|juger`.

## Comment lancer

```bash
python3 figure.py ecrire --nom-public "Alex Moreau" --usages nom,voix --fin 2027-08-31
python3 figure.py lire examples/fictive-adulte.figure.json
python3 figure.py juger examples/fictive-adulte.figure.json
```

Sans date de fin : refus. Mineur : refus. Fichier biométrique dans Git : refus.
Le jour calendaire est UTC. Le jour nommé est déjà trop tard à l'écriture.
Un `deny` du juge ne dit pas que la personne est fausse. Il dit : servitude terminée. La personne n'est pas fausse. Parler de, jamais comme.

Verrous physiques (stdlib, sans paquet extra) :

```bash
python3 -m unittest discover -s tests -v
```

## Vérifié vs présumé

Les tests verrouillent les lignes ci-dessous. Rien dans ce dépôt n'est un théorème. Rien ici n'est un sceau QUANTUM. Un merge n'est pas un sceau.

| Affirmation | Statut |
|---|---|
| `fin` manquante est refusée | **vérifié** par les tests de ce rail |
| `fin` passée ou aujourd'hui à l'écriture est refusée | **vérifié** |
| `lire` d'une carte expirée réussit | **vérifié** |
| `juger` expirée / jour UTC nommé est deny + pas fausse | **vérifié** |
| `majeur` false est refusé | **vérifié** |
| `lire` refuse `majeur ≠ true` | **vérifié** |
| usage inconnu est refusé | **vérifié** |
| nom vide est refusé | **vérifié** |
| `ecrire` par défaut est adulte + `fin` future | **vérifié** |
| `mandat` sans date de fin est refusé | **vérifié** |
| la carte JSON n'est pas un sceau QUANTUM | **vérifié** |
| l'exemple reste adulte fictif ; `identite_sha256` est null | **vérifié** |
| `juger` nomme qui, pas `quantique` | **vérifié** |
| signature QUANTUM | **plus tard** — clés hors Git, pas dans ce dépôt |
| EasyCrypt / formal-layer | **pas ici** |
| frapper `quantique` / collapser MODE | **refusé** |
| figure mineure / fichier biométrique dans Git | **refusé** |
| consentement parce que le nom est public | **refusé** |

## Ce que v0 refuse

Voir [INTERDIT.md](INTERDIT.md). En bref :

- figure d'un mineur
- `fin` manquante à l'écriture ; passée ou aujourd'hui (UTC) à l'écriture
- usage `mandat` sans date de fin
- usage inconnu, nom vide
- fichier voix / visage / pièce d'identité dans Git
- inventer le consentement parce que le nom est public
- un token, un L1, un cloud de voix, un marketplace de visages
- un avis juridique
- un sceau QUANTUM
- frapper `quantique` sur ce rail
- collapser MODE depuis FIGURE

Une `fin` expirée n'est pas une personne fausse. `juger` deny : servitude terminée. La personne n'est pas fausse. Parler de, jamais comme.

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
- [`JUGE.md`](JUGE.md) — ce rail nomme qui, ne frappe pas `quantique`
- [`schema/figure.v0.json`](schema/figure.v0.json)
- [`figure.py`](figure.py) — `python3 figure.py ecrire` / `lire` / `juger`
- [`examples/fictive-adulte.figure.json`](examples/fictive-adulte.figure.json) — adulte fictif, hash null
- [`tests/test_physics_locks.py`](tests/test_physics_locks.py) — verrous physiques
- [`.github/workflows/physics.yml`](.github/workflows/physics.yml) — CI des tests
