"""s08 · Tangent vectors as derivations, Leibniz, basis ∂/∂q; tangent bundle TM (R²×R², cylinder); derivative f_*."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, Axes, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI, ball
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, Circle, Arc, NumberPlane, LaggedStart, VMobject,
                   ValueTracker, always_redraw, linear, interpolate_color, ReplacementTransform, SurroundingRectangle)


class Tangent(Narrated):
    def construct(self):
        self.chapter("8 · Velocities: the tangent bundle")
        c, R = 3.6 * LEFT + 0.2 * DOWN, 1.7
        ring = VGroup()
        for k in range(120):
            a0, a1 = 2 * PI * k / 120, 2 * PI * (k + 1) / 120
            h = -np.cos(a0)                                   # φ = hauteur de la masse
            ring.add(Arc(radius=R, start_angle=a0 - PI / 2, angle=a1 - a0, color=interpolate_color(BLUE, RED, (h + 1) / 2), stroke_width=9).move_arc_center_to(c))
        phi = MathTex(r"\varphi = \text{height} = -\cos\theta", font_size=30).next_to(ring, UP, buff=0.3)
        self.say("On a circle, you cannot subtract two positions to get a velocity: the difference would leave the "
                 "circle. So we define a velocity by what it does. Take any smooth function phi on M, here the height "
                 "of the pendulum's bob, shown in colour.", FadeIn(ring), Write(phi))
        th0, w = 0.7, 1.0
        ax = Axes(x_range=[-1, 1, 1], y_range=[-1.2, 1.2, 1], x_length=4.2, y_length=2.6, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.2 * RIGHT + 1.0 * UP)
        fl = MathTex(r"t \mapsto \varphi(\gamma(t))", font_size=28).next_to(ax, UP, buff=0.1)
        curve = ax.plot(lambda t: -np.cos(th0 + w * t), x_range=[-1, 1], color=FG, stroke_width=3)
        slope = w * np.sin(th0)
        tl = Line(ax.c2p(-0.6, -np.cos(th0) - 0.6 * slope), ax.c2p(0.6, -np.cos(th0) + 0.6 * slope), color=GOLD, stroke_width=4)
        t = ValueTracker(-1)
        p = always_redraw(lambda: Dot(c + R * np.array([np.sin(th0 + w * t.get_value()), -np.cos(th0 + w * t.get_value()), 0]), color=FG, radius=0.11))
        pc = always_redraw(lambda: Dot(ax.c2p(t.get_value(), -np.cos(th0 + w * t.get_value())), color=FG, radius=0.07))
        vdef = MathTex(r"v(\varphi) = \frac{d}{dt}\Big|_{t=0}\varphi(\gamma(t))", font_size=40, color=GOLD).shift(3.2 * RIGHT + 1.6 * DOWN)
        self.say("Move along a curve gamma through the point q, and watch phi change. The tangent vector v is the "
                 "rule that gives, for every function phi, its rate of change at that instant: the slope, in gold.",
                 Create(ax), FadeIn(fl), Create(curve), FadeIn(p), FadeIn(pc))
        self.play(t.animate.set_value(0), run_time=1.5, rate_func=linear)
        self.play(Create(tl), Write(vdef), run_time=1.5)
        self.play(FadeOut(VGroup(ax, fl, curve, tl, pc, p)), run_time=0.5)
        th = VGroup(Tex(r"\textbf{Theorem.} $T_qM$ = the linear maps $v : C^\infty(M)\to\mathbb R$ with", font_size=30),
                    MathTex(r"v(\varphi\psi) = v(\varphi)\,\psi(q) + \varphi(q)\,v(\psi)", font_size=38, color=GOLD),
                    Tex(r"a vector space of dimension $n$, with basis $\dfrac{\partial}{\partial q^1},\dots,\dfrac{\partial}{\partial q^n}$:"
                        r"\quad $v = \sum_i v^i \dfrac{\partial}{\partial q^i}$", font_size=30)
                    ).arrange(DOWN, buff=0.35).shift(2.6 * RIGHT + 0.3 * UP)
        th.scale_to_fit_width(7.6)
        self.play(FadeOut(vdef), run_time=0.3)
        self.say("These rules are exactly the linear maps that obey the product rule, the Leibniz rule you know "
                 "from calculus. They form the tangent space at q, a vector space of the same dimension as M. "
                 "A basis: the partial derivatives along each coordinate, and v has components v i in it.", Write(th), run_time=3)
        self.play(FadeOut(VGroup(th, phi)), run_time=0.5)
        # fibré tangent
        tang = VGroup()
        for a in np.linspace(0, 2 * PI, 13)[:-1]:
            q = c + R * np.array([np.sin(a), -np.cos(a), 0]); u = np.array([np.cos(a), np.sin(a), 0])
            tang.add(Line(q - 1.2 * u, q + 1.2 * u, color=GOLD, stroke_width=2))
        TM = VGroup(MathTex(r"TM = \bigsqcup_{q\in M} T_qM", font_size=40), MathTex(r"\pi : TM \to M,\ (q, v)\mapsto q", font_size=34),
                    Tex(r"a manifold of dimension $2n$", font_size=30, color=MUTED)).arrange(DOWN, buff=0.3).shift(3.0 * RIGHT + 1.5 * UP)
        self.say("Now gather all the tangent spaces, one for each point: that's the tangent bundle, TM. A point of TM "
                 "is a pair: a position q, and a velocity v at q. It is itself a manifold, of dimension two n, and "
                 "pi forgets the velocity.", LaggedStart(*[Create(x) for x in tang], lag_ratio=0.1), Write(TM), run_time=3)
        ax2 = Axes(x_range=[-PI, PI, PI / 2], y_range=[-3, 3, 1], x_length=5.2, y_length=2.6, tips=False,
                   axis_config=dict(color=MUTED, include_ticks=False)).shift(3.0 * RIGHT + 1.7 * DOWN)
        cyl = VGroup(*[Line(ax2.c2p(x, -3), ax2.c2p(x, 3), color=GOLD, stroke_width=2) for x in np.linspace(-PI, PI, 13)[:-1]])
        cl = VGroup(MathTex(r"\theta", font_size=28).next_to(ax2.x_axis, RIGHT), MathTex(r"v", font_size=28).next_to(ax2.y_axis, UP, buff=0.05),
                    Tex(r"pendulum: $TS^1$ = a cylinder \quad free fall: $T\mathbb R^2 = \mathbb R^2\times\mathbb R^2$", font_size=26, color=MUTED).next_to(ax2, DOWN, buff=0.2))
        self.say("For the pendulum, cut the circle open and stand the tangent lines up: T M is a cylinder, angle "
                 "across, angular velocity up. For the falling ball, T M is simply four numbers: position and velocity.",
                 ReplacementTransform(tang.copy(), cyl), Create(ax2), FadeIn(cl))
        self.play(FadeOut(VGroup(tang, TM, ax2, cyl, cl)), run_time=0.5)
        # dérivée d'une application
        fdef = VGroup(MathTex(r"f : M\to N, \qquad (T_qf)(v)(\varphi) = v(\varphi\circ f)", font_size=34),
                      MathTex(r"f_* : TM \to TN,\qquad f_*(q, v) = \big(f(q),\,(T_qf)(v)\big)", font_size=34, color=GOLD)
                      ).arrange(DOWN, buff=0.3).to_edge(UP, buff=1.0)
        self.say("Last tool: if f maps M to another manifold N, it also maps velocities. Its derivative, f star, "
                 "sends a position and a velocity to their images.", Write(fdef))
        c2 = 3.3 * RIGHT + 0.6 * DOWN
        thv = 0.6
        q = c + R * np.array([np.sin(thv), -np.cos(thv), 0])
        vq = Arrow(q, q + 1.0 * np.array([np.cos(thv), np.sin(thv), 0]), buff=0, color=TEAL, stroke_width=5)
        piv = c2 + 1.4 * UP
        bob = piv + 2.4 * np.array([np.sin(thv), -np.cos(thv), 0])
        rod = Line(piv, bob, color=FG, stroke_width=3)
        vb = Arrow(bob, bob + 1.4 * np.array([np.cos(thv), np.sin(thv), 0]), buff=0, color=TEAL, stroke_width=5)
        fmap = MathTex(r"f(\theta) = (\ell\sin\theta,\ -\ell\cos\theta)", font_size=30).next_to(c2 + 2.0 * UP, UP, buff=0.05)
        res = MathTex(r"f_*\Big(\dot\theta\,\tfrac{\partial}{\partial\theta}\Big) = \ell\dot\theta(\cos\theta,\ \sin\theta)"
                      r"\ \Rightarrow\ T = \tfrac12 m\,|f_*v|^2 = \tfrac12 m\ell^2\dot\theta^2", font_size=30, color=GOLD).to_edge(DOWN, buff=0.4)
        self.say("Example: the map that places the bob in the plane, from the angle. It turns an angular velocity on "
                 "the circle into the actual velocity of the bob. And its length squared gives the kinetic energy of "
                 "the pendulum: one half m l squared theta dot squared.", FadeIn(Dot(q, color=GOLD)), Create(vq), FadeIn(rod),
                 FadeIn(Dot(bob, color=GOLD, radius=0.13)), Create(vb), Write(fmap), Write(res), run_time=3)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
