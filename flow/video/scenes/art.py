"""« How Chess Flows » : pièce contemplative, lignes de courant du flot moyen (interpolation décorative).

    manim -ql art.py HowChessFlows
Nappe sonore : modes propres du cavalier (projet chess-sound), transposés de deux octaves, un accord par tranche d'Elo.
"""
import sys
import numpy as np
from fc import Narrated, FLOW, ROOT, FG, MUTED, GOLD, BG, UP, DOWN, LEFT, RIGHT, linear
from artlib import ART, stream, arrows, ghost_board, vmax_of, SIZE
from manim import (FadeIn, FadeOut, Text, Tex, VGroup, Square, UpdateFromAlphaFunc, interpolate_color, ManimColor,
                   AnimationGroup)
import soundfile as sf

sys.path.insert(0, str(ROOT / "src"))
from synth import Instrument  # noqa: E402

SR = 44100
SND = ROOT / "media" / "flow_art" / "pad"
KN = np.sort(Instrument("N").freqs[Instrument("N").freqs > 0])


def pad(name, freqs, dur, amp=0.05):
    """Nappe : sinus légèrement désaccordés, attaque et relâche lentes."""
    SND.mkdir(parents=True, exist_ok=True)
    t = np.arange(int(dur * SR)) / SR
    y = np.zeros_like(t)
    for k, f in enumerate(freqs):
        for det in (-0.6, 0.0, 0.7):
            y += np.sin(2 * np.pi * (f + det) * t + k) / (1 + 0.6 * k)
        y += 0.15 * np.sin(2 * np.pi * 2 * f * t) / (1 + k)              # léger scintillement
    env = np.minimum(1, t / 1.8) * np.minimum(1, (dur - t) / 2.2)
    y *= env * amp / max(np.abs(y).max(), 1e-9) * 6
    path = SND / f"{name}.wav"
    sf.write(path, np.stack([y, np.roll(y, 300)], 1), SR)
    return str(path)


def chord(k):
    return KN[k:k + 4] / 4                                              # deux octaves plus bas


class HowChessFlows(Narrated):
    def label(self, s, size=30, color=MUTED):
        return Text(s, font_size=size, color=color).to_edge(DOWN, buff=0.35)

    def construct(self):
        board = ghost_board()
        # 1 · les pièces fondent ---------------------------------------------------------------------------
        rho = ART["lapse_rho"]
        cells = VGroup(*[Square(SIZE, stroke_width=0, fill_opacity=0).move_to(
            np.array([(i % 8 - 3.5) * SIZE, (i // 8 - 3.5) * SIZE, 0])) for i in range(64)])
        glow = lambda x: interpolate_color(ManimColor(BG), ManimColor("#3FC8B4"), min(1, x ** 0.6))
        for i, c in enumerate(cells):
            c.set_fill(glow(rho[0][i] / rho.max()), opacity=1)
        self.add_sound(pad("p0", chord(0), 18))
        self.play(FadeIn(board), FadeIn(cells), run_time=2)
        d = self.voice("A hundred and seventy-five thousand games of blitz, averaged into one.")

        def melt(m, a):
            r = rho[int(a * 60)]
            for i, c in enumerate(m):
                c.set_fill(glow(r[i] / rho.max()), opacity=1)
        self.play(UpdateFromAlphaFunc(cells, melt, rate_func=linear), run_time=max(d + 1, 7))
        vm1 = vmax_of([f"D_{e}_1" for e in ART["elos"]])
        sl = stream(ART["D_1600_1"], vm1)
        sl.start_animation(warm_up=False, flow_speed=1.0, time_width=0.6)
        title = Tex("How Chess Flows", font_size=64, color=FG).to_edge(UP, buff=0.25)
        d = self.voice("This is how chess flows.")
        self.play(FadeOut(cells), FadeIn(sl), FadeIn(title), run_time=2)
        self.wait(max(d, 4))
        # 2 · le voyage en Elo (développement, demi-coups 10-30) -------------------------------------------
        self.play(FadeOut(title), run_time=1)
        d = self.voice("From beginners to masters.")
        cur, lab = sl, self.label("development  ·  800 – 1000 Elo")
        for j, e in enumerate(ART["elos"]):
            self.add_sound(pad(f"e{e}", chord(1 + j), 6.5))
            nxt = stream(ART[f"D_{e}_1"], vm1)
            nxt.start_animation(warm_up=False, flow_speed=1.0, time_width=0.6)
            nl = self.label(f"development  ·  {e} – {e + 200} Elo")
            self.play(FadeOut(cur), FadeIn(nxt), FadeOut(lab) if j else FadeIn(nl), FadeIn(nl) if j else FadeIn(VGroup()),
                      run_time=1.2)
            self.remove(cur)
            cur, lab = nxt, nl
            self.wait(3.8)
        # 3 · une partie en accéléré (1600-1800) ------------------------------------------------------------
        self.add_sound(pad("lapse", chord(10), 30))
        d = self.voice("One game, from the first move to the endgame.")
        ts, Ds = ART["lapse_t"], ART["lapse_D"]
        vml = max(np.linalg.norm(D, axis=1).max() for D in Ds[2:])
        for t in range(2, len(ts), 4):
            nxt = stream(Ds[t], vml)
            nxt.start_animation(warm_up=False, flow_speed=1.0, time_width=0.6)
            nl = self.label(f"1600 – 1800 Elo  ·  half-move {ts[t]}")
            self.play(FadeOut(cur), FadeIn(nxt), FadeOut(lab), FadeIn(nl), run_time=1.0)
            self.remove(cur)
            cur, lab = nxt, nl
            self.wait(1.4)
        self.play(FadeOut(cur), FadeOut(lab), FadeOut(board), run_time=1.5)
        # 4 · tourbillons, puis pentes : débutants / maîtres --------------------------------------------------
        s2 = 0.6
        cL, cR = np.array([-3.45, -0.05, 0]), np.array([3.45, -0.05, 0])
        bL, bR = ghost_board(s2, cL), ghost_board(s2, cR)
        for part, txt, voice, snd in (("C", "whirlpools", "Take away the slope, and only the whirlpools remain. "
                                       "Beginners swirl. Masters, less.", chord(14)),
                                      ("G", "slopes", "And the slope: the steady pull towards the other side.", chord(18))):
            self.add_sound(pad(part, snd, 15))
            vm = vmax_of([f"{part}_800_3", f"{part}_2400_3"])
            L = stream(ART[f"{part}_800_3"], vm, size=s2, center=cL, density=0.12, width=2.0)
            R = stream(ART[f"{part}_2400_3"], vm, size=s2, center=cR, density=0.12, width=2.0)
            for x in (L, R):
                x.start_animation(warm_up=False, flow_speed=1.0, time_width=0.6)
            tl = Text("800 – 1000 Elo", font_size=26, color=MUTED).next_to(bL, DOWN, buff=0.25)
            tr = Text("2400 – 2600 Elo", font_size=26, color=MUTED).next_to(bR, DOWN, buff=0.25)
            head = Text(f"endgame  ·  {txt}", font_size=32, color=FG).to_edge(UP, buff=0.4)
            d = self.voice(voice)
            self.play(FadeIn(VGroup(bL, bR, tl, tr, head)), FadeIn(L), FadeIn(R), run_time=1.5)
            self.wait(max(d + 1, 9))
            self.play(FadeOut(VGroup(L, R, tl, tr, head)), run_time=1.2)
            self.remove(L, R)
        self.play(FadeOut(VGroup(bL, bR)), run_time=0.8)
        # 5 · final : champ de flèches + lignes -------------------------------------------------------------
        self.add_sound(pad("end", chord(0), 14))
        V = ART["D_2400_1"]
        sl = stream(V, vm1, width=1.4)
        sl.start_animation(warm_up=False, flow_speed=0.8, time_width=0.6)
        ar = arrows(V, vm1)
        note = Text("the lines between squares are imagined  ·  the averages are real", font_size=22,
                    color=MUTED).to_edge(DOWN, buff=0.35)
        d = self.voice("The lines between the squares are imagined. The averages are real.")
        self.play(FadeIn(board), FadeIn(sl), FadeIn(ar), FadeIn(note), run_time=2)
        self.wait(max(d, 4))
        end = Tex("How Chess Flows", font_size=72, color=FG)
        self.play(FadeOut(VGroup(ar, note)), FadeIn(end), sl.animate.set_opacity(0.35), run_time=2)
        self.wait(4)
        self.play(FadeOut(VGroup(end, board, sl)), run_time=2)
