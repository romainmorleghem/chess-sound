"""Synthèse du son d'une pièce « frappée » sur une case.

Règle : un coup excite l'instrument de la pièce (réseau masses-ressorts L = D - A).
Pour chaque fréquence propre distincte f = F0·sqrt(λ) (λ > 0), l'amplitude est
    a_λ = || P_λ x ||,   x = e_arrivée            (frappe ponctuelle)
                         x = e_arrivée - e_départ  (option « geste » A -> B)
où P_λ est le projecteur sur l'espace propre de λ. Cette amplitude ne dépend pas
de la base choisie dans un espace propre dégénéré (contrairement à V_k[arrivée]
pris mode par mode) : c'est l'énergie déposée dans la fréquence f.
"""
import numpy as np
from scipy.io import wavfile
from graphs import adjacency, laplacian, parse, PIECES  # noqa: F401
from modes import levels, TOL

SR = 44100
F0 = 220.0          # f = F0 * sqrt(λ) : 113 Hz (pion) ... 1206 Hz (dame)
TAU0 = 1.6          # durée de vie (s) d'un mode à 220 Hz ; τ ∝ 1/f
TILT = 1.0          # amplitude × (220/f)^TILT : 1 = frappe physique (déplacement ∝ 1/ω), 0 = règle brute


class Instrument:
    def __init__(self, piece):
        self.piece = piece
        w, V = np.linalg.eigh(laplacian(adjacency(piece)).astype(float))
        self.levels = [(w[a:b].mean(), V[:, a:b]) for a, b in levels(w)]
        self.freqs = np.array([F0 * np.sqrt(l) if l > TOL else 0.0 for l, _ in self.levels])

    def amplitudes(self, to, frm=None):
        x = np.zeros(64)
        x[parse(to) if isinstance(to, str) else to] += 1
        if frm is not None:
            x[parse(frm) if isinstance(frm, str) else frm] -= 1
        a = np.array([np.linalg.norm(U.T @ x) for _, U in self.levels])
        a[self.freqs == 0] = 0  # mode λ = 0 (translation) ignoré
        a[self.freqs > 0] *= (220.0 / self.freqs[self.freqs > 0]) ** TILT
        return a

    def note(self, to, frm=None, dur=2.0, accent=1.0, drone=0.0):
        t = np.arange(int(dur * SR)) / SR
        a = self.amplitudes(to, frm)
        y = np.zeros_like(t)
        for f, ak in zip(self.freqs, a):
            if ak < 1e-9 or f <= 0:
                continue
            tau = TAU0 * (220.0 / f)
            y += ak * np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
        if drone:  # bourdon grave pour le mode λ = 0 (option)
            y += drone * np.sin(2 * np.pi * 55 * t) * np.exp(-t / 3)
        attack = np.minimum(1, t / (0.004 / accent))
        y *= attack
        rms = np.sqrt(np.mean(y[: int(0.3 * SR)] ** 2)) + 1e-12
        return accent * 0.12 * y / rms


def sequence(events, step=0.5, tail=2.0, stereo=False):
    """events : liste de dict(piece, to, frm=None, accent=1, pan=0 (-1 g, +1 d))."""
    n = int((step * len(events) + tail) * SR)
    out = np.zeros((n, 2))
    for k, ev in enumerate(events):
        y = Instrument.cache(ev["piece"]).note(ev["to"], ev.get("frm"), dur=tail, accent=ev.get("accent", 1.0))
        i0 = int(k * step * SR)
        pan = ev.get("pan", 0.0) if stereo else 0.0
        gl, gr = np.sqrt((1 - pan) / 2) * np.sqrt(2), np.sqrt((1 + pan) / 2) * np.sqrt(2)
        out[i0:i0 + len(y), 0] += gl * y[: n - i0]
        out[i0:i0 + len(y), 1] += gr * y[: n - i0]
    return out


_CACHE = {}


def _cache(piece):
    if piece not in _CACHE:
        _CACHE[piece] = Instrument(piece)
    return _CACHE[piece]


Instrument.cache = staticmethod(_cache)


def save(path, y):
    y = np.asarray(y)
    y = y / max(1e-9, np.abs(y).max()) * 0.89
    if y.ndim == 1:
        y = np.stack([y, y], 1)
    wavfile.write(path, SR, (y * 32767).astype(np.int16))


def concat(*parts, gap=0.3):
    sil = np.zeros((int(gap * SR), 2))
    out = []
    for p in parts:
        p = np.asarray(p)
        out += [p if p.ndim == 2 else np.stack([p, p], 1), sil]
    return np.concatenate(out)


if __name__ == "__main__":
    import pathlib
    from graphs import NAMES_FR
    out = pathlib.Path(__file__).resolve().parents[1] / "sounds"
    out.mkdir(exist_ok=True)
    N = _cache("N")
    save(out / "cavalier_a1.wav", N.note("a1", dur=2.5))
    save(out / "cavalier_d4.wav", N.note("d4", dur=2.5))
    save(out / "cavalier_coin_puis_centre.wav", concat(N.note("a1", dur=2.5), N.note("d4", dur=2.5), gap=0.4))
    R = _cache("R")
    save(out / "tour_accord.wav", R.note("d4", dur=3.0))
    save(out / "tour_gestes_a1a8_a1h1_a1h8.wav",
         concat(R.note("a8", "a1"), R.note("h1", "a1"), R.note("d4", "a1")))
    notes = [_cache(p).note("d4", dur=2.0) for p in PIECES]
    for p, y in zip(PIECES, notes):
        save(out / f"piece_{p}_d4.wav", y)
    save(out / "six_pieces_d4.wav", concat(*notes, gap=0.4))
    # petite phrase : coups de cavalier a1-b3-d4-f5-h6, Blancs à gauche
    tour = ["a1", "b3", "d4", "f5", "h6"]
    ev = [dict(piece="N", to=b, frm=a, pan=-0.6) for a, b in zip(tour, tour[1:])]
    save(out / "phrase_cavalier.wav", sequence(ev, step=0.45, stereo=True))

    print(f"{'pièce':9s} {'nb freq':>7s} {'f min':>7s} {'f max':>7s} {'centroïde d4':>12s}  3 plus fortes à d4 (Hz)")
    for p in PIECES:
        I = _cache(p)
        a = I.amplitudes("d4")
        top = np.argsort(a)[::-1][:3]
        nz = I.freqs[I.freqs > 0]
        cen = (a**2 @ I.freqs) / (a**2).sum()
        print(f"{NAMES_FR[p]:9s} {len(nz):7d} {nz.min():7.0f} {nz.max():7.0f} {cen:12.0f}  " +
              ", ".join(f"{I.freqs[k]:.0f}" for k in top))
    r = _cache("R")
    print("tour : 8 -> %.1f Hz, 16 -> %.1f Hz, rapport %.4f (= √2, triton)" % (r.freqs[1], r.freqs[2], r.freqs[2] / r.freqs[1]))


def fig_strike(piece, squares, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from graphs import NAMES_FR
    I = _cache(piece)
    fig, ax = plt.subplots(figsize=(8, 3))
    for k, s in enumerate(squares):
        a = I.amplitudes(s)
        m = I.freqs > 0
        ax.vlines(I.freqs[m] * (1 + 0.004 * k), 0, a[m] / a.max(), color=f"C{k}", lw=2, label=f"frappé en {s}")
    ax.set_xscale("log"); ax.set_xlabel("fréquence (Hz)"); ax.set_ylabel("amplitude relative")
    ax.set_title(f"{NAMES_FR[piece]} : même instrument, son différent selon la case frappée")
    ax.legend(); fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)


if __name__ == "__main__":
    fig_strike("N", ["a1", "d4"], pathlib.Path(__file__).resolve().parents[1] / "figures" / "cavalier_a1_vs_d4.png")
