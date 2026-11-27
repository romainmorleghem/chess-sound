"""s10 · Standard coordinates on TM (the dot is a name), γ' = (q, dq/dt), Euler-Lagrange theorem and full proof."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, LaggedStart, SurroundingRectangle, Brace,
                   TransformMatchingTex, VMobject, Polygon)


class Theorem(Narrated):
    def construct(self):
        self.chapter("10 · The Euler-Lagrange theorem")
        sc = VGroup(Tex(r"a chart $(q^1,\dots,q^n)$ on $M$ gives coordinates on $TM$:", font_size=32),
                    MathTex(r"(q, v)\ \longmapsto\ (q^1,\dots,q^n,\ v^1,\dots,v^n), \qquad v = \sum_i v^i\,\frac{\partial}{\partial q^i}", font_size=34),
                    MathTex(r"\text{notation: } v^i =: \dot q^i \qquad\Rightarrow\qquad (q^1,\dots,q^n,\ \dot q^1,\dots,\dot q^n)", font_size=34, color=GOLD)
                    ).arrange(DOWN, buff=0.35).to_edge(UP, buff=1.0)
        self.say("To compute, we need coordinates on T M. A chart on M gives n coordinates q; a tangent vector has "
                 "n components v in the basis of partial derivatives. Together: two n coordinates on T M, the standard "
                 "coordinates.", Write(sc[0]), Write(sc[1]))
        warn = Tex(r"here $\dot q^i$ is just a \textbf{name} for $v^i$: an independent coordinate, \textbf{not} a derivative", font_size=30, color=RED).next_to(sc, DOWN, buff=0.4)
        self.say("Traditionally, we write the components with a dot: q dot. Careful: at this stage the dot is only a "
                 "name. q dot is an independent coordinate on T M, not the derivative of anything.", Write(sc[2]), FadeIn(warn))
        thm = VGroup(Tex(r"\textbf{Theorem.} along a path $\gamma(t) = (q^1(t),\dots,q^n(t))$:", font_size=32),
                     MathTex(r"\gamma'(t) = \Big(q(t),\ \frac{dq}{dt}(t)\Big) \quad\Longrightarrow\quad S(\gamma) = \int_{t_0}^{t_1} L\big(q(t), \dot q(t), t\big)\,dt", font_size=34, color=GOLD)
                     ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        self.say("Only along a path does the coordinate q dot take the value of the true derivative of q. That's what "
                 "justifies the familiar formula for the action.", Write(thm))
        self.play(FadeOut(VGroup(sc, warn, thm)), run_time=0.5)
        st = VGroup(Tex(r"\textbf{Theorem.} In standard coordinates, the physical paths of $(M, L)$ satisfy", font_size=32),
                    MathTex(r"\frac{d}{dt}\Big(\frac{\partial L}{\partial \dot q^i}\Big) = \frac{\partial L}{\partial q^i}, \qquad i = 1,\dots,n", font_size=42, color=GOLD)
                    ).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.9)
        self.say("Now the theorem, and its proof.", Write(st))
        p1 = MathTex(r"\gamma_\varepsilon(t) = q(t,\varepsilon), \qquad S(\gamma_\varepsilon) = \int_{t_0}^{t_1} L\big(q(t,\varepsilon),\ \dot q(t,\varepsilon),\ t\big)\,dt", font_size=34).next_to(st, DOWN, buff=0.45)
        self.say("Take a physical path and any variation of it. In coordinates, the varied path is q of t and epsilon.", Write(p1))
        p2 = MathTex(r"\frac{d}{d\varepsilon}S\Big|_0 = \int \Big(\frac{\partial q^i}{\partial\varepsilon}\frac{\partial L}{\partial q^i} + \frac{\partial \dot q^i}{\partial\varepsilon}\frac{\partial L}{\partial \dot q^i}\Big)dt", font_size=34).next_to(p1, DOWN, buff=0.35)
        self.say("Differentiate under the integral, with the chain rule. Sums over i are implied.", Write(p2))
        p3 = MathTex(r"\frac{\partial\dot q^i}{\partial\varepsilon}\frac{\partial L}{\partial\dot q^i} = \frac{d}{dt}\Big(\frac{\partial q^i}{\partial\varepsilon}\frac{\partial L}{\partial\dot q^i}\Big) - \frac{\partial q^i}{\partial\varepsilon}\frac{d}{dt}\frac{\partial L}{\partial\dot q^i}", font_size=32, color=TEAL).next_to(p2, DOWN, buff=0.35)
        self.say("On the path, q dot is the time derivative of q, so the two derivatives commute, and we can integrate "
                 "by parts. The total derivative integrates to a boundary term, which is zero: the ends do not move.", Write(p3))
        p4 = MathTex(r"\frac{d}{d\varepsilon}S\Big|_0 = \int_{t_0}^{t_1} \frac{\partial q^i}{\partial\varepsilon}\Big[", r"\frac{\partial L}{\partial q^i} - \frac{d}{dt}\frac{\partial L}{\partial\dot q^i}", r"\Big]dt = 0", font_size=36).next_to(p3, DOWN, buff=0.35)
        self.say("What's left must be zero, for every variation.", Write(p4))
        self.play(FadeOut(VGroup(p1, p2, p3)), p4.animate.next_to(st, DOWN, buff=0.4), run_time=0.8)
        ax = Axes(x_range=[0, 1, 1], y_range=[-1, 1.3, 1], x_length=6, y_length=2.6, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(1.9 * DOWN)
        br = ax.plot(lambda t: 0.8 * np.sin(2 * np.pi * t) * np.exp(-((t - 0.5) ** 2) / 0.2), x_range=[0, 1], color=FG, stroke_width=3)
        bump = ax.plot(lambda t: np.exp(-((t - 0.25) ** 2) / 0.003), x_range=[0.1, 0.4], color=GOLD, stroke_width=4)
        lb = VGroup(Tex(r"bracket", font_size=26, color=FG).next_to(ax.c2p(0.55, 0.7), UP), Tex(r"a variation $\partial q/\partial\varepsilon$ = a bump", font_size=26, color=GOLD).next_to(ax, LEFT, buff=0.2).shift(0.6 * UP))
        self.say("Why does that force the bracket itself to vanish? Suppose it were positive somewhere. Choose a "
                 "variation that is a tiny bump right there: the integral would be positive, not zero. Contradiction. "
                 "So the bracket is zero at every time: that's the Euler-Lagrange equation.",
                 Create(ax), Create(br), Create(bump), FadeIn(lb), run_time=3)
        box = SurroundingRectangle(p4[1], color=GOLD)
        self.play(Create(box), run_time=0.6)
        self.play(FadeOut(VGroup(ax, br, bump, lb, p4, box)), run_time=0.5)
        ex = VGroup(MathTex(r"\text{free fall: } L = \tfrac12 m(\dot x^2+\dot y^2) - mgy \ \Rightarrow\ \ddot x = 0,\ \ \ddot y = -g", font_size=34),
                    MathTex(r"\text{pendulum: } L = \tfrac12 m\ell^2\dot\theta^2 + mg\ell\cos\theta \ \Rightarrow\ \ddot\theta + \tfrac{g}{\ell}\sin\theta = 0", font_size=34)
                    ).arrange(DOWN, buff=0.5).shift(0.6 * DOWN)
        self.say("And our two examples follow in one line each: the parabola of the falling ball, and the pendulum.", Write(ex))
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
