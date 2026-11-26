"""PGN -> mélodie (WAV + frise JSON) et score de « beauté musicale ».

Règles (cf. README) :
- un demi-coup = on frappe l'instrument de la pièce jouée (promotion : la nouvelle pièce) ;
  frappe en « arrivée », sauf la tour : « geste » arrivée - départ (sinon tous ses coups sonnent pareil) ;
- prise : accent ; roque : accord roi + tour ; échec : petite dissonance (demi-ton au-dessus
  de la note dominante) ; mat : accord final de résolution (majeur juste sur la note du mat) ;
- Blancs à gauche, Noirs à droite.
"""
import json, pathlib, re, subprocess, sys
import numpy as np
import chess

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data"))
from synth import Instrument, SR, save, F0
from graphs import parse

LETTER = {chess.PAWN: "P", chess.KNIGHT: "N", chess.BISHOP: "B", chess.ROOK: "R", chess.QUEEN: "Q", chess.KING: "K"}


def san_list(text):
    toks = [re.sub(r"^\d+\.(\.\.)?", "", t) for t in text.split()]
    return [t for t in toks if t and t not in ("1-0", "0-1", "1/2-1/2", "*")]


def events(text):
    """Liste d'événements musicaux pour une suite de coups SAN."""
    b = chess.Board()
    out = []
    for ply, san in enumerate(san_list(text)):
        mv = b.parse_san(san)
        piece = b.piece_at(mv.from_square)
        color = "w" if piece.color else "b"
        cap, castle = b.is_capture(mv), b.is_castling(mv)
        b.push(mv)
        p = LETTER[mv.promotion] if mv.promotion else LETTER[piece.piece_type]
        frm, to = chess.square_name(mv.from_square), chess.square_name(mv.to_square)
        strikes = [dict(piece=p, to=to, frm=frm if p == "R" else None)]
        if castle:  # accord roi + tour
            r = mv.to_square > mv.from_square
            rank = 0 if color == "w" else 7
            rf, rt = (chess.square(7, rank), chess.square(5, rank)) if r else (chess.square(0, rank), chess.square(3, rank))
            strikes.append(dict(piece="R", to=chess.square_name(rt), frm=chess.square_name(rf)))
        out.append(dict(ply=ply, san=san, color=color, piece=p, frm=frm, to=to, capture=cap,
                        castle=castle, check=b.is_check(), mate=b.is_checkmate(), strikes=strikes))
    return out


def note_spectrum(ev):
    """(fréquences, amplitudes) de la note principale d'un événement."""
    s = ev["strikes"][0]
    I = Instrument.cache(s["piece"])
    return I.freqs, I.amplitudes(s["to"], s["frm"])


def dominant(ev):
    f, a = note_spectrum(ev)
    return float(f[np.argmax(a)])


def _decay(f, t, amp=1.0, tau=None):
    tau = tau or 1.6 * F0 / f
    return amp * np.sin(2 * np.pi * f * t) * np.exp(-t / tau) * np.minimum(1, t / 0.004)


def render(evs, step=0.45, tail=2.2, pan=0.6):
    n = int((step * len(evs) + tail + 2.5) * SR)
    out = np.zeros((n, 2))
    t = np.arange(int(tail * SR)) / SR
    for k, ev in enumerate(evs):
        acc = 1.6 if ev["capture"] else 1.0
        y = sum(Instrument.cache(s["piece"]).note(s["to"], s["frm"], dur=tail, accent=acc) for s in ev["strikes"])
        if ev["check"] and not ev["mate"]:
            fd = dominant(ev)
            y = y + _decay(fd * 2 ** (1 / 12), t, amp=0.12, tau=0.5)
        p = -pan if ev["color"] == "w" else pan
        i0 = int(k * step * SR)
        out[i0:i0 + len(y), 0] += np.sqrt(1 - p) * y
        out[i0:i0 + len(y), 1] += np.sqrt(1 + p) * y
        ev["t"] = round(k * step, 3)
        ev["f_dom"] = round(dominant(ev), 2)
    if evs and evs[-1]["mate"]:  # résolution : accord majeur juste (1, 5/4, 3/2, 2) sur la note du mat
        f = evs[-1]["f_dom"]
        while f > 2 * F0:
            f /= 2
        t2 = np.arange(int(2.5 * SR)) / SR
        chord = sum(_decay(f * r, t2, amp=0.1, tau=2.0) for r in (1, 5 / 4, 3 / 2, 2))
        i0 = int((len(evs) * step + 0.15) * SR)
        out[i0:i0 + len(chord)] += chord[:, None]
    return out


# ------------------------------------------------------------- beauté -----
def sethares(f1, a1, f2, a2):
    """Rugosité de Sethares (1993) entre deux spectres (termes croisés seulement)."""
    F1, F2 = np.meshgrid(f1, f2, indexing="ij")
    A1, A2 = np.meshgrid(a1, a2, indexing="ij")
    fmin, df = np.minimum(F1, F2), np.abs(F1 - F2)
    s = 0.24 / (0.021 * fmin + 19)
    return float(np.sum(np.minimum(A1, A2) * (np.exp(-3.5 * s * df) - np.exp(-5.75 * s * df))))


def _ratios(qmax=12):
    out = []
    for q in range(1, qmax + 1):
        for p in range(q, 2 * q + 1):
            if np.gcd(p, q) == 1:
                out.append((p, q, 1200 * np.log2(p / q), np.log2(p * q)))
    return out


RATIOS = _ratios()


def simplicity(f1, f2):
    """Consonance d'un intervalle : rapport simple proche (hauteur de Tenney log2(p·q),
    tolérance ~15 cents). Unisson / octave = 1, quinte ≈ 0,28, triton ≈ 0,1."""
    c = abs(1200 * np.log2(f2 / f1)) % 1200
    best = 0.0
    for p, q, cents, H in RATIOS:
        err = min(abs(c - cents), abs(c - cents + 1200), abs(c - cents - 1200))
        best = max(best, np.exp(-err / 15) / (1 + H))
    return best


def scores(evs):
    if len(evs) < 2:
        return dict(simplicite=np.nan, rugosite=np.nan, unissons=np.nan)
    specs = []
    for ev in evs:
        f, a = note_spectrum(ev)
        m = f > 0
        specs.append((f[m], a[m] / np.linalg.norm(a[m])))
    dom = [dominant(ev) for ev in evs]
    sim = [simplicity(x, y) for x, y in zip(dom, dom[1:])]
    rug = [sethares(*s1, *s2) for s1, s2 in zip(specs, specs[1:])]
    uni = [abs(1200 * np.log2(y / x)) < 15 for x, y in zip(dom, dom[1:])]
    return dict(simplicite=float(np.mean(sim)), rugosite=float(np.mean(rug)), unissons=float(np.mean(uni)))


def random_baseline(n_games=300, plies=90, seed=0):
    """Scores de parties au hasard (coups légaux tirés uniformément), tronquées à n demi-coups."""
    rng = np.random.default_rng(seed)
    games = []
    for _ in range(n_games):
        b = chess.Board(); sans = []
        while len(sans) < plies and not b.is_game_over():
            mv = list(b.legal_moves)[rng.integers(b.legal_moves.count())]
            sans.append(b.san(mv)); b.push(mv)
        games.append(events(" ".join(sans)))
    return games


def zscore(evs, base):
    n = len(evs)
    ref = [scores(g[:n]) for g in base if len(g) >= n]
    me = scores(evs)
    z = {}
    for k in ("simplicite", "rugosite"):
        v = np.array([r[k] for r in ref])
        z[k] = (me[k] - v.mean()) / v.std()
    return me, z


def to_mp3(wav, mp3):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-b:a", "160k", str(mp3)], check=True)


if __name__ == "__main__":
    from games import OPENINGS, GAMES
    outdir = ROOT / "melodies"
    outdir.mkdir(exist_ok=True)
    items = [(k, t, s, 0.5) for k, (t, s) in OPENINGS.items()] + \
            [(k, g["title"], g["moves"], 0.34) for k, g in GAMES.items()]
    base = random_baseline()
    rows = []
    for key, title, moves, step in items:
        evs = events(moves)
        y = render(evs, step=step)
        wav = outdir / f"{key}.wav"
        save(wav, y)
        to_mp3(wav, outdir / f"{key}.mp3")
        me, z = zscore(evs, base)
        json.dump(dict(title=title, step=step, scores=me, z=z,
                       events=[{k: v for k, v in e.items() if k != "strikes"} for e in evs]),
                  open(outdir / f"{key}.json", "w"), ensure_ascii=False, indent=1)
        rows.append((title, len(evs), me["simplicite"], z["simplicite"], me["rugosite"], z["rugosite"], me["unissons"]))
    rows.sort(key=lambda r: -r[3])
    print(f"{'mélodie':32s} {'n':>3s} {'simpl.':>6s} {'z':>5s} {'rugos.':>6s} {'z':>5s} {'unis.':>5s}")
    for r in rows:
        print(f"{r[0]:32s} {r[1]:3d} {r[2]:6.3f} {r[3]:+5.2f} {r[4]:6.3f} {r[5]:+5.2f} {r[6]:5.2f}")
