"""s04 · Euler-Lagrange: general equation, momentum and force, Newton's law; pendulum in θ in two lines."""
from lc import (Narrated, np, VGroup, Line, Dot, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, UP, DOWN, LEFT, RIGHT, ORIGIN,
                ball, ceiling, pendulum_sol)
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, SurroundingRectangle, Brace, ValueTracker,
                   always_redraw, linear, TransformMatchingTex)


class EulerLagrange(Narrated):
    def construct(self):
        self.chapter("4 · The Euler-Lagrange equation")
        pr = MathTex(r"\delta S = 0", font_size=56, color=GOLD).shift(2.3 * UP + 3.3 * LEFT)
        iff = MathTex(r"\Longleftrightarrow", font_size=56).shift(2.3 * UP + 1.1 * LEFT)
        el = MathTex(r"\frac{d}{dt}\Big(", r"\frac{\partial L}{\partial \dot q}", r"\Big)", r"=", r"\frac{\partial L}{\partial q}",
                     font_size=56).shift(2.3 * UP + 2.6 * RIGHT)
        self.say("The same computation works for any Lagrangian, with any coordinates q. Stationary action is "
                 "equivalent to one equation: the Euler-Lagrange equation.", Write(pr), Write(iff), Write(el))
        b1 = Brace(el[1], DOWN, color=TEAL); t1 = Text("momentum", font_size=24, color=TEAL).next_to(b1, DOWN)
        b2 = Brace(el[4], DOWN, color=RED); t2 = Text("force", font_size=24, color=RED).next_to(b2, DOWN)
        self.say("Read it like Newton: the left side is the rate of change of a momentum, the right side is a force.",
                 FadeIn(b1), FadeIn(t1), FadeIn(b2), FadeIn(t2))
        nw = VGroup(MathTex(r"L = \tfrac12 m\dot q^2 - E_p(q)", font_size=40),
                    MathTex(r"\frac{\partial L}{\partial\dot q} = m\dot q, \qquad \frac{\partial L}{\partial q} = -\frac{dE_p}{dq} = F", font_size=40),
                    MathTex(r"\frac{d}{dt}(m\dot q) = F", font_size=46, color=GOLD)).arrange(DOWN, buff=0.4).shift(0.9 * DOWN)
        self.say("Check it with the simplest Lagrangian, one half m q dot squared minus a potential. Out comes "
                 "Newton's second law.", Write(nw[0]), Write(nw[1]), Write(nw[2]))
        self.play(FadeOut(VGroup(pr, iff, b1, t1, b2, t2, nw)), el.animate.scale(0.7).to_corner(UP + RIGHT, buff=0.5), run_time=0.8)
        # pendule en θ
        piv = 2.3 * UP + 3.6 * LEFT
        l = 3.0
        ts, th, om = pendulum_sol(1.2, 9.81, 1.0, 6)
        k = ValueTracker(0)
        bob = lambda: piv + l * np.array([np.sin(th[int(k.get_value())]), -np.cos(th[int(k.get_value())]), 0])
        rod = always_redraw(lambda: Line(piv, bob(), color=FG, stroke_width=3))
        bb = always_redraw(lambda: ball(GOLD, 0.16).move_to(bob()))
        lab = MathTex(r"\theta", font_size=34, color=GOLD).move_to(piv + 0.8 * DOWN + 0.25 * RIGHT)
        steps = VGroup(MathTex(r"L = \tfrac12 m l^2\dot\theta^2 + m g l\cos\theta", font_size=40),
                       MathTex(r"\frac{d}{dt}\big(ml^2\dot\theta\big) = -mgl\sin\theta", font_size=40),
                       MathTex(r"\ddot\theta + \frac{g}{l}\sin\theta = 0", font_size=48, color=GOLD)).arrange(DOWN, buff=0.5).shift(2.3 * RIGHT + 0.3 * DOWN)
        self.say("Now the pendulum again, but with a single coordinate, the angle theta. Kinetic energy: one half m "
                 "l squared theta dot squared. Potential: minus m g l cos theta.", FadeIn(ceiling(2.2, piv)), FadeIn(rod), FadeIn(bb),
                 FadeIn(lab), Write(steps[0]))
        d = self.voice("Apply Euler-Lagrange: two lines, and we have the pendulum's equation. No tension, no projection, "
                       "no unknown force. The rod is simply built into the choice of coordinate.")
        self.play(k.animate.set_value(len(th) - 1), Write(steps[1]), Write(steps[2]), run_time=max(d, 5), rate_func=linear)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
