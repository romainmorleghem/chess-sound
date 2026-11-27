"""Étapes 3-4 : indicateurs par tranche d'Elo avec IC bootstrap (sur les parties), stabilité, témoin 1.

    python3 src/stats.py data/blitz [--n N] [--ctrl 5000] [--R 200] [--jobs 4]

Sorties : data/stats_<elo>.npz (indicateurs : central, ECO, moitiés, réplicats bootstrap ; témoin) et un tableau.
"""
import os
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import argparse, glob, gzip, json, sys, time
from multiprocessing import Pool
import numpy as np
import chess
sys.path.insert(0, os.path.dirname(__file__))
from flow import game_record, random_game, W
from reduce import reduce_record, view, DIM, TA, WINDOWS
from hodge import Hodge

CHUNK = 500
H = Hodge()
NAMES = ["act", "rot", "coh", "ent", "conv"]


def indicators(v):
    """v[..., DIM] (sommes pondérées) -> dict d'indicateurs (4 fenêtres chacun ; act : 4 fenêtres en t < TA)."""
    v = np.asarray(v, float)
    Jt, At = view(v, "Jt"), view(v, "At")
    act_t = np.abs(Jt).sum(-1) / (W * np.maximum(At, 1e-12))              # [.., TA]
    wins_t = [(a, min(b, TA)) for a, b in WINDOWS]
    act = np.stack([act_t[..., a:b].mean(-1) for a, b in wins_t], -1)
    rot = H.fractions(view(v, "Jw"))[..., 1]                              # [.., 4]
    Sw, Dw, D2w = view(v, "Sw"), view(v, "Dw"), view(v, "D2w")
    with np.errstate(invalid="ignore", divide="ignore"):
        m = np.sqrt((Dw ** 2).sum(-1)) / Sw
        rms = np.sqrt(D2w / Sw)
        c = np.where(Sw > 0, m / rms, 0)
        coh = (np.nan_to_num(c) * Sw).sum(-1) / Sw.sum(-1)
        K = view(v, "Kw")
        p = K / K.sum(-1, keepdims=True)
        ent = -(np.where(p > 0, p * np.log2(np.where(p > 0, p, 1)), 0)).sum(-1)
    Z = view(v, "Zw")
    conv = -Z[..., 5:10, 5:10].sum((-1, -2)) / (W * view(v, "Nw"))        # arrivées nettes / transition, |Δ| ≤ 2
    return dict(act=act, rot=rot, coh=coh, ent=ent, conv=conv, act_t=act_t)


def eco_group(e):
    return e[:2] if len(e) >= 2 and e[0] in "ABCDE" else "??"


def parse_san(san):
    b = chess.Board(); out = []
    for tok in san.split():
        mv = b.parse_san(tok.rstrip("?!")); out.append(mv); b.push(mv)
    return out


def accumulate(games, weights_fn, R, seed, checkpoints=()):
    """games : itérable de listes de coups. Retourne sommes [rows, DIM] (+ instantanés aux checkpoints)."""
    rng = np.random.default_rng(seed)
    rows = 4 + 2 * R
    acc = np.zeros((rows, DIM))
    snaps = {}
    X = np.zeros((CHUNK, DIM), np.float32)
    Wc = np.zeros((rows, CHUNK))
    n = k = 0
    for moves, ew in games:
        X[k] = 0
        reduce_record(game_record(moves), X[k])
        po = rng.poisson(1.0, R)
        half = rng.integers(2)
        Wc[:, k] = np.concatenate([[1, ew, half == 0, half == 1], po, po * ew])
        k += 1; n += 1
        if k == CHUNK or n in checkpoints:
            acc += Wc[:, :k] @ X[:k]
            k = 0
            if n in checkpoints:
                snaps[n] = acc.copy()
    if k:
        acc += Wc[:, :k] @ X[:k]
    return acc, snaps, n


def summarize(acc, R):
    ind = indicators(acc)
    out = {}
    for name in NAMES + ["act_t"]:
        x = ind[name]
        out[f"{name}.c"], out[f"{name}.eco"] = x[0], x[1]
        out[f"{name}.hA"], out[f"{name}.hB"] = x[2], x[3]
        out[f"{name}.boot"], out[f"{name}.bootE"] = x[4:4 + R], x[4 + R:]
    return out


def run(path, n, n_ctrl, R, eco_target):
    t0 = time.time()
    elo = path.split("_")[-1].split(".")[0]
    rows = [json.loads(l) for l in gzip.open(path, "rt")]
    if n:
        rows = rows[:n]
    groups = [eco_group(r["eco"]) for r in rows]
    cnt = {}
    for g in groups:
        cnt[g] = cnt.get(g, 0) + 1
    ew = np.array([eco_target.get(g, 0) / (cnt[g] / len(rows)) for g in groups])
    N = len(rows)
    cps = tuple(sorted({N // 4, N // 2}))
    games = ((parse_san(r["san"])[:400], w) for r, w in zip(rows, ew))
    acc, snaps, n_done = accumulate(games, None, R, seed=int(elo), checkpoints=cps)
    out = summarize(acc, R)
    for cp, a in snaps.items():                    # test 6 : largeur des IC selon N
        s = summarize(a, R)
        for name in NAMES:
            out[f"{name}.sd_{cp}"] = s[f"{name}.boot"].std(0)
    out["N"], out["checkpoints"] = np.array(N), np.array(cps)
    out["central"] = acc[:4]
    # témoin 1 : coups légaux au hasard, longueurs tirées dans la distribution de la tranche
    T = np.array([len(r["san"].split()) for r in rows])
    rng = np.random.default_rng(1000 + int(elo))
    ctrl = ((random_game(rng, int(min(rng.choice(T), 400))), 1.0) for _ in range(n_ctrl))
    acc_c, _, _ = accumulate(ctrl, None, R, seed=2000 + int(elo))
    sc = summarize(acc_c, R)
    for k_, v in sc.items():
        out["ctrl." + k_] = v
    out["ctrl.central"] = acc_c[:4]
    np.savez_compressed(os.path.join(os.path.dirname(path), f"stats_{elo}.npz"), **out)
    return elo, N, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--ctrl", type=int, default=5000)
    ap.add_argument("--R", type=int, default=200)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    paths = sorted(glob.glob(f"{a.prefix}_*.jsonl.gz"), key=lambda p: int(p.split("_")[-1].split(".")[0]))
    # mélange d'ouvertures cible : toutes tranches réunies, à poids égal par tranche
    target = {}
    for p in paths:
        rows = [json.loads(l)["eco"] for l in gzip.open(p, "rt")][: a.n or None]
        for e in rows:
            g = eco_group(e)
            target[g] = target.get(g, 0) + 1 / len(rows) / len(paths)
    with Pool(a.jobs) as pool:
        res = pool.starmap(run, [(p, a.n, a.ctrl, a.R, target) for p in paths])
    for elo, N, dt in res:
        print(f"{elo:>5s} {N:6d} parties  {dt:6.0f} s", flush=True)


if __name__ == "__main__":
    main()
