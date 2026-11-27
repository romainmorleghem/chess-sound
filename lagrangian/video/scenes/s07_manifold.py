"""s07 · Configuration space: M = R² (free fall), M = S¹ (pendulum); smooth manifold, charts; system (M, L)."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI, ball, ceiling
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, Circle, Arc, NumberPlane, NumberLine, LaggedStart,
                   SurroundingRectangle, ValueTracker, always_redraw, linear, DashedLine, Brace)


class Manifold(Narrated):
    def construct(self):
        self.chapter("7 · The space of configurations")
        self.say("Now let's build the mathematics properly, step by step, so that every object has a precise meaning. "
                 "Everything starts with one question: what are all the possible positions of the system?")
        # chute libre : M = R²
        pl = NumberPlane(x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=5.4, y_length=3.6,
                         background_line_style=dict(stroke_color=BLUE, stroke_opacity=0.35)).shift(3.4 * LEFT + 0.3 * DOWN)
        b = ball().move_to(pl.c2p(1, 0.8))
        lab = MathTex(r"M = \mathbb R^2,\quad q = (x, y)", font_size=34, color=GOLD).next_to(pl, UP, buff=0.25)
        self.say("For the ball in free fall, a configuration is a point of the plane, with two coordinates x and y. "
                 "The configuration space M is R two.", Create(pl), FadeIn(b), Write(lab))
        # pendule : M = S¹
        c = 3.4 * RIGHT + 0.3 * DOWN
        R = 1.5
        circ = Circle(radius=R, color=TEAL, stroke_width=4).move_to(c)
        th = ValueTracker(0.8)
        pt = always_redraw(lambda: Dot(c + R * np.array([np.sin(th.get_value()), -np.cos(th.get_value()), 0]), color=GOLD, radius=0.12))
        rod = always_redraw(lambda: Line(c, pt.get_center(), color=MUTED, stroke_width=2))
        lab2 = MathTex(r"M = S^1,\quad q = \theta", font_size=34, color=GOLD).next_to(circ, UP, buff=0.25)
        self.say("For the pendulum, the rod has a fixed length, so the only thing that can change is the angle. "
                 "The configuration space is a circle: one dimension, but curved, and closed on itself.",
                 Create(circ), FadeIn(rod), FadeIn(pt), Write(lab2))
        self.play(th.animate.set_value(0.8 + 2 * PI), run_time=3, rate_func=linear)
        self.play(FadeOut(VGroup(pl, b, lab)), VGroup(circ, lab2).animate.shift(6.8 * LEFT), FadeOut(pt), FadeOut(rod), run_time=0.8)
        # variété, cartes
        c = circ.get_center()
        d = Tex(r"a \textbf{smooth manifold} of dimension $n$: near every point, it looks like $\mathbb R^n$", font_size=32).to_edge(UP, buff=1.0)
        self.say("Both are examples of a smooth manifold of dimension n: a space which, near every point, looks like "
                 "ordinary space R n.", Write(d))
        a1 = Arc(radius=R + 0.12, start_angle=-PI / 2 + 0.25, angle=2 * PI - 0.5, color=GOLD, stroke_width=6).move_arc_center_to(c)
        a2 = Arc(radius=R + 0.3, start_angle=PI / 2 + 0.25, angle=2 * PI - 0.5, color=PURPLE, stroke_width=6).move_arc_center_to(c)
        n1 = NumberLine(x_range=[-PI, PI, PI / 2], length=4.4, color=GOLD, include_ticks=True).shift(2.6 * RIGHT + 0.6 * UP)
        n2 = NumberLine(x_range=[0, 2 * PI, PI / 2], length=4.4, color=PURPLE, include_ticks=True).shift(2.6 * RIGHT + 1.4 * DOWN)
        l1 = MathTex(r"\theta \in (-\pi, \pi)", font_size=30, color=GOLD).next_to(n1, DOWN, buff=0.2)
        l2 = MathTex(r"\theta' \in (0, 2\pi)", font_size=30, color=PURPLE).next_to(n2, DOWN, buff=0.2)
        self.say("A chart is a way to put coordinates on a piece of it. One angle cannot cover the whole circle "
                 "without a jump, so we use two charts: an angle from minus pi to pi, and another from zero to two pi.",
                 Create(a1), Create(n1), FadeIn(l1), Create(a2), Create(n2), FadeIn(l2), run_time=3)
        tr = MathTex(r"\theta' = \theta \ \text{ or } \ \theta + 2\pi \quad\text{(smooth)}", font_size=32).to_edge(DOWN, buff=0.5)
        self.say("Where the charts overlap, going from one coordinate to the other is smooth. That's all a manifold "
                 "is: patches of R n, glued together smoothly.", Write(tr))
        self.play(FadeOut(VGroup(a1, a2, n1, n2, l1, l2, tr, d, circ, lab2)), run_time=0.6)
        sysd = VGroup(Tex(r"a \textbf{Lagrangian system} is a pair $(M, L)$", font_size=40),
                      MathTex(r"L : TM \times \mathbb R \longrightarrow \mathbb R", font_size=46, color=GOLD),
                      Tex(r"(position, velocity) $\times$ time $\longmapsto$ a number", font_size=32, color=MUTED)).arrange(DOWN, buff=0.45)
        self.say("A Lagrangian system is a pair: the manifold M, and a smooth function L. L eats a position, a "
                 "velocity and a time, and returns a number. Positions live in M. But where do velocities live? "
                 "That's the object called T M.", Write(sysd))
        self.play(FadeOut(sysd), run_time=0.6)
