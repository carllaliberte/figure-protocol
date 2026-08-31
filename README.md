# FIGURE Protocol

**Une servitude pour une personne.**

FIGURE est un registre de droits sur un nom, une voix ou un visage : un agent n'emprunte X **que** s'il existe une figure active.

Ce dépôt est la version 0. Elle tient dans un téléphone. Zéro token. Zéro serveur payant.

**Open source (MIT).** Le protocole reste public. Voir [COPYRIGHT.md](COPYRIGHT.md) et [INTERDIT.md](INTERDIT.md).

## Primitive

```
figure active  →  parler comme X, cloner la voix, porter le nom
figure absente →  parler de X, jamais comme X
```

Quatre usages, séparés :

| Code | Droit |
|---|---|
| `nom` | Signer / se présenter sous ce nom |
| `voix` | Synthèse ou imitation vocale |
| `visage` | Image, deepfake, avatar |
| `mandat` | Agir en son nom auprès d'un tiers |

## v0 au cellulaire

```bash
python3 figure.py ecrire --nom-public "Alex Moreau" --usages nom,voix --fin 2027-08-31
python3 figure.py lire examples/fictive-adulte.figure.json
```

Sans date de fin : refus. Mineur : refus. Fichier biométrique dans Git : refus.

## Ce que v0 n'est pas

- pas SITUS (un lieu n'a pas de gorge)
- pas UNFORGE (un fichier n'est pas une personne)
- pas QUELLE (l'origine d'un bit n'est pas un visage)
- pas un token, pas un cloud de voix, pas un avis juridique

## Famille

| Rail | Question |
|---|---|
| [FIGURE](https://github.com/carllaliberte/figure-protocol) | qui |
| [SITUS](https://github.com/carllaliberte/situs-protocol) | où |
| [UNFORGE](https://github.com/carllaliberte/unforge-check) | quoi |
| [QUELLE](https://github.com/carllaliberte/quelle) | d'où le bit |
| [TÉMOIN](https://github.com/carllaliberte/temoin-protocol) | avec quelle force |
| [HORIZON](https://github.com/carllaliberte/horizon-protocol) | jusqu'à quand le sceau tient |

MIT (protocoles) · Apache-2.0 (œil UNFORGE). QUANTUM signe. Les clés restent hors Git.

## Fichiers

- [`INTERDIT.md`](INTERDIT.md) — ce qu'on ne prétend pas
- [`schema/figure.v0.json`](schema/figure.v0.json)
- [`figure.py`](figure.py) — écrire + lire
- [`examples/fictive-adulte.figure.json`](examples/fictive-adulte.figure.json)
