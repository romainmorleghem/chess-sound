"""Champs pour la pièce artistique -> flow/video/art.npz : déplacement moyen D (« mon camp »), parties gradient et
rotationnelle (vecteurs aux cases), pour les 9 tranches × 4 phases, et en continu (fenêtre glissante) pour 1600."""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
os.chdir(os.path.join(HERE, ".."))
from flow import load_flows, W, EDGES
from hodge import Hodge

H = Hodge()
WINS = [(0, 10), (10, 30), (30, 60), (60, 300)]


def ev(J):
    V = np.zeros((64, 2))
    for k, (u, w) in enumerate(EDGES):
        d = np.array([w % 8 - u % 8, w // 8 - u // 8], float); d /= np.linalg.norm(d)
        V[u] += 0.5 * J[k] * d; V[w] += 0.5 * J[k] * d
    return V


out = {}
elos = sorted(int(p.split("_")[-1].split(".")[0]) for p in glob.glob("data/flow_*.npz"))
for e in elos:
    f = load_flows(f"data/flow_{e}.npz")[0]["mine"]
    Jt, Dt, N = f.J().sum(1).astype(float), f.D.sum(1).astype(float), f.N.astype(float)
    for k, (a, b) in enumerate(WINS):
        ntr = N[a + 1:b + 1].sum()
        J = Jt[a:b].sum(0) / (W * ntr)
        g, c, _, _, _ = H.decompose(J)
        out[f"D_{e}_{k}"] = Dt[a:b].sum(0) / (W * ntr)
        out[f"G_{e}_{k}"], out[f"C_{e}_{k}"] = ev(g), ev(c)
    if e == 1600:
        ts = np.arange(0, 91, 2)
        out["lapse_t"] = ts
        out["lapse_D"] = np.array([Dt[max(t - 5, 0):t + 5].sum(0) / (W * N[max(t - 5, 0) + 1:t + 6].sum()) for t in ts])
        out["lapse_rho"] = np.array([f.S[t].sum(0) / (2 * W * N[t]) for t in range(0, 91)])
out["elos"] = np.array(elos)
np.savez_compressed(os.path.join(HERE, "art.npz"), **out)
print("art.npz", os.path.getsize(os.path.join(HERE, "art.npz")) // 1024, "Ko")
