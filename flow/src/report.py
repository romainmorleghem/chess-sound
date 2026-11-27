"""Tableaux de synthèse : indicateurs par tranche (IC 95 % bootstrap), ECO, témoin, stabilité (test 6), pente en Elo."""
import glob, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from reduce import WINDOWS

NAMES = {"act": "activité Σ|J|", "rot": "fraction rotationnelle", "coh": "cohérence",
         "ent": "entropie des prises (bits)", "conv": "convergence près du roi adverse"}
WL = ["0-10", "10-30", "30-60", "≥60"]


def load(prefix="data/stats"):
    paths = sorted(glob.glob(prefix + "_*.npz"), key=lambda p: int(p.split("_")[-1].split(".")[0]))
    return [(int(p.split("_")[-1].split(".")[0]), dict(np.load(p))) for p in paths]


def main():
    D = load()
    elos = np.array([e + 100 for e, _ in D])
    for key, title in NAMES.items():
        print(f"\n## {title}   (valeur ± demi-largeur IC 95 % ; [témoin])")
        print(f"{'Elo':>5s} " + " ".join(f"{w:>22s}" for w in WL) + "   ECO-repond. (≥60)")
        for e, d in D:
            c, b, ctrl = d[f"{key}.c"], d[f"{key}.boot"], d[f"ctrl.{key}.c"]
            lo, hi = np.nanpercentile(b, [2.5, 97.5], axis=0)
            cells = [f"{c[k]:7.3f}±{(hi[k]-lo[k])/2:5.3f} [{ctrl[k]:6.3f}]" for k in range(4)]
            print(f"{e:>5d} " + " ".join(f"{x:>22s}" for x in cells) + f"   {d[f'{key}.eco'][3]:7.3f}")
        # pente en Elo (par 1000 Elo), IC en combinant les réplicats indépendants des tranches
        R = min(d[f"{key}.boot"].shape[0] for _, d in D)
        for k in range(4):
            y = np.array([d[f"{key}.c"][k] for _, d in D])
            yb = np.array([d[f"{key}.boot"][:R, k] for _, d in D])        # [tranches, R]
            yE = np.array([d[f"{key}.bootE"][:R, k] for _, d in D])
            sl = np.polyfit(elos / 1000, y, 1)[0]
            slb = np.array([np.polyfit(elos / 1000, yb[:, r], 1)[0] for r in range(R)])
            slE = np.array([np.polyfit(elos / 1000, yE[:, r], 1)[0] for r in range(R)])
            ctrl = np.array([d[f"ctrl.{key}.c"][k] for _, d in D])
            slc = np.polyfit(elos / 1000, ctrl, 1)[0]
            print(f"   pente {WL[k]:>5s} : {sl:+.4f} /1000 Elo  IC95 [{np.percentile(slb,2.5):+.4f}, {np.percentile(slb,97.5):+.4f}]"
                  f"   ECO : [{np.percentile(slE,2.5):+.4f}, {np.percentile(slE,97.5):+.4f}]   témoin : {slc:+.4f}")
    # test 6 : stabilité et 1/√N
    print("\n## Test 6 — stabilité (deux moitiés) et largeur des IC selon N")
    zs, ratios = [], []
    for e, d in D:
        N = int(d["N"]); cps = d["checkpoints"]
        for key in NAMES:
            sd = d[f"{key}.boot"].std(0)
            diff = d[f"{key}.hA"] - d[f"{key}.hB"]
            zs.append(np.abs(diff) / (2 * sd))          # écart entre moitiés / écart-type attendu (≈ 2 sd_N)
            for cp in cps:
                ratios.append((N / cp, np.nanmedian(d[f"{key}.sd_{cp}"] / sd)))
    zs = np.concatenate(zs)
    print(f"   |moitié A − moitié B| / (2·sd) : médiane {np.nanmedian(zs):.2f}, 95e centile {np.nanpercentile(zs,95):.2f}"
          f"  (attendu pour du bruit pur : médiane ≈ 0,67, 95e ≈ 1,96)")
    for f in sorted({round(r[0], 1) for r in ratios}):
        v = [r[1] for r in ratios if round(r[0], 1) == f]
        print(f"   sd(N/{f:.0f}) / sd(N) : médiane {np.median(v):.2f}   (attendu √{f:.0f} = {np.sqrt(f):.2f})")


if __name__ == "__main__":
    main()
