"""Analyses sur les champs agrégés : localité (test 5), fractions de Hodge, résumé par tranche.

    python3 src/analysis.py data/blitz
"""
import glob, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from flow import load_flows, W, PT_NAMES
from hodge import Hodge

WINDOWS = [(0, 10), (10, 30), (30, 60), (60, 300)]


def fd_divergence(D):
    """Divergence par différences finies (schéma « amont » : exact pour un pas d'une case orthogonal) du champ
    de vecteurs aux cases D[..., 64, 2] (somme des déplacements partant de chaque case)."""
    G = D.reshape(D.shape[:-2] + (8, 8, 2))            # [..., rang, colonne, (df, dr)]
    jx, jy = G[..., 0], G[..., 1]
    div = jx.copy() + jy
    div[..., :, 1:] -= jx[..., :, :-1]
    div[..., 1:, :] -= jy[..., :-1, :]
    return div.reshape(D.shape[:-2] + (64,))


def locality(f, species=None):
    """Écart relatif Σ|div_fd − div_exacte| / Σ|div_exacte| par fenêtre de demi-coups."""
    sl = slice(None) if species is None else species
    dex = f.div()[:, sl].reshape(f.div().shape[0], -1, 64).sum(1).astype(float)
    dfd = fd_divergence(f.D[:, sl].reshape(f.D.shape[0], -1, 64, 2).sum(1).astype(float))
    out = []
    for a, b in WINDOWS:
        num = np.abs(dfd[a:b] - dex[a:b]).sum()
        den = np.abs(dex[a:b]).sum()
        out.append(num / den if den else np.nan)
    return out


def window_flux(f, a, b):
    """Flux net moyen par partie et par demi-coup, toutes espèces : Σ_t J(t) / Σ_t N(t) (en pièces)."""
    J = f.J()[a:b].sum(1).sum(0).astype(float)
    return J / (W * f.N[a:b].sum())


def main(prefix):
    paths = sorted(glob.glob(os.path.join(os.path.dirname(prefix), "flow_*.npz")),
                   key=lambda p: int(p.split("_")[-1].split(".")[0]))
    h = Hodge()
    print("Localité (test 5) : Σ|div_fd − div_exacte| / Σ|div_exacte|, toutes pièces, par fenêtre")
    print(f"{'Elo':>5s} " + " ".join(f"{a:>3d}-{b:<4d}" for a, b in WINDOWS) + "   | Hodge : fraction rotationnelle par fenêtre")
    for p in paths:
        fl, meta = load_flows(p)
        f = fl["abs"]
        assert not np.any(f.residual()), "continuité violée"
        loc = locality(f)
        rot = [h.fractions(window_flux(f, a, b))[1] for a, b in WINDOWS]
        elo = p.split("_")[-1].split(".")[0]
        print(f"{elo:>5s} " + " ".join(f"{x:8.3f}" for x in loc) + "   | " + " ".join(f"{x:6.3f}" for x in rot))
    # localité par type de pièce (dernière tranche lue, toutes fenêtres)
    print("\nLocalité par type de pièce (tranche", elo, "), fenêtres :", WINDOWS)
    for k, name in enumerate(PT_NAMES):
        print(f"  {name}  " + " ".join(f"{x:8.3f}" for x in locality(f, [k, k + 6])))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "data/blitz")
