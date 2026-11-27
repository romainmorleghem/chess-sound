"""s01 · Density: ρ(x, t) for 800 vs 2400; games end (exit)."""
from fc import Narrated, Board, DATA, np, FG, MUTED, GOLD, UP, DOWN, LEFT, RIGHT, linear
from manim import FadeIn, FadeOut, Write, Text, MathTex, Tex, VGroup, UpdateFromAlphaFunc


class Density(Narrated):
    def construct(self):
        self.chapter("1 · Density")
        eq = MathTex(r"\rho(x,t) = \frac{\#\{\text{games with a piece on } x \text{ at half-move } t\}}{\#\{\text{games still running}\}}",
                     font_size=36).to_edge(UP, buff=1.0)
        self.say("First quantity: the density. For each square x and each half-move t, the fraction of games that have "
                 "a piece there.", Write(eq))
        r8, r24 = DATA["rho_800"], DATA["rho_2400"]
        vmax = max(r8.max(), r24.max())
        b1 = Board(0.5).paint(r8[0], vmax=vmax).shift(3.3 * LEFT + 0.7 * DOWN)
        b2 = Board(0.5).paint(r24[0], vmax=vmax).shift(3.3 * RIGHT + 0.7 * DOWN)
        l1 = Text("800-1000 Elo", font_size=26, color=FG).next_to(b1, UP, buff=0.2)
        l2 = Text("2400-2600 Elo", font_size=26, color=FG).next_to(b2, UP, buff=0.2)
        tl = Text("t = 0", font_size=28, color=GOLD).move_to(0.7 * DOWN)
        note = Text("each player seen from their own side", font_size=20, color=MUTED).next_to(VGroup(b1, b2), DOWN, buff=0.3)
        self.say("We compare beginners, around 900, with masters, around 2500. Twenty thousand games each. "
                 "And we turn the board for Black, so every player marches upwards.",
                 FadeIn(b1), FadeIn(b2), FadeIn(l1), FadeIn(l2), FadeIn(tl), FadeIn(note))

        def upd(m, a):
            t = int(a * 100)
            b1.paint(r8[t], vmax=vmax); b2.paint(r24[t], vmax=vmax)
            tl.become(Text(f"t = {t}", font_size=28, color=GOLD).move_to(0.7 * DOWN))
        d = self.voice("Watch a hundred half-moves. The camp empties, pieces fan out to the centre, and the board "
                       "slowly drains as pieces are captured.")
        self.play(UpdateFromAlphaFunc(VGroup(b1, b2), upd, rate_func=linear), run_time=max(d + 0.5, 8))
        a8, a24 = DATA["alive_800"][100] * 100, DATA["alive_2400"][100] * 100
        self.say(f"One catch: games end. After a hundred half-moves, only {a8:.0f} percent of beginners' games are "
                 f"still running, against {a24:.0f} percent for masters. We keep track of games leaving the ensemble, "
                 "exactly, like water leaving through a drain.")
        self.play(FadeOut(VGroup(eq, b1, b2, l1, l2, tl, note)), run_time=0.6)
