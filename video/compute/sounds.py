"""All sounds used by the scenes -> media/sounds/*.wav (≈ 10 s)."""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "data")]
import synth
from synth import Instrument, save, concat, SR
from melody import events, render
from games import OPENINGS, GAMES

OUT = ROOT / "media" / "sounds"


def tone(f, dur=1.6, amp=1.0):
    t = np.arange(int(dur * SR)) / SR
    return amp * np.sin(2 * np.pi * f * t) * np.exp(-t / (1.6 * 220 / f)) * np.minimum(1, t / 0.005)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for p in "RBNKQP":
        save(OUT / f"{p}_d4.wav", Instrument.cache(p).note("d4", "d1" if p == "R" else None, dur=2.2))
    N = Instrument.cache("N")
    save(OUT / "N_a1.wav", N.note("a1", dur=2.2))
    save(OUT / "R_chord.wav", Instrument.cache("R").note("d4", dur=3.0))
    # quiz: three pieces struck on e4 (rook as a move e1 -> e4)
    for k, p in enumerate("NQK"):
        save(OUT / f"quiz{k}.wav", Instrument.cache(p).note("e4", dur=2.2))
    # string harmonics and single modes of the knight (pure tones)
    for k in range(1, 4):
        save(OUT / f"string{k}.wav", tone(196 * k))
    w = np.linalg.eigvalsh(synth.laplacian(synth.adjacency("N")).astype(float))
    for k in (1, 3, 10, 63):
        save(OUT / f"Nmode{k}.wav", tone(220 * np.sqrt(w[k]), dur=2.0))
    # melodies (same rendering as src/melody.py)
    for key in ("italienne", "gambit_evans"):
        save(OUT / f"mel_{key}.wav", render(events(OPENINGS[key][1]), step=0.5))
    for key in ("opera", "immortelle"):
        save(OUT / f"mel_{key}.wav", render(events(GAMES[key]["moves"]), step=0.34))


if __name__ == "__main__":
    main()
