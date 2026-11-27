"""Exporte les données nécessaires aux scènes de la vidéo -> flow/video/data.npz (quelques centaines de Ko)."""
import glob, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
os.chdir(os.path.join(HERE, ".."))
from flow import load_flows, W, B_LOC
from hodge import Hodge, block_circulation
from reduce import view
from spectrum import spectra, LG, LC

H = Hodge()
WINS = [(0, 10), (10, 30), (30, 60), (60, 300)]
out = {}
ELOS = sorted(int(p.split("_")[-1].split(".")[0]) for p in glob.glob("data/flow_*.npz"))
for e in (800, 2400):
    fl, _ = load_flows(f"data/flow_{e}.npz"); f = fl["mine"]
    rho = f.S[:101].sum(1) / (2 * W * f.N[:101, None])            # densité des pièces d'UN joueur, t = 0..100
    out[f"rho_{e}"] = rho
    out[f"alive_{e}"] = f.N[:101] / f.N[0]
    for k, (a, b) in enumerate(WINS):
        ntr = f.N[a + 1:b + 1].sum()
        J = f.J()[a:b].sum((0, 1)) / (W * ntr)
        out[f"J_{e}_{k}"] = J
        out[f"D_{e}_{k}"] = f.D[a:b].sum((0, 1)) / (W * ntr)
        out[f"div_{e}_{k}"] = J @ B_LOC
        g, c, h, phi, psi = H.decompose(J)
        out[f"phi_{e}_{k}"], out[f"g_{e}_{k}"], out[f"c_{e}_{k}"] = phi, g, c
        out[f"circ_{e}_{k}"] = block_circulation(c)
    # par type de pièce, fin de partie
    Js = f.J()[60:].sum(0).astype(float)
    out[f"species_rot_{e}"] = np.array([H.fractions(Js[k])[1] for k in range(6)])
# tendances (indicateurs pré-enregistrés, référentiel absolu) avec IC
for key, k in (("rot", 3), ("ent", 0), ("conv", 1), ("rot", 0)):
    c, lo, hi, ctrl = [], [], [], []
    for e in ELOS:
        d = np.load(f"data/stats_{e}.npz")
        c.append(d[f"{key}.c"][k]); b = d[f"{key}.boot"][:, k]
        lo.append(np.percentile(b, 2.5)); hi.append(np.percentile(b, 97.5)); ctrl.append(d[f"ctrl.{key}.c"][k])
    out[f"trend_{key}_{k}"] = np.array([c, lo, hi, ctrl])
out["elos"] = np.array(ELOS)
# cartes : prises (10-30) et autour du roi adverse (10-30), Lichess 800/2400 et témoin
for tag, e, src in (("800", 800, "central"), ("2400", 2400, "central"), ("ctrl", 800, "ctrl.central")):
    c = np.load(f"data/stats_{e}.npz")[src][0]
    K = view(c, "Kw")[1]; out[f"capt_{tag}"] = K / K.sum()
    out[f"king_{tag}"] = (-view(c, "Zw")[1] / (W * view(c, "Nw")[1]))[3:12, 3:12]
    out[f"coh_{tag}"] = np.array([np.load(f"data/stats_{e}.npz")[f"{'ctrl.' if tag == 'ctrl' else ''}coh.c"]][0])
# spectres (fin de partie et développement)
for tag, e, src in (("800", 800, "central"), ("2400", 2400, "central"), ("ctrl", 800, "ctrl.central")):
    c = np.load(f"data/stats_{e}.npz")[src]
    for k in (1, 3):
        eg, ec = spectra(c, k)
        out[f"spec_g_{tag}_{k}"], out[f"spec_c_{tag}_{k}"] = eg, ec
out["LG"], out["LC"] = LG, LC
np.savez_compressed(os.path.join(HERE, "data.npz"), **out)
print("data.npz :", os.path.getsize(os.path.join(HERE, "data.npz")) // 1024, "Ko ;", len(out), "tableaux")
