"""s11 · Conservation laws; energy E = Σ q̇ ∂L/∂q̇ − L = T + V; proof; free-fall bars and pendulum phase portrait."""
from lc import (Narrated, np, VGroup, Line, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT,
                RIGHT, PI, ball, ceiling, pendulum_sol)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, ValueTracker, always_redraw, linear, VMobject,
                   interpolate_color, TracedPath, Rectangle)


class Energy(Narrated):
    def construct(self):
        self.chapter("11 · Conservation of energy")
        d1 = VGroup(Tex(r"a \textbf{conservation law}: a smooth $I : TM\to\mathbb R$ with $\dfrac{d}{dt} I(\gamma'(t)) = 0$ for every physical $\gamma$", font_size=30),
                    Tex(r"the \textbf{energy}: \quad $E(q,\dot q,t) = \displaystyle\sum_i \dot q^i\,\frac{\partial L}{\partial\dot q^i} - L$", font_size=34, color=GOLD)
                    ).arrange(DOWN, buff=0.4).to_edge(UP, buff=1.0)
        self.say("A conservation law is a function on T M that stays constant along every physical motion. The first "
                 "one is built from L itself: the energy, q dot times the derivative of L with respect to q dot, minus L.", Write(d1))
        chk = VGroup(MathTex(r"L = \tfrac12 m v^2 - V \ \Rightarrow\ E = v\cdot mv - \tfrac12 mv^2 + V = T + V", font_size=36),
                     MathTex(r"\frac{dE}{dt} = \ddot q\,\frac{\partial L}{\partial\dot q} + \dot q\,\frac{d}{dt}\frac{\partial L}{\partial\dot q} - \frac{\partial L}{\partial q}\dot q - \frac{\partial L}{\partial\dot q}\ddot q = 0", font_size=34)
                     ).arrange(DOWN, buff=0.45).shift(0.6 * DOWN)
        self.say("With L equals T minus V, it gives T plus V: the usual energy.", Write(chk[0]))
        self.say("And if L does not depend explicitly on time, an isolated system, differentiate along a motion and "
                 "use Euler-Lagrange: every term cancels. The energy is conserved.", Write(chk[1]))
        self.play(FadeOut(VGroup(d1, chk)), run_time=0.5)
        # chute libre : T et V s'échangent
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=6, y_length=3.2, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(2.6 * LEFT + 0.3 * DOWN)
        vx, vy, g = 3.4, 6.2, 9.81
        tt = ValueTracker(0)
        Tf = 2 * vy / g
        pos = lambda t: ax.c2p(vx * t, vy * t - 0.5 * g * t * t)
        b = always_redraw(lambda: ball().move_to(pos(tt.get_value())))
        tr = TracedPath(b.get_center, stroke_color=GOLD, stroke_width=3)
        E0 = 0.5 * (vx ** 2 + vy ** 2)
        base = 3.6 * RIGHT + 2.0 * DOWN
        def bars():
            t = tt.get_value()
            Tk = 0.5 * (vx ** 2 + (vy - g * t) ** 2); V = g * (vy * t - 0.5 * g * t * t)
            h = lambda x: max(4.0 * x / E0, 0.01)
            r1 = Rectangle(width=0.8, height=h(Tk), stroke_width=0, fill_color=TEAL, fill_opacity=0.9).move_to(base + LEFT * 1.1, aligned_edge=DOWN)
            r2 = Rectangle(width=0.8, height=h(V), stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to(base, aligned_edge=DOWN)
            r3 = Rectangle(width=0.8, height=h(Tk + V), stroke_width=0, fill_color=GOLD, fill_opacity=0.9).move_to(base + RIGHT * 1.1, aligned_edge=DOWN)
            return VGroup(r1, r2, r3)
        br = always_redraw(bars)
        bl = VGroup(*[MathTex(s, font_size=30, color=c).move_to(base + o + 0.3 * DOWN) for s, c, o in
                      (("T", TEAL, LEFT * 1.1), ("V", RED, 0 * RIGHT), ("E", GOLD, RIGHT * 1.1))])
        self.add(tr, b)
        self.play(Create(ax), FadeIn(br), FadeIn(bl), run_time=0.8)
        d = self.voice("Watch the falling ball. Kinetic energy turns into potential energy and back, but their sum, "
                       "in gold, never moves.")
        self.play(tt.animate.set_value(Tf), run_time=max(d, 4), rate_func=linear)
        self.play(FadeOut(VGroup(ax, b, tr, br, bl)), run_time=0.5)
        # pendule : portrait de phase sur TM
        ax2 = Axes(x_range=[-PI, PI, PI / 2], y_range=[-7, 7, 2], x_length=6.6, y_length=4.8, tips=False,
                   axis_config=dict(color=MUTED, include_ticks=False)).shift(2.6 * RIGHT + 0.3 * DOWN)
        lab = VGroup(MathTex(r"\theta", font_size=30).next_to(ax2.x_axis, RIGHT), MathTex(r"\dot\theta", font_size=30).next_to(ax2.y_axis, UP))
        ttl = Tex(r"$TS^1$: the pendulum's states, \ $E = \tfrac12 m\ell^2\dot\theta^2 - mg\ell\cos\theta$", font_size=28).next_to(ax2, UP, buff=0.15)
        curves = VGroup()
        for E in np.linspace(-0.9, 2.2, 13):
            col = interpolate_color(BLUE, RED, (E + 1) / 3.2)
            x = np.linspace(-PI, PI, 400)
            v2 = 2 * g * (E + np.cos(x))
            for sgn in (1, -1):
                ok = v2 >= 0
                if ok.sum() < 3:
                    continue
                curves.add(VMobject(color=col, stroke_width=2.5).set_points_smoothly([ax2.c2p(xx, sgn * np.sqrt(vv)) for xx, vv in zip(x[ok], v2[ok])]))
        self.say("For the pendulum, draw its whole space of states, the cylinder T M, cut open. Each curve is one "
                 "value of the energy: closed loops for swinging back and forth, waves for spinning over the top.",
                 Create(ax2), FadeIn(lab), FadeIn(ttl), Create(curves, lag_ratio=0.05), run_time=3)
        piv = 2.0 * UP + 4.4 * LEFT
        l = 2.2
        ts, th, om = pendulum_sol(2.2, g, 1.0, 6)
        k = ValueTracker(0)
        bob = lambda: piv + l * np.array([np.sin(th[int(k.get_value())]), -np.cos(th[int(k.get_value())]), 0])
        rod = always_redraw(lambda: Line(piv, bob(), color=FG, stroke_width=3))
        bb = always_redraw(lambda: ball(GOLD, 0.14).move_to(bob()))
        st = always_redraw(lambda: Dot(ax2.c2p(th[int(k.get_value())], om[int(k.get_value())]), color=GOLD, radius=0.1))
        trc = TracedPath(st.get_center, stroke_color=GOLD, stroke_width=4)
        self.add(ceiling(1.8, piv), rod, bb, trc, st)
        d = self.voice("As the pendulum swings, its state, the point gamma prime of t, runs around one loop and never "
                       "leaves it. Conservation of energy, drawn.")
        self.play(k.animate.set_value(len(th) - 1), run_time=max(d, 6), rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
