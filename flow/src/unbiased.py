"""Correction du biais de bruit (moitiés indépendantes A et B) :
- énergie sans biais d'une partie P du flux : (P J_A) · (P J_B)  (le bruit de A et celui de B ne se corrèlent pas) ;
- plancher de bruit de l'activité : Σ|(J_A − J_B)/2| (pur bruit, à l'échelle de l'échantillon complet)."""
import glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from reduce import view, WINDOWS, TA
from hodge import Hodge
from flow import W

H = Hodge()
WL = ["0-10", "10-30", "30-60", "≥60"]


def norm_J(v):
    return view(v, "Jw") / (W * view(v, "Nw"))[..., None]


def rot_unbiased(c):
    JA, JB = norm_J(c[2]), norm_J(c[3])
    gA, cA, _, _, _ = H.decompose(JA); gB, cB, _, _, _ = H.decompose(JB)
    Eg, Ec = (gA * gB).sum(-1), (cA * cB).sum(-1)
    return Ec / (Eg + Ec)


def activity_floor(c):
    out = []
    for v in (c[0], c[2], c[3]):
        out.append(view(v, "Jt") / (W * np.maximum(view(v, "At"), 1e-12))[..., None])
    J, JA, JB = out
    noise = np.abs((JA - JB) / 2).sum(-1)
    act = np.abs(J).sum(-1)
    wins = [(a, min(b, TA)) for a, b in WINDOWS]
    return np.array([act[a:b].mean() for a, b in wins]), np.array([noise[a:b].mean() for a, b in wins])


def main(which="central"):
    paths = sorted(glob.glob("data/stats_*.npz"), key=lambda p: int(p.split("_")[-1].split(".")[0]))
    print("Fraction rotationnelle SANS BIAIS (produit croisé des moitiés)  |  témoin")
    print(f"{'Elo':>5s} " + " ".join(f"{w:>7s}" for w in WL) + "   | " + " ".join(f"{w:>7s}" for w in WL))
    for p in paths:
        d = np.load(p); e = p.split("_")[-1].split(".")[0]
        r, rc = rot_unbiased(d["central"]), rot_unbiased(d["ctrl.central"])
        print(f"{e:>5s} " + " ".join(f"{x:7.3f}" for x in r) + "   | " + " ".join(f"{x:7.3f}" for x in rc))
    print("\nActivité Σ|J| et plancher de bruit Σ|(J_A − J_B)/2| (même unité), par fenêtre")
    for p in paths:
        d = np.load(p); e = p.split("_")[-1].split(".")[0]
        a, n = activity_floor(d["central"])
        print(f"{e:>5s} " + " ".join(f"{x:6.3f} (bruit {y:5.3f})" for x, y in zip(a, n)))


if __name__ == "__main__":
    main()
