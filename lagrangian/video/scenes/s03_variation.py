"""s03 · Doing the variation by hand (free fall): δS to first order, integration by parts, ẍ = 0, ÿ = −g."""
from lc import Narrated, np, Axes, VGroup, Dot, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, UP, DOWN, LEFT, RIGHT
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, TransformMatchingTex, SurroundingRectangle,
                   ReplacementTransform, Indicate)


class Variation(Narrated):
    def construct(self):
        self.chapter("3 · Varying the path")
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=4.6, y_length=2.4, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).to_corner(UP + RIGHT, buff=0.6).shift(0.3 * DOWN)
        p = ax.plot(lambda x: 1.6 * x * (4 - x) / 4, x_range=[0, 4], color=GOLD, stroke_width=4)
        q = ax.plot(lambda x: 1.6 * x * (4 - x) / 4 + 0.35 * np.sin(np.pi * x / 2) * np.sin(np.pi * x / 4), x_range=[0, 4],
                    color=FG, stroke_width=3)
        dl = MathTex(r"x+\delta x,\ y+\delta y", font_size=28, color=FG).next_to(q, UP, buff=0.05)
        ends = VGroup(Dot(ax.c2p(0, 0), color=FG), Dot(ax.c2p(4, 0), color=FG))
        self.say("Let's prove it by hand, for the falling ball. Take the true path, and nudge it by small amounts "
                 "delta x and delta y, with both ends held fixed.", Create(ax), Create(p), FadeIn(ends), Create(q), FadeIn(dl))
        e1 = MathTex(r"\delta S", r"=", r"\int \Big[\tfrac12 m\big((\dot x+\delta\dot x)^2+(\dot y+\delta\dot y)^2\big) - mg(y+\delta y)\Big]dt",
                     r"-", r"\int\Big[\tfrac12 m(\dot x^2+\dot y^2)-mgy\Big]dt", font_size=30).to_edge(LEFT, buff=0.5).shift(0.2 * UP)
        e1.scale_to_fit_width(13)
        self.say("The change in action is the action of the nudged path minus the original one.", Write(e1))
        e2 = MathTex(r"\delta S", r"=", r"\int \Big(m\dot x\,\delta\dot x + m\dot y\,\delta\dot y - mg\,\delta y\Big)\,dt", font_size=40).move_to(e1)
        self.say("Expand, and keep only first-order terms: the squares of the small nudges are negligible.",
                 TransformMatchingTex(e1, e2))
        ibp = MathTex(r"\int_{t_0}^{t_1} m\dot x\,\delta\dot x\,dt = \Big[m\dot x\,\delta x\Big]_{t_0}^{t_1} - \int m\ddot x\,\delta x\,dt",
                      font_size=36, color=TEAL).next_to(e2, DOWN, buff=0.5)
        zero = MathTex(r"=0", font_size=34, color=TEAL).next_to(ibp[0][13:26], DOWN, buff=0.15)
        self.say("The trick is an integration by parts: it moves the time derivative from the nudge onto the path. "
                 "The boundary term vanishes, because the ends are fixed: the nudge is zero there.", Write(ibp))
        self.play(FadeIn(zero), run_time=0.5)
        e3 = MathTex(r"\delta S", r"=", r"-m\int \Big(", r"\ddot x", r"\,\delta x + (", r"\ddot y + g", r")\,\delta y\Big)\,dt", r"= 0",
                     font_size=42).move_to(e2)
        self.play(FadeOut(VGroup(ibp, zero)), run_time=0.4)
        self.say("What remains must vanish for every possible nudge, delta x and delta y. The only way: both "
                 "brackets are zero.", TransformMatchingTex(e2, e3))
        b1, b2 = SurroundingRectangle(e3[3], color=GOLD), SurroundingRectangle(e3[5], color=GOLD)
        res = MathTex(r"\ddot x = 0, \qquad \ddot y = -g", font_size=50, color=GOLD).next_to(e3, DOWN, buff=0.7)
        self.say("And there it is: x double dot equals zero, y double dot equals minus g. Exactly Newton's equations, "
                 "without ever mentioning a force.", Create(b1), Create(b2), Write(res))
        self.play(FadeOut(VGroup(ax, p, q, dl, ends, e3, b1, b2, res)), run_time=0.6)
