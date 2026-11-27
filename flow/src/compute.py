"""Étape 2 : parties d'une tranche d'Elo -> champs d'écoulement agrégés (data/flow_<elo>.npz).

    python3 src/compute.py data/blitz [--n 1000] [--jobs 4]

Quatre accumulateurs, remplis à partir d'un seul rejeu par partie :
  abs     référentiel absolu, cavalier = deux chemins en L (analyse principale)
  mine    référentiel « mon camp » (échiquier retourné pour les Noirs)
  direct  absolu, cavalier = lien direct non local (sensibilité au choix du cavalier)
  surv    absolu, seulement les parties d'au moins T0 = 60 demi-coups (biais de survie, à comparer à « exit »)
Méta-données par partie (pour la repondération ECO et les longueurs) : T, eco, w, b, res.
"""
import argparse, glob, gzip, json, os, sys, time
from multiprocessing import Pool
import numpy as np
import chess
sys.path.insert(0, os.path.dirname(__file__))
from flow import Flow, game_record, save_flows

TMAX, T0 = 300, 60


def parse_san(san):
    b = chess.Board()
    out = []
    for tok in san.split():
        mv = b.parse_san(tok.rstrip("?!"))        # annotations des parties analysées : ?! ?? !! ...
        out.append(mv)
        b.push(mv)
    return out


def run(path, n=None):
    flows = dict(abs=Flow(TMAX, "abs", "L"), mine=Flow(TMAX, "mine", "L"),
                 direct=Flow(TMAX, "abs", "direct"), surv=Flow(TMAX, "abs", "L"))
    meta = dict(T=[], eco=[], w=[], b=[], res=[])
    bad = 0
    t0 = time.time()
    with gzip.open(path, "rt") as fh:
        for k, line in enumerate(fh):
            if n is not None and k >= n:
                break
            g = json.loads(line)
            try:
                moves = parse_san(g["san"])
            except ValueError:
                bad += 1
                continue
            Tg = len(moves)
            if Tg > TMAX:
                moves = moves[:TMAX]
                for f in flows.values():
                    f.truncated += 1
            rec = game_record(moves)
            flows["abs"].add_record(rec); flows["mine"].add_record(rec); flows["direct"].add_record(rec)
            if Tg >= T0:
                flows["surv"].add_record(rec)
            for key, v in (("T", Tg), ("eco", g["eco"]), ("w", g["w"]), ("b", g["b"]), ("res", g["res"])):
                meta[key].append(v)
    elo = path.split("_")[-1].split(".")[0]
    out = os.path.join(os.path.dirname(path), f"flow_{elo}{'' if n is None else '_n' + str(n)}.npz")
    save_flows(out, flows, **meta)
    dt = time.time() - t0
    ng = len(meta["T"])
    return elo, ng, bad, dt, float(np.mean(meta["T"])) if ng else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prefix")
    ap.add_argument("--n", type=int, default=None)
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    paths = sorted(glob.glob(f"{a.prefix}_*.jsonl.gz"), key=lambda p: int(p.split("_")[-1].split(".")[0]))
    with Pool(a.jobs) as pool:
        res = pool.starmap(run, [(p, a.n) for p in paths])
    print(f"{'Elo':>5s} {'parties':>8s} {'rejetées':>8s} {'durée moy.':>10s} {'temps (s)':>9s} {'ms/partie':>9s}")
    for elo, ng, bad, dt, Tm in res:
        print(f"{elo:>5s} {ng:8d} {bad:8d} {Tm:10.1f} {dt:9.1f} {1000*dt/max(ng,1):9.2f}")


if __name__ == "__main__":
    main()
