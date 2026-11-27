"""s04 · Is chess a (local) fluid? Finite differences fail even on a diagonal step; error ≈ 2."""
from fc import Narrated, Board, np, FG, MUTED, GOLD, RED, BLUE, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Write, Text, MathTex, Tex, VGroup, Arrow


class Local(Narrated):
    def construct(self):
        self.chapter("4 · Is chess really a fluid?")
        t = Tex(r"In a fluid, matter only moves to \textbf{neighbouring} points:\\"
                r"the divergence is computed from the nearest neighbours (finite differences).", font_size=32).to_edge(UP, buff=1.0)
        self.say("A real fluid is local: water only moves to neighbouring points. That's why its divergence can be "
                 "computed with finite differences, from the four nearest neighbours.", FadeIn(t))
        b1 = Board(0.55).shift(3.4 * LEFT + 0.8 * DOWN)
        b2 = Board(0.55).shift(3.4 * RIGHT + 0.8 * DOWN)
        ex = np.zeros(64); ex[27] = 1; ex[36] = -1                   # d4 -> e5
        fd = np.zeros(64); fd[27] = 2; fd[28] = -1; fd[35] = -1
        b1.paint(ex, kind="div", vmax=2); b2.paint(fd, kind="div", vmax=2)
        a1 = Arrow(b1.pos(27), b1.pos(36), buff=0.05, color=FG, stroke_width=5)
        a2 = Arrow(b2.pos(27), b2.pos(36), buff=0.05, color=FG, stroke_width=5)
        l1 = Text("exact: +1 and −1", font_size=24, color=FG).next_to(b1, DOWN, buff=0.2)
        l2 = Text("finite differences: +2, −1, −1", font_size=24, color=FG).next_to(b2, DOWN, buff=0.2)
        self.say("Test it on the simplest move: one diagonal step, d4 to e5. Exactly, d4 loses one piece and e5 gains one. "
                 "Finite differences only know left, right, up and down: they spread the arrival over the wrong squares. "
                 "Already an error twice the signal.", FadeIn(b1), FadeIn(b2), FadeIn(a1), FadeIn(a2), FadeIn(l1), FadeIn(l2))
        self.play(FadeOut(VGroup(b1, b2, a1, a2, l1, l2)), run_time=0.5)
        r = VGroup(MathTex(r"\frac{\sum |\,\text{div}_{\text{fluid}} - \text{div}_{\text{exact}}|}{\sum|\text{div}_{\text{exact}}|} \approx 2",
                           font_size=44, color=GOLD),
                   Tex(r"at every Elo; bishops 3.3, rooks 3.8", font_size=32, color=MUTED)).arrange(DOWN, buff=0.4).shift(0.6 * DOWN)
        self.say("On real games, the error is about twice the signal, at every level, and worse for bishops and rooks "
                 "that slide across the board.", Write(r[0]), FadeIn(r[1]))
        self.say("So chess is not a local fluid. From now on we never use the smooth picture for numbers: everything "
                 "is computed exactly on the network of squares. The smooth flow lines are only for the eye.")
        self.play(FadeOut(VGroup(t, r)), run_time=0.6)
