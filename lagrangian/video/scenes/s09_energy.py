"""s09 · Energy E = Σ q̇ ∂L/∂q̇ − L = Ec + Ep, conserved; pendulum phase portrait with level sets."""
from lc import (Narrated, np, VGroup, Line, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT,
                RIGHT, PI, ball, ceiling, pendulum_sol)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, ValueTracker, always_redraw, linear,
                   TransformMatchingTex, VMobject, interpolate_color, SurroundingRectangle, TracedPath)


class Energy(Narrated):
    def construct(self):
        self.chapter("9 · Conservation of energy")
        d = MathTex(r"E = \sum_i \dot q^i\,\frac{\partial L}{\partial \dot q^i} - L", font_size=46).to_edge(UP, buff=1.0)
        self.say("A conservation law is a function of the state that stays constant along every physical path. "
                 "The first one: the energy, defined from L like this.", Write(d))
        chk = VGroup(MathTex(r"L = \tfrac12 m v^2 - E_p", font_size=38),
                     MathTex(r"E = v\cdot m v - \tfrac12 m v^2 + E_p", font_size=38),
                     MathTex(r"E = E_c + E_p", font_size=46, color=GOLD)).arrange(DOWN, buff=0.35).shift(0.4 * DOWN)
        self.say("Check: with kinetic minus potential, it gives kinetic plus potential, the familiar energy.", Write(chk))
        pr = MathTex(r"\frac{dE}{dt} = \ddot q\frac{\partial L}{\partial\dot q} + \dot q\frac{d}{dt}\frac{\partial L}{\partial\dot q}"
                     r" - \frac{\partial L}{\partial q}\dot q - \frac{\partial L}{\partial\dot q}\ddot q = 0", font_size=34).to_edge(DOWN, buff=0.5)
        self.say("And if L does not depend on time, Euler-Lagrange makes every term cancel: the energy is conserved.", Write(pr))
        self.play(FadeOut(VGroup(d, chk, pr)), run_time=0.5)
        # portrait de phase
        ax = Axes(x_range=[-PI, PI, PI / 2], y_range=[-7, 7, 2], x_length=6.8, y_length=4.8, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(2.6 * RIGHT + 0.3 * DOWN)
        lab = VGroup(MathTex(r"\theta", font_size=30).next_to(ax.x_axis, RIGHT), MathTex(r"\dot\theta", font_size=30).next_to(ax.y_axis, UP))
        g = 9.81
        curves = VGroup()
        for E in np.linspace(-0.9, 2.2, 13):
            col = interpolate_color(BLUE, RED, (E + 1) / 3.2)
            x = np.linspace(-PI, PI, 400)
            v2 = 2 * g * (E + np.cos(x))
            for sgn in (1, -1):
                ok = v2 >= 0
                if ok.sum() < 3:
                    continue
                seg = [ax.c2p(xx, sgn * np.sqrt(vv)) for xx, vv in zip(x[ok], v2[ok])]
                curves.add(VMobject(color=col, stroke_width=2.5).set_points_smoothly(seg))
        self.say("Here is the whole state space of the pendulum, angle across, angular velocity up. Each coloured "
                 "curve is one value of the energy: closed loops for swinging, open waves for spinning over the top.",
                 Create(ax), FadeIn(lab), Create(curves, lag_ratio=0.05), run_time=3)
        piv = 2.0 * UP + 4.4 * LEFT
        l = 2.2
        ts, th, om = pendulum_sol(2.2, g, 1.0, 6)
        k = ValueTracker(0)
        bob = lambda: piv + l * np.array([np.sin(th[int(k.get_value())]), -np.cos(th[int(k.get_value())]), 0])
        rod = always_redraw(lambda: Line(piv, bob(), color=FG, stroke_width=3))
        bb = always_redraw(lambda: ball(GOLD, 0.14).move_to(bob()))
        st = always_redraw(lambda: Dot(ax.c2p(th[int(k.get_value())], om[int(k.get_value())]), color=GOLD, radius=0.1))
        tr = TracedPath(st.get_center, stroke_color=GOLD, stroke_width=4)
        self.add(ceiling(1.8, piv), rod, bb, tr, st)
        d = self.voice("As the pendulum swings, its state travels around one loop, and never leaves it: that is "
                       "conservation of energy, drawn.")
        self.play(k.animate.set_value(len(th) - 1), run_time=max(d, 6), rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
