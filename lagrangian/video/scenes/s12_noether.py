"""s12 · Symmetries and Noether's theorem (definition, statement, proof); free fall: x-shift -> m ẋ; pendulum: no rotation
symmetry, but time symmetry -> energy."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI, ball
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, ValueTracker, always_redraw, linear, TracedPath,
                   LaggedStart, DashedLine, SurroundingRectangle)


class Noether(Narrated):
    def construct(self):
        self.chapter("12 · Symmetries: Noether's theorem")
        d = VGroup(Tex(r"a \textbf{symmetry} of $(M, L)$: a diffeomorphism $g : M\to M$ such that", font_size=32),
                   MathTex(r"L\big(g_*(v)\big) = L(v) \qquad \text{for all } v\in TM", font_size=40, color=GOLD)).arrange(DOWN, buff=0.3).to_edge(UP, buff=1.0)
        self.say("Last idea, the deepest. A symmetry is a smooth, invertible map of M which, together with its "
                 "derivative acting on velocities, leaves the Lagrangian unchanged.", Write(d))
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 2, 1], x_length=8, y_length=2.6, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(0.9 * DOWN)
        par = lambda s: ax.plot(lambda x: 1.6 * (x - s) * (3 - (x - s)) / 2.25 * 0.95, x_range=[s, s + 3], color=GOLD, stroke_width=4)
        p0 = par(0.3)
        p1 = par(3.6).set_color(TEAL)
        gs = MathTex(r"g_s(x, y) = (x + s,\ y)", font_size=36).next_to(ax, UP, buff=0.2)
        self.say("Free fall: shift everything sideways by s. The Lagrangian does not contain x, only x dot, so it "
                 "doesn't notice. A whole family of symmetries, one for each s.", Create(ax), Create(p0), Write(gs))
        self.play(Create(p1), run_time=1.2)
        self.play(FadeOut(VGroup(ax, p0, p1, gs)), run_time=0.5)
        th = VGroup(Tex(r"\textbf{Theorem (Noether, 1918).} If $\{g_s\}_{s\in\mathbb R}$ is a group of symmetries, then", font_size=32),
                    MathTex(r"I(q, \dot q) = \sum_i \frac{\partial L}{\partial \dot q^i}(q,\dot q)\;\frac{d g_s^i}{ds}\Big|_{s=0}", font_size=40, color=GOLD),
                    Tex(r"is a conservation law.", font_size=32)).arrange(DOWN, buff=0.3).next_to(d, DOWN, buff=0.4)
        self.say("Emmy Noether's theorem: every one-parameter group of symmetries gives a conservation law, with an "
                 "explicit formula.", Write(th))
        self.play(FadeOut(d), th.animate.to_edge(UP, buff=0.9), run_time=0.6)
        pf = VGroup(MathTex(r"L(q, \dot q) = L\Big(g_s(q),\ \frac{\partial g_s}{\partial q}\,\dot q\Big) \quad \forall s", font_size=34),
                    MathTex(r"\xrightarrow{\ d/ds|_{s=0}\ }\quad 0 = \frac{dg_s}{ds}\,\frac{\partial L}{\partial q} + \frac{d}{dt}\Big(\frac{dg_s}{ds}\Big)\,\frac{\partial L}{\partial\dot q}", font_size=34),
                    MathTex(r"= \frac{dg_s}{ds}\,\frac{d}{dt}\Big(\frac{\partial L}{\partial\dot q}\Big) + \frac{d}{dt}\Big(\frac{dg_s}{ds}\Big)\,\frac{\partial L}{\partial\dot q} = \frac{d}{dt}\Big(\frac{dg_s}{ds}\,\frac{\partial L}{\partial\dot q}\Big)", font_size=34)
                    ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(0.8 * DOWN)
        self.say("The proof. Along a motion, the symmetry says L is the same for every s. Differentiate in s at zero.", Write(pf[0]), Write(pf[1]))
        self.say("Replace the derivative of L with respect to q using Euler-Lagrange: what remains is the time "
                 "derivative of a single quantity. It is zero, so that quantity is conserved.", Write(pf[2]))
        self.play(FadeOut(pf), run_time=0.5)
        # chute libre : m ẋ conservée
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=7, y_length=3, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(1.6 * DOWN + 1.5 * LEFT)
        vx, vy, g = 3.4, 6.2, 9.81
        tt = ValueTracker(0)
        pos = lambda t: ax.c2p(vx * t, vy * t - 0.5 * g * t * t)
        b = always_redraw(lambda: ball().move_to(pos(tt.get_value())))
        sh = always_redraw(lambda: Dot(ax.c2p(vx * tt.get_value(), 0), color=TEAL, radius=0.1))
        tr = TracedPath(b.get_center, stroke_color=GOLD, stroke_width=3)
        res = VGroup(MathTex(r"\frac{dg_s}{ds} = (1, 0)", font_size=34), MathTex(r"I = \frac{\partial L}{\partial\dot x} = m\dot x", font_size=40, color=TEAL),
                     Tex(r"horizontal momentum: conserved", font_size=28, color=TEAL)).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.6).shift(1.4 * DOWN)
        self.add(tr, b, sh)
        self.play(Create(ax), FadeIn(res[0]), run_time=0.8)
        d_ = self.voice("For the falling ball, the shift gives I equals m x dot: the horizontal momentum. Look at the "
                        "ball's shadow on the ground: it moves at constant speed. Vertically, gravity breaks the "
                        "symmetry, and nothing is conserved.")
        self.play(tt.animate.set_value(2 * vy / g), Write(res[1]), FadeIn(res[2]), run_time=max(d_, 4), rate_func=linear)
        self.play(FadeOut(VGroup(ax, b, sh, tr, res, th)), run_time=0.5)
        tbl = VGroup(*[VGroup(Tex(a, font_size=32), MathTex(r"\longrightarrow", font_size=32), Tex(b_, font_size=32, color=c)).arrange(RIGHT, buff=0.3)
                       for a, b_, c in (("free fall: shift in $x$", r"$m\dot x$ conserved", TEAL),
                                        (r"pendulum: rotation $\theta\mapsto\theta+s$", r"not a symmetry: $\cos\theta$ changes", RED),
                                        (r"both: shift in time ($L$ has no $t$)", r"energy conserved", GOLD))]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        self.say("And the pendulum? Turning the angle is not a symmetry: gravity, through cos theta, picks out the "
                 "vertical, and indeed the angular velocity is not conserved. But for both systems, shifting time "
                 "is a symmetry, and that one gives the energy. Symmetries and conservation laws are two faces of "
                 "the same coin.", LaggedStart(*[FadeIn(r) for r in tbl], lag_ratio=0.5), run_time=3)
        self.play(FadeOut(tbl), run_time=0.6)
