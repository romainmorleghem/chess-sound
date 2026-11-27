"""s09 · Paths, variations, γ' ∈ TM, the action functional, the principle; numerical check on the pendulum."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI, solve_ivp
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, LaggedStart, ValueTracker, always_redraw, linear,
                   DecimalNumber)

g = 9.81
T1 = 0.9
sol = solve_ivp(lambda t, y: [y[1], -g * np.sin(y[0])], (0, T1), [1.0, 0.0], t_eval=np.linspace(0, T1, 500), rtol=1e-10, atol=1e-12)
TS, TH, OM = sol.t, sol.y[0], sol.y[1]
ETA, DETA = np.sin(np.pi * TS / T1), np.pi / T1 * np.cos(np.pi * TS / T1)


def S(e):
    th, om = TH + e * ETA, OM + e * DETA
    return np.trapezoid(0.5 * om ** 2 + g * np.cos(th), TS)


class Paths(Narrated):
    def construct(self):
        self.chapter("9 · Paths and the action")
        P = MathTex(r"\mathcal P(M) = \big\{\gamma : [t_0, t_1]\to M \ \big|\ \gamma(t_0) = q_0,\ \gamma(t_1) = q_1\big\}", font_size=36).to_edge(UP, buff=1.0)
        self.say("Next, motions. A path is a smooth map from a time interval into M. We fix where it starts and "
                 "where it ends, and call P of M the set of all such paths.", Write(P))
        inf = Tex(r"each point of $\mathcal P(M)$ is a whole function: an \textbf{infinite-dimensional} space", font_size=30, color=RED).next_to(P, DOWN, buff=0.3)
        self.say("Each point of this space is a whole function, so the space is infinite-dimensional. That's what "
                 "makes the subject subtle.", FadeIn(inf))
        self.play(FadeOut(inf), run_time=0.4)
        ax = Axes(x_range=[0, T1, T1], y_range=[-0.6, 1.4, 1], x_length=5.6, y_length=3.2, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.3 * LEFT + 0.9 * DOWN)
        al = VGroup(MathTex(r"t", font_size=28).next_to(ax.x_axis, RIGHT), MathTex(r"\theta", font_size=28).next_to(ax.y_axis, UP, buff=0.05))
        fam = VGroup(*[ax.plot_line_graph(TS, TH + e * ETA, add_vertex_dots=False, line_color=GOLD if e == 0 else MUTED,
                                          stroke_width=4 if e == 0 else 2) for e in np.linspace(-0.6, 0.6, 7)])
        var = VGroup(Tex(r"a \textbf{variation} of $\gamma$: smooth $(t,\varepsilon)\mapsto\gamma_\varepsilon(t)$", font_size=30),
                     MathTex(r"\gamma_\varepsilon(t_0) = q_0,\quad \gamma_\varepsilon(t_1) = q_1,\quad \gamma_0 = \gamma", font_size=32)
                     ).arrange(DOWN, buff=0.25).shift(3.3 * RIGHT + 1.3 * UP)
        self.say("A variation of a path gamma is a smooth family of paths gamma epsilon, all with the same ends, "
                 "which is gamma itself when epsilon is zero. Here, for the pendulum, the angle over time.",
                 Create(ax), FadeIn(al), LaggedStart(*[Create(f) for f in fam], lag_ratio=0.15), Write(var), run_time=3)
        gp = VGroup(MathTex(r"\gamma'(t) = \gamma_*\Big(t, \frac{\partial}{\partial t}\Big) \in TM", font_size=34),
                    MathTex(r"\gamma(t) = (x(t), y(t)) \ \Rightarrow\ \gamma'(t) = \big(x, y, \dot x, \dot y\big)", font_size=30, color=MUTED)
                    ).arrange(DOWN, buff=0.3).next_to(var, DOWN, buff=0.45)
        self.say("Along a path, its derivative gamma prime, at each instant, is a point of T M: where we are, and how "
                 "fast we move. For the ball: x, y, x dot, y dot. Not just the velocity, the whole state.", Write(gp))
        act = MathTex(r"S(\gamma) = \int_{t_0}^{t_1} L\big(\gamma'(t), t\big)\,dt", font_size=40, color=GOLD).next_to(gp, DOWN, buff=0.45)
        self.say("Now the action is a precise object: a function on the space of paths, which integrates L along "
                 "gamma prime.", Write(act))
        self.play(FadeOut(VGroup(P, var, gp, act)), run_time=0.5)
        pr = VGroup(Tex(r"\textbf{Principle of stationary action.} $\gamma$ is a physical motion of $(M,L)$ iff", font_size=32),
                    MathTex(r"\frac{d}{d\varepsilon}\,S(\gamma_\varepsilon)\Big|_{\varepsilon = 0} = 0 \quad\text{for every variation } \gamma_\varepsilon", font_size=36, color=GOLD)
                    ).arrange(DOWN, buff=0.3).to_edge(UP, buff=1.0)
        self.say("And here is the principle, stated precisely: a path is a physical motion exactly when it is a "
                 "critical point of the action. Along every variation, the derivative of S at epsilon zero vanishes.", Write(pr))
        a3 = Axes(x_range=[-0.6, 0.6, 0.3], y_range=[-0.05, 0.25, 0.1], x_length=4.6, y_length=3.0, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.4 * RIGHT + 1.1 * DOWN)
        S0 = S(0)
        cs = a3.plot(lambda e: S(e) - S0, x_range=[-0.6, 0.6], color=FG, stroke_width=3)
        lab = VGroup(MathTex(r"S(\gamma_\varepsilon) - S(\gamma)", font_size=28).next_to(a3, UP, buff=0.1),
                     MathTex(r"\varepsilon", font_size=28).next_to(a3.x_axis, RIGHT))
        e = ValueTracker(0.5)
        dot = always_redraw(lambda: Dot(a3.c2p(e.get_value(), S(e.get_value()) - S0), color=GOLD, radius=0.08))
        cur = always_redraw(lambda: ax.plot_line_graph(TS, TH + e.get_value() * ETA, add_vertex_dots=False, line_color=TEAL, stroke_width=4))
        self.say("Let's check it numerically on the real pendulum. Compute the action of each varied path: the curve "
                 "is flat at epsilon zero.", Create(a3), FadeIn(lab), Create(cs), FadeIn(dot), FadeIn(cur))
        self.play(e.animate.set_value(-0.5), run_time=3, rate_func=linear)
        self.play(e.animate.set_value(0), run_time=1.5)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
