"""s01 · Newton's way: free fall (ma = ΣF -> parabola), then the pendulum (unknown tension)."""
from lc import (Narrated, np, Axes, VGroup, Dot, Line, Arrow, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, UP, DOWN, LEFT,
                RIGHT, ORIGIN, ball, ceiling, pendulum_sol)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, TransformMatchingTex, UpdateFromAlphaFunc,
                   linear, always_redraw, ValueTracker, TracedPath, DashedLine, Arc, SurroundingRectangle)


class Newton(Narrated):
    def construct(self):
        self.chapter("1 · Newton's way")
        # chute libre
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2.2, 1], x_length=6, y_length=3.4, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).to_edge(LEFT, buff=0.6).shift(0.6 * DOWN)
        lx, ly = MathTex("x", font_size=30, color=MUTED).next_to(ax.x_axis, RIGHT), MathTex("y", font_size=30, color=MUTED).next_to(ax.y_axis, UP)
        vx, vy, g = 3.0, 5.8, 9.81
        tt = ValueTracker(0)
        pos = lambda t: ax.c2p(vx * t * 0.95, (vy * t - 0.5 * g * t * t) * 1.15)
        b = always_redraw(lambda: ball().move_to(pos(tt.get_value())))
        vel = always_redraw(lambda: Arrow(pos(tt.get_value()), pos(tt.get_value()) + 0.12 * np.array([vx, vy - g * tt.get_value(), 0]),
                                          buff=0, color=TEAL, stroke_width=4))
        grav = always_redraw(lambda: Arrow(pos(tt.get_value()), pos(tt.get_value()) + 0.7 * DOWN, buff=0, color=RED, stroke_width=4))
        trace = TracedPath(b.get_center, stroke_color=GOLD, stroke_width=3)
        eqs = VGroup(MathTex(r"m\vec a = \sum \vec F = m\vec g", font_size=40),
                     MathTex(r"\ddot x = 0, \qquad \ddot y = -g", font_size=40),
                     MathTex(r"x = v_x t, \qquad y = -\tfrac12 g t^2 + v_y t", font_size=40),
                     MathTex(r"y = -\frac{g}{2}\Big(\frac{x}{v_x}\Big)^2 + v_y \frac{x}{v_x}", font_size=40, color=GOLD)
                     ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6)
        self.say("First, the familiar way. A ball in free fall feels one force, its weight. Newton's second law: "
                 "mass times acceleration equals the sum of the forces.", Create(ax), FadeIn(lx), FadeIn(ly), Write(eqs[0]))
        self.add(trace, b, vel, grav)
        d = self.voice("So the acceleration is just g, pointing down. Integrate twice: x grows steadily, y rises and falls.")
        self.play(tt.animate.set_value(1.18), Write(eqs[1]), Write(eqs[2]), run_time=max(d, 3), rate_func=linear)
        self.say("Eliminate time, and the path is a parabola.", Write(eqs[3]))
        self.play(FadeOut(VGroup(ax, lx, ly, eqs, trace, b, vel, grav)), run_time=0.6)
        # pendule
        piv = 2.6 * UP + 3.3 * LEFT
        l = 3.2
        ts, th, om = pendulum_sol(1.0, 9.81, 1.0, 8)
        k = ValueTracker(0)
        bob = lambda: piv + l * np.array([np.sin(th[int(k.get_value())]), -np.cos(th[int(k.get_value())]), 0])
        rod = always_redraw(lambda: Line(piv, bob(), color=FG, stroke_width=3))
        bb = always_redraw(lambda: ball(GOLD, 0.16).move_to(bob()))
        P = always_redraw(lambda: Arrow(bob(), bob() + 1.1 * DOWN, buff=0, color=RED, stroke_width=4))
        Tn = always_redraw(lambda: Arrow(bob(), bob() + 0.95 * (piv - bob()) / l, buff=0, color=BLUE, stroke_width=4))
        lab = always_redraw(lambda: VGroup(MathTex(r"\vec P", font_size=30, color=RED).next_to(bob() + 1.1 * DOWN, RIGHT, buff=0.1),
                                           MathTex(r"\vec T\,?", font_size=30, color=BLUE).next_to(bob() + 0.5 * (piv - bob()) / l, LEFT, buff=0.15)))
        ce = ceiling(2.4, piv)
        self.say("Now a pendulum: a mass on a rigid rod. Two forces: the weight, and the tension of the rod.",
                 FadeIn(ce), FadeIn(rod), FadeIn(bb), FadeIn(P), FadeIn(Tn), FadeIn(lab))
        eq = VGroup(MathTex(r"m\vec a = \vec P + \vec T", font_size=38),
                    MathTex(r"\vec a = -l\dot\theta^2\,\vec e_r + l\ddot\theta\,\vec e_\theta", font_size=38),
                    MathTex(r"-ml\dot\theta^2 = -T + mg\cos\theta", font_size=38),
                    MathTex(r"ml\ddot\theta = -mg\sin\theta", font_size=38),
                    MathTex(r"\ddot\theta + \frac{g}{l}\sin\theta = 0", font_size=44, color=GOLD)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).to_edge(RIGHT, buff=0.7)
        d = self.voice("But the tension is unknown. It changes as the pendulum swings. To use Newton, we must project "
                       "everything on polar axes, and drag the tension along.")
        self.play(k.animate.set_value(len(th) - 1), Write(eq[0]), Write(eq[1]), Write(eq[2]), Write(eq[3]), run_time=max(d, 6), rate_func=linear)
        box = SurroundingRectangle(eq[2], color=BLUE, buff=0.1)
        self.say("One equation only serves to find the tension, a quantity we never asked for. The other gives the "
                 "motion. It works, but it is clumsy. Keep that in mind.", Write(eq[4]), Create(box))
        self.play(FadeOut(VGroup(ce, rod, bb, P, Tn, lab, eq, box)), run_time=0.6)
