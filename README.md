# TP3 EF : couplage Navier-Stokes / Température

## Prérequis

- FreeFem++ (≥ 4.13, avec `FreeFem++-nw`)
- python3 avec numpy et matplotlib

## Exécution

Toutes les commandes se lancent depuis la racine du dépôt. `make` sans argument affiche l'aide.

| Commande | Options (valeurs par défaut) | Sorties |
|---|---|---|
| `make q1` | `K=2` (2 ou 3), `N=16` | `results/q1/freefem_P<K>.txt`, `newton_P<K>.txt`, `errors_P<K>.txt` |
| `make q2` | `NMIN=4`, `NMAX=128` | `results/q2/freefem_P<k>.txt`, `conv_P<k>.txt` (k = 2, 3) |
| `make q2-k2`, `make q2-k3` | `NMIN`, `NMAX` | un seul des deux fichiers ci-dessus |
| `make q3` | `NMIN=8`, `NMAX=64` | `results/q3/freefem_P2.txt`, `visc_P2.txt` |
| `make q4` | `NU=0.1`, `N=64` | `results/q4/freefem_nu<NU>.txt`, `cavity_nu<NU>.txt` |
| `make figures` | | `figures/*.png` (à partir des fichiers de `results/`) |
| `make all` | | q1, q2, q3, q4 puis figures |
| `make clean` | | supprime `results/` et `figures/` |

Les maillages vont de `NMIN` à `NMAX` en doublant n (h = 1/n).
Les fichiers `freefem_*.txt` contiennent la sortie console de FreeFem++ ; les autres `.txt` sont les données utilisées par `make figures`.

Exemples :

```sh
make q1 K=3 N=32
make q2-k3 NMAX=64
make q4 NU=0.01 N=128
make figures
```

On peut aussi lancer un script directement, par exemple :

```sh
FreeFem++-nw -v 0 src/q2_convergence.edp -k 3 -nmin 4 -nmax 64
```
