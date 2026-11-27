"""s06 · Constraints: pendulum with a Lagrange multiplier; λ turns out to be the tension."""
from lc import (Narrated, np, VGroup, Line, Arrow, Dot, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, UP, DOWN, LEFT, RIGHT,
                ball, ceiling, pendulum_sol)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, Brace, ValueTracker, always_redraw, linear,
                   DashedVMobject, Circle, SurroundingRectangle)


class Constraint(Narrated):
    def construct(self):
        self.chapter("6 · Constraints for free")
        L = MathTex(r"L =", r"\tfrac12 m(\dot x^2+\dot y^2) - mgy", r"+", r"\lambda\,(x^2+y^2-\ell^2)", font_size=42).to_edge(UP, buff=1.0)
        b1 = Brace(L[1], DOWN, color=GREEN); t1 = Text("free fall", font_size=22, color=GREEN).next_to(b1, DOWN, buff=0.1)
        b2 = Brace(L[3], DOWN, color=TEAL); t2 = Text("constraint", font_size=22, color=TEAL).next_to(b2, DOWN, buff=0.1)
        self.say("Back to the pendulum, written another way: as a free falling ball, plus a constraint "
                 "keeping it on a circle of radius l, multiplied by a new unknown, lambda.", Write(L), FadeIn(b1), FadeIn(t1), FadeIn(b2), FadeIn(t2))
        eqs = VGroup(MathTex(r"m\ddot x = 2\lambda x", font_size=38), MathTex(r"m\ddot y = 2\lambda y - mg", font_size=38),
                     MathTex(r"0 = x^2+y^2-\ell^2", font_size=38)).arrange(DOWN, buff=0.25, aligned_edge=LEFT).shift(2.8 * RIGHT + 0.2 * DOWN)
        self.say("Treat x, y and lambda as three coordinates and apply Euler-Lagrange to each. The equation for lambda "
                 "just gives back the constraint.", Write(eqs))
        res = VGroup(MathTex(r"\ddot\theta + \frac{g}{\ell}\sin\theta = 0", font_size=40, color=GOLD),
                     MathTex(r"\lambda = -\frac{T}{2\ell}", font_size=44, color=BLUE)).arrange(RIGHT, buff=0.8).next_to(eqs, DOWN, buff=0.45)
        self.say("Put x equals l sine theta, y equals minus l cos theta, and the pendulum equation falls out. "
                 "And lambda? It is the tension of the rod, up to a factor.", Write(res[0]), Write(res[1]))
        piv = 0.1 * DOWN + 3.8 * LEFT
        l = 2.0
        ts, th, om = pendulum_sol(1.3, 9.81, 1.0, 6)
        Ten = 9.81 * np.cos(th) + om ** 2                     # T/m (l = 1)
        k = ValueTracker(0)
        bob = lambda: piv + l * np.array([np.sin(th[int(k.get_value())]), -np.cos(th[int(k.get_value())]), 0])
        circ = DashedVMobject(Circle(radius=l, color=TEAL, stroke_width=2).move_to(piv), num_dashes=60)
        rod = always_redraw(lambda: Line(piv, bob(), color=FG, stroke_width=3))
        bb = always_redraw(lambda: ball(GOLD, 0.15).move_to(bob()))
        tens = always_redraw(lambda: Arrow(bob(), bob() + (piv - bob()) / l * 0.09 * Ten[int(k.get_value())], buff=0, color=BLUE, stroke_width=5))
        d = self.voice("So the multiplier does double duty: it enforces the rod, and it measures how hard the rod pulls. "
                       "Watch the tension, in blue, peak at the bottom of each swing.")
        self.play(FadeIn(ceiling(2.0, piv)), Create(circ), FadeIn(rod), FadeIn(bb), FadeIn(tens), run_time=1)
        self.play(k.animate.set_value(len(th) - 1), run_time=max(d, 6), rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
