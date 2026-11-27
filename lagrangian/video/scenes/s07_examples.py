"""s07 · Four Lagrangians: planets, geodesics, rigid body (tennis racket), rotating frame (Coriolis)."""
from lc import (Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN,
                LEFT, RIGHT, ORIGIN, PI, solve_ivp, ball)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, ValueTracker, always_redraw, linear, TracedPath,
                   Circle, Ellipse, Arc, VMobject, Rotate, Square)


class Examples(Narrated):
    def construct(self):
        self.chapter("7 · A gallery of Lagrangians")
        # planètes
        e, a = 0.6, 2.2
        th = np.linspace(0, 2 * np.pi, 600)
        M = np.linspace(0, 2 * np.pi, 600)                          # anomalie moyenne -> temps uniforme
        E_ = M.copy()
        for _ in range(30):
            E_ = M + e * np.sin(E_)
        xs, ys = a * (np.cos(E_) - e), a * np.sqrt(1 - e * e) * np.sin(E_)
        sun = Dot(ORIGIN, radius=0.16, color=GOLD).shift(3.2 * LEFT)
        orbit = VMobject(color=MUTED, stroke_width=2).set_points_as_corners([sun.get_center() + np.array([x, y, 0]) for x, y in zip(xs, ys)])
        k = ValueTracker(0)
        pl = always_redraw(lambda: Dot(sun.get_center() + np.array([xs[int(k.get_value()) % 600], ys[int(k.get_value()) % 600], 0]), color=BLUE, radius=0.1))
        Lp = MathTex(r"L = \tfrac12 m v^2 + \frac{\alpha}{r}", font_size=44).shift(3 * RIGHT + 1.5 * UP)
        self.say("A gallery. First, the planets: kinetic energy, plus alpha over r for gravity. Euler-Lagrange gives "
                 "Kepler's ellipses.", FadeIn(sun), Create(orbit), FadeIn(pl), Write(Lp))
        self.play(k.animate.set_value(1199), run_time=5, rate_func=linear)
        inv = Tex("invariant under rotation", font_size=30, color=GOLD).next_to(Lp, DOWN, buff=0.4)
        self.say("Notice: this Lagrangian does not change if you rotate everything around the sun. Remember that, "
                 "it will matter.", FadeIn(inv), Rotate(VGroup(orbit), angle=PI / 3, about_point=sun.get_center()))
        self.play(FadeOut(VGroup(sun, orbit, pl, Lp, inv)), run_time=0.5)
        # géodésiques
        R = 2.2
        c = 3.2 * LEFT + 0.2 * DOWN
        sph = VGroup(Circle(radius=R, color=MUTED, stroke_width=2).move_to(c))
        for lat in (-0.9, -0.45, 0, 0.45, 0.9):
            sph.add(Ellipse(width=2 * R * np.cos(lat), height=0.5 * R * np.cos(lat), color=MUTED, stroke_width=1, stroke_opacity=0.4).move_to(c + R * np.sin(lat) * UP))
        tilt = 0.9
        gc = lambda s: c + R * np.array([np.cos(s), np.sin(s) * np.sin(tilt) * 0.25 + np.sin(s) * np.cos(tilt) * 0.0 + 0.95 * np.sin(s) * np.sin(tilt), 0])
        front = VMobject(color=GOLD, stroke_width=4).set_points_smoothly([gc(s) for s in np.linspace(-np.pi / 2, np.pi / 2, 80)])
        Lg = VGroup(MathTex(r"L = \tfrac12 m\,\langle v, v\rangle = \tfrac12 m\, g_{\mu\nu}\dot x^\mu \dot x^\nu", font_size=40),
                    MathTex(r"\ddot x^\sigma + \Gamma^\sigma_{\mu\nu}\dot x^\mu\dot x^\nu = 0", font_size=44, color=GOLD)
                    ).arrange(DOWN, buff=0.5).shift(3 * RIGHT + 0.5 * UP)
        s = ValueTracker(-np.pi / 2)
        p = always_redraw(lambda: Dot(gc(s.get_value()), color=BLUE, radius=0.1))
        self.say("Second: a free particle on a curved surface. The Lagrangian is just kinetic energy, measured with "
                 "the surface's own ruler, the metric. Euler-Lagrange gives the geodesic equation: the straightest "
                 "possible lines. On a sphere, great circles.", Create(sph), Write(Lg[0]))
        self.add(p)
        self.play(Create(front), s.animate.set_value(np.pi / 2), Write(Lg[1]), run_time=4, rate_func=linear)
        self.say("Einstein's gravity is exactly this, in curved spacetime.")
        self.play(FadeOut(VGroup(sph, front, p, Lg)), run_time=0.5)
        # solide : théorème de la raquette de tennis
        I1, I2, I3 = 1.0, 2.0, 3.0
        sol = solve_ivp(lambda t, w: [(I2 - I3) / I1 * w[1] * w[2], (I3 - I1) / I2 * w[2] * w[0], (I1 - I2) / I3 * w[0] * w[1]],
                        (0, 40), [0.01, 1.0, 0.01], t_eval=np.linspace(0, 40, 2000), rtol=1e-9)
        ax = Axes(x_range=[0, 40, 10], y_range=[-1.2, 1.2, 1], x_length=7, y_length=3.2, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(2.6 * RIGHT + 1.0 * DOWN)
        curves = VGroup(*[ax.plot_line_graph(sol.t, sol.y[i], add_vertex_dots=False, line_color=c_, stroke_width=3)
                          for i, c_ in ((0, TEAL), (1, GOLD), (2, PURPLE))])
        lab = VGroup(*[MathTex(s_, font_size=28, color=c_) for s_, c_ in ((r"\Omega_1", TEAL), (r"\Omega_2", GOLD), (r"\Omega_3", PURPLE))]
                     ).arrange(RIGHT, buff=0.4).next_to(ax, UP, buff=0.1)
        Lr = VGroup(MathTex(r"L = \tfrac12\left(I_1\Omega_1^2 + I_2\Omega_2^2 + I_3\Omega_3^2\right)", font_size=38),
                    MathTex(r"I_1\dot\Omega_1 = (I_2 - I_3)\,\Omega_2\Omega_3", font_size=38, color=GOLD)).arrange(DOWN, buff=0.35).to_edge(LEFT, buff=0.5).shift(1.6 * UP)
        racket = VGroup(Square(1.0, color=FG, stroke_width=3), Line(0.5 * DOWN, 1.6 * DOWN, color=FG, stroke_width=4)).shift(4.6 * LEFT + 1.4 * DOWN)
        self.say("Third: a spinning solid. Its Lagrangian is rotational kinetic energy, and Euler-Lagrange gives "
                 "Euler's equations.", Write(Lr))
        d = self.voice("Solve them for a body spun around its middle axis, like a tennis racket tossed in the air. "
                       "The spin, in gold, keeps flipping over: the famous tennis racket effect, hidden in one line of L.")
        self.play(Create(ax), FadeIn(lab), Create(curves, lag_ratio=0), FadeIn(racket), run_time=max(d - 1, 4), rate_func=linear)
        self.play(Rotate(racket, PI, axis=RIGHT), run_time=1)
        self.play(FadeOut(VGroup(ax, curves, lab, Lr, racket)), run_time=0.5)
        # référentiel tournant : Coriolis
        Rd = 1.9
        cL, cR = 4.7 * LEFT + 0.4 * DOWN, 0.6 * LEFT + 0.4 * DOWN
        dL, dR = Circle(radius=Rd, color=MUTED).move_to(cL), Circle(radius=Rd, color=MUTED).move_to(cR)
        tt = ValueTracker(0)
        Om = 1.2
        v = np.array([0.75, 0.42, 0])
        p0 = np.array([-1.3, -0.75, 0])
        posI = lambda t: p0 + v * t
        def posR(t):
            x, y, _ = posI(t)
            c_, s_ = np.cos(-Om * t), np.sin(-Om * t)
            return np.array([c_ * x - s_ * y, s_ * x + c_ * y, 0])
        mL = always_redraw(lambda: Dot(cL + posI(tt.get_value()), color=GOLD, radius=0.1))
        mR = always_redraw(lambda: Dot(cR + posR(tt.get_value()), color=GOLD, radius=0.1))
        trL, trR = TracedPath(mL.get_center, stroke_color=GOLD, stroke_width=3), TracedPath(mR.get_center, stroke_color=RED, stroke_width=3)
        spokes = always_redraw(lambda: VGroup(*[Line(cR, cR + Rd * np.array([np.cos(a_ - 0 * tt.get_value()), np.sin(a_), 0]), color=MUTED, stroke_width=1)
                                               for a_ in np.linspace(0, 2 * np.pi, 7)[:-1]]))
        hdr = VGroup(Text("seen from above", font_size=22, color=MUTED).next_to(dL, UP, buff=0.15),
                     Text("seen from the turntable", font_size=22, color=MUTED).next_to(dR, UP, buff=0.15))
        Lc = VGroup(MathTex(r"L = \tfrac12 m\,(\dot{\vec r} + \vec\Omega\wedge\vec r)^2", font_size=34),
                    MathTex(r"m\ddot{\vec r} = -2m\,\vec\Omega\wedge\dot{\vec r} - m\,\vec\Omega\wedge(\vec\Omega\wedge\vec r)", font_size=30, color=GOLD)
                    ).arrange(DOWN, buff=0.35)
        Lc.scale_to_fit_width(4.6).to_edge(RIGHT, buff=0.3).shift(0.4 * DOWN)
        self.say("Fourth: a puck sliding on a turntable. From above, it goes in a straight line. Written in the "
                 "turning coordinates, the same free Lagrangian picks up extra terms.", Create(dL), Create(dR), FadeIn(hdr), Write(Lc[0]))
        self.add(trL, trR, mL, mR)
        d = self.voice("Euler-Lagrange hands us, without effort, the Coriolis force and the centrifugal force: "
                       "the curve you see on the right.")
        self.play(tt.animate.set_value(3.4), Write(Lc[1]), run_time=max(d, 4), rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
