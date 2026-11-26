"""s05 · Symmetry and ambiguity: D4, degenerate modes, any mix is a mode, adapted basis, sound is basis-free."""
from _common import Narrated, Board, modes, np, FG, MUTED, BAND, ACCENT, UP, DOWN, LEFT, RIGHT, PI, linear
from manim import FadeIn, FadeOut, Rotate, Text, Tex, MathTex, VGroup, UpdateFromAlphaFunc, LaggedStart, Write


class Symmetry(Narrated):
    def construct(self):
        self.chapter("5 · Symmetry and ambiguity")
        w, V, lab = modes("N")
        b = Board(0.62).paint(V[:, 4])
        self.play(FadeIn(b), run_time=0.5)
        d = self.voice("A chessboard looks the same if you turn it a quarter turn, or flip it in a mirror. "
                       "There are eight such moves: four rotations and four reflections. "
                       "Mathematicians call this group D4.")
        rt = (d + 0.3) / 3
        self.play(Rotate(b, PI / 2), run_time=rt)
        self.play(Rotate(b, PI, axis=UP), run_time=rt)
        self.play(Rotate(b, PI, axis=np.array([1.0, 1.0, 0])), run_time=rt)
        self.play(FadeOut(b), run_time=0.4)

        v1, v2 = V[:, 1], V[:, 2]
        b1 = Board(0.36).paint(v1).shift(4.6 * LEFT)
        b2 = Board(0.36).paint(v2).shift(1.2 * LEFT)
        f = 220 * np.sqrt(w[1])
        t1 = Text(f"{f:.0f} Hz", font_size=24, color=MUTED).next_to(b1, DOWN)
        t2 = Text(f"{f:.0f} Hz", font_size=24, color=MUTED).next_to(b2, DOWN)
        self.say("So if you turn a mode, you get a mode again, with the same frequency. Sometimes it's a new "
                 "shape: then two different modes share one note. Here, the knight's lowest note, twice.",
                 FadeIn(b1), FadeIn(t1), FadeIn(b2), FadeIn(t2))
        b3 = Board(0.36).paint(v1).shift(3.9 * RIGHT)
        mix = MathTex(r"\cos\theta\, v_1 + \sin\theta\, v_2", font_size=34).next_to(b3, DOWN)

        def upd(m, a):
            th = 2 * PI * a
            m.paint(np.cos(th) * v1 + np.sin(th) * v2, vmax=np.abs(v1).max())
        self.say("And then any mix of the two is a mode too, with the same note. There is a whole circle of "
                 "them, and none is more natural than the others.", FadeIn(b3), FadeIn(mix))
        self.play(UpdateFromAlphaFunc(b3, upd, rate_func=linear), run_time=5.0)
        self.play(FadeOut(VGroup(b1, b2, b3, t1, t2, mix)), run_time=0.5)

        picks = {}
        for k in range(1, 64):
            picks.setdefault(lab[k]["irrep"], k)
        names = {"A1": "unchanged by all 8", "A2": "flips sign in mirrors", "B1": "flips sign in quarter turns",
                 "B2": "flips in quarter turns\nand axis mirrors", "E": "comes in pairs"}
        row = VGroup()
        for r in ("A1", "A2", "B1", "B2", "E"):
            bb = Board(0.21).paint(V[:, picks[r]])
            row.add(VGroup(Tex(r if r != "E" else "E", font_size=40, color=BAND), bb,
                           Text(names[r], font_size=17, color=MUTED, line_spacing=1.0)).arrange(DOWN, buff=0.2))
        row.arrange(RIGHT, buff=0.4, aligned_edge=UP)
        row.scale_to_fit_width(min(row.width, 12.5))
        self.say("To pick, we sort the modes by how they react to the eight symmetries: unchanged, or flipping "
                 "sign, in a definite way. There are exactly five possible behaviours, called the irreducible "
                 "representations of D4. Pairs that share a note are chosen to be even or odd in the mirrors.",
                 LaggedStart(*[FadeIn(x) for x in row], lag_ratio=0.25), run_time=3.0)
        self.say("The good news: the sound will not depend on this choice. We'll only use how much energy each "
                 "frequency receives, and that is the same whichever mix you take.")
        self.play(FadeOut(row), run_time=0.6)
