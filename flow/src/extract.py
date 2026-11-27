"""Lecture EN FLUX d'un fichier mensuel Lichess (.pgn.zst sur stdin) -> parties Blitz par tranche d'Elo.

    curl -s --range 0-2000000000 URL | python3 src/extract.py --quota 20000 --out data/blitz

Sélection : cadence Blitz (durée estimée base + 40·incrément dans [180, 480[ s, définition Lichess),
partie classée standard, les deux joueurs dans la même tranche [800+200k, 1000+200k[, k = 0..8,
fin « Normal » ou « Time forfeit » (on écarte « Abandoned », « Rules infraction »).
Sortie : un fichier jsonl.gz par tranche : {w, b, eco, tc, res, term, san} (san = coups séparés par des espaces).
"""
import argparse, gzip, io, json, re, sys, time
import zstandard

BINS = [(800 + 200 * k, 1000 + 200 * k) for k in range(9)]
COMMENT = re.compile(r"\{[^}]*\}")
MOVENUM = re.compile(r"\d+\.(\.\.)?")
RESULTS = {"1-0", "0-1", "1/2-1/2", "*"}


def bin_of(we, be):
    for k, (lo, hi) in enumerate(BINS):
        if lo <= we < hi and lo <= be < hi:
            return k
    return None


def is_blitz(tc):
    try:
        base, inc = tc.split("+")
        d = int(base) + 40 * int(inc)
    except ValueError:
        return False
    return 180 <= d < 480


def games(stream):
    head, moves = {}, None
    for line in stream:
        if line.startswith("["):
            sp = line.find(" ")
            head[line[1:sp]] = line[sp + 2:line.rfind('"')]
        elif line.strip() and head:
            yield head, line
            head = {}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quota", type=int, default=20000)
    ap.add_argument("--out", default="data/blitz")
    a = ap.parse_args()
    outs = [gzip.open(f"{a.out}_{lo}.jsonl.gz", "wt") for lo, hi in BINS]
    count = [0] * len(BINS)
    seen = blitz = 0
    t0 = time.time()
    reader = zstandard.ZstdDecompressor().stream_reader(sys.stdin.buffer, read_across_frames=True)
    text = io.TextIOWrapper(reader, encoding="utf-8", errors="replace")
    try:
        for h, mt in games(text):
            seen += 1
            if seen % 500000 == 0:
                print(f"{seen/1e6:.1f} M parties lues, {time.time()-t0:.0f} s, par tranche : {count}", file=sys.stderr, flush=True)
            if not is_blitz(h.get("TimeControl", "")) or "Rated" not in h.get("Event", ""):
                continue
            blitz += 1
            if h.get("Termination") not in ("Normal", "Time forfeit"):
                continue
            try:
                k = bin_of(int(h["WhiteElo"]), int(h["BlackElo"]))
            except (KeyError, ValueError):
                continue
            if k is None or count[k] >= a.quota:
                continue
            san = " ".join(t for t in MOVENUM.sub(" ", COMMENT.sub(" ", mt)).split() if t not in RESULTS)
            if not san:
                continue
            outs[k].write(json.dumps(dict(w=int(h["WhiteElo"]), b=int(h["BlackElo"]), eco=h.get("ECO", "?"),
                                          tc=h["TimeControl"], res=h.get("Result"), term=h["Termination"], san=san)) + "\n")
            count[k] += 1
            if min(count) >= a.quota:
                break
    except zstandard.ZstdError as e:   # fin de flux tronquée par --range : normal
        print(f"fin du flux ({e.__class__.__name__})", file=sys.stderr)
    for o in outs:
        o.close()
    dt = time.time() - t0
    print(f"FIN : {seen} parties lues ({blitz} blitz classées) en {dt:.0f} s ; par tranche : {dict(zip([lo for lo,_ in BINS], count))}", file=sys.stderr)


if __name__ == "__main__":
    main()
