"""Spectre d'énergie du flux moyen sur les modes propres du graphe (analogue discret du spectre de Fourier).

Modes gradient : B v / √λ, v vecteur propre du laplacien des cases L0 = BᵀB (63 modes, λ > 0).
Modes rotationnels : Cᵀ u / √μ, u vecteur propre de C Cᵀ (147 modes, μ > 0).
λ, μ jouent le rôle de k² : petit = grande échelle, grand = petite échelle.
Énergie sans biais du mode m : (J_A · m)(J_B · m), J_A et J_B = flux des deux moitiés indépendantes.
"""
import glob, os, sys
import numpy as np
import scipy.linalg as sla
sys.path.insert(0, os.path.dirname(__file__))
from hodge import Hodge
from reduce import view
from flow import W

H = Hodge()


def modes():
    l0, V = sla.eigh(H.B.T @ H.B)
    g = [(l, H.B @ v / np.sqrt(l)) for l, v in zip(l0, V.T) if l > 1e-9]
    l2, U = sla.eigh(H.C @ H.C.T)
    c = [(m, H.C.T @ u / np.sqrt(m)) for m, u in zip(l2, U.T) if m > 1e-9]
    return (np.array([x[0] for x in g]), np.array([x[1] for x in g]),
            np.array([x[0] for x in c]), np.array([x[1] for x in c]))


LG, MG, LC, MC = modes()
BINS = np.geomspace(0.1, 40, 9)


def spectra(c, win):
    JA = view(c[2], "Jw")[win] / (W * view(c[2], "Nw")[win])
    JB = view(c[3], "Jw")[win] / (W * view(c[3], "Nw")[win])
    eg = (MG @ JA) * (MG @ JB)
    ec = (MC @ JA) * (MC @ JB)
    return eg, ec


def binned(lam, e):
    idx = np.digitize(lam, BINS) - 1
    return np.array([e[idx == k].sum() if np.any(idx == k) else np.nan for k in range(len(BINS) - 1)])


def slope(lam, e):
    """Pente log-log de l'énergie par mode en fonction de λ (k² ; pente en k = 2 × pente en λ)."""
    m = e > 0
    return np.polyfit(np.log(lam[m]), np.log(e[m]), 1)[0]


def main(win=3):
    print(f"Spectre d'énergie, fenêtre {['0-10','10-30','30-60','≥60'][win]} (énergie sans biais ; fraction aux grandes échelles λ<1)")
    print(f"{'Elo':>5s}  {'E_grad':>8s} {'E_rot':>8s} {'rot':>6s}  {'grad λ<1':>8s} {'rot μ<1':>8s}   pentes log-log (grad, rot)   | témoin pentes")
    for p in sorted(glob.glob("data/stats_*.npz"), key=lambda p: int(p.split("_")[-1].split(".")[0])):
        d = np.load(p); e = p.split("_")[-1].split(".")[0]
        eg, ec = spectra(d["central"], win)
        tg, tc = spectra(d["ctrl.central"], win)
        Eg, Ec = eg.sum(), ec.sum()
        print(f"{e:>5s}  {Eg:8.4f} {Ec:8.4f} {Ec/(Eg+Ec):6.3f}  {eg[LG<1].sum()/Eg:8.3f} {ec[LC<1].sum()/Ec:8.3f}"
              f"   {slope(LG, eg):+6.2f} {slope(LC, ec):+6.2f}              | {slope(LG, tg):+6.2f} {slope(LC, tc):+6.2f}")


if __name__ == "__main__":
    for w in (1, 3):
        main(w)
