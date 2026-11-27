"""s08 · The mathematical formalism: configuration manifold, tangent bundle (circle -> phase cylinder), paths,
variations, critical points; the dot is not a derivative."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, Circle, LaggedStart, ReplacementTransform,
                   VMobject, Rectangle, SurroundingRectangle, ValueTracker, always_redraw, linear, DashedLine)


class Formalism(Narrated):
    def construct(self):
        self.chapter("8 · The mathematical picture")
        d1 = Tex(r"a \textbf{system} $(M, L)$: \quad $M$ a smooth manifold (configurations), \quad $L : TM\times\mathbb R \to \mathbb R$",
                 font_size=32).to_edge(UP, buff=1.0)
        self.say("Now let's make it precise. A system is a pair: a space M of all possible configurations, and a "
                 "Lagrangian L, a function of position, velocity and time.", Write(d1))
        R = 1.8
        c = 3.5 * LEFT + 0.6 * DOWN
        circ = Circle(radius=R, color=TEAL, stroke_width=4).move_to(c)
        M = MathTex("M = S^1", font_size=34, color=TEAL).next_to(circ, DOWN, buff=0.2)
        self.say("For the pendulum, a configuration is just an angle: M is a circle.", Create(circ), FadeIn(M))
        tang = VGroup()
        for a in np.linspace(0, 2 * np.pi, 13)[:-1]:
            p = c + R * np.array([np.cos(a), np.sin(a), 0])
            t = np.array([-np.sin(a), np.cos(a), 0])
            tang.add(Line(p - 1.3 * t, p + 1.3 * t, color=GOLD, stroke_width=2, stroke_opacity=0.8))
        TMt = MathTex(r"TM", font_size=40, color=GOLD).next_to(circ, UP, buff=1.0)
        self.say("At each point, the possible velocities form a line tangent to the circle. Gather all these lines: "
                 "that's the tangent bundle, TM. Its points are pairs: a position and a velocity.",
                 LaggedStart(*[Create(t) for t in tang], lag_ratio=0.1), FadeIn(TMt), run_time=2.5)
        ax = Axes(x_range=[-PI, PI, PI / 2], y_range=[-3, 3, 1], x_length=5.6, y_length=3.6, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.3 * RIGHT + 0.6 * DOWN)
        lab = VGroup(MathTex(r"q = \theta", font_size=30, color=TEAL).next_to(ax.x_axis, DOWN, buff=0.15),
                     MathTex(r"\dot q", font_size=30, color=GOLD).next_to(ax.y_axis, UP, buff=0.1))
        lines = VGroup(*[Line(ax.c2p(x, -3), ax.c2p(x, 3), color=GOLD, stroke_width=2, stroke_opacity=0.8) for x in np.linspace(-PI, PI, 13)[:-1]])
        self.say("Cut the circle open and stand the tangent lines upright: TM becomes a cylinder, the space of "
                 "states, with the angle across and the velocity up. It has twice the dimension of M.",
                 ReplacementTransform(tang.copy(), lines), Create(ax), FadeIn(lab))
        warn = VGroup(MathTex(r"(q^1,\dots,q^n,\ \dot q^1,\dots,\dot q^n)", font_size=34),
                      Tex(r"here the dot is \textbf{not} a derivative: $\dot q$ is an independent coordinate", font_size=28, color=RED)
                      ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        self.say("A subtle point from the notes. On TM we use coordinates q and q dot. But here, q dot is not a "
                 "derivative: it is just a second, independent coordinate.", Write(warn))
        self.play(FadeOut(VGroup(d1, circ, M, tang, TMt, ax, lab, lines, warn)), run_time=0.6)
        # chemins, variations, point critique
        a2 = Axes(x_range=[0, 1, 1], y_range=[-1, 1.6, 1], x_length=6, y_length=3.4, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.0 * LEFT + 0.4 * DOWN)
        base = lambda t: 1.2 * np.sin(np.pi * t) * 0.8
        fam = VGroup(*[a2.plot(lambda t, e=e: base(t) + e * np.sin(2 * np.pi * t) * np.sin(np.pi * t), x_range=[0, 1],
                               color=GOLD if e == 0 else MUTED, stroke_width=4 if e == 0 else 2) for e in np.linspace(-0.6, 0.6, 7)])
        ends = VGroup(Dot(a2.c2p(0, 0), color=FG), Dot(a2.c2p(1, 0), color=FG),
                      MathTex("q_0, t_0", font_size=26).next_to(a2.c2p(0, 0), DOWN), MathTex("q_1, t_1", font_size=26).next_to(a2.c2p(1, 0), DOWN))
        txt = VGroup(MathTex(r"\mathcal P(M) = \{\gamma : [t_0,t_1]\to M,\ \gamma(t_0)=q_0,\ \gamma(t_1)=q_1\}", font_size=30),
                     Tex(r"infinite-dimensional!", font_size=26, color=RED),
                     MathTex(r"S(\gamma) = \int_{t_0}^{t_1} L\big(\gamma'(t), t\big)\,dt, \qquad \gamma'(t) = (q(t), \dot q(t))", font_size=30),
                     MathTex(r"\text{physical} \iff \frac{d}{d\varepsilon}\, S(\gamma_\varepsilon)\Big|_{\varepsilon=0} = 0", font_size=34, color=GOLD)
                     ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(3.3 * RIGHT + 0.3 * DOWN)
        txt.scale_to_fit_width(6.6)
        self.say("Next, the space of all paths with fixed endpoints. A whole function per point: this space is "
                 "infinite-dimensional, which is why the subject needs care.", Create(a2), FadeIn(ends), Write(txt[0]), FadeIn(txt[1]))
        self.say("Along a path, the velocity is a point of TM, and the action integrates L over it. Only on a path "
                 "does q dot become the actual derivative of q.", Write(txt[2]))
        self.say("A variation is a smooth family of paths through our path, all sharing its ends. The physical path "
                 "is a critical point of the action: along every variation, the derivative of S vanishes. "
                 "In standard coordinates, this is exactly Euler-Lagrange.", LaggedStart(*[Create(f) for f in fam], lag_ratio=0.15), Write(txt[3]), run_time=2.5)
        self.play(FadeOut(VGroup(a2, fam, ends, txt)), run_time=0.6)
