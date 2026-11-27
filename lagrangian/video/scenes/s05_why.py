"""s05 · Why the Lagrangian: generality, any coordinates, concise, constraints, quantum (sum over paths, Cornu spiral)."""
from lc import Narrated, np, VGroup, Line, Arrow, Dot, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, NumberPlane, ApplyPointwiseFunction, LaggedStart,
                   VMobject, interpolate_color, ValueTracker, always_redraw, linear, Axes)


class Why(Narrated):
    def construct(self):
        self.chapter("5 · Why bother?")
        items = VGroup(*[Tex(t, font_size=34) for t in (
            r"1. it generalises to all of physics", r"2. it works in any coordinates", r"3. one function defines the system",
            r"4. constraints are easy", r"5. it is the door to quantum mechanics")]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(LEFT, buff=0.6)
        self.say("Why go to all this trouble, when Newton works? Five reasons.", LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3), run_time=2.5)
        # 1
        sm = MathTex(r"\mathcal L = \sqrt{-g}\,\Big(\tfrac{1}{16\pi G}R \;-\; \tfrac14 F_{\mu\nu}F^{\mu\nu} \;+\; \bar\psi\, i\!\not{\!D}\,\psi \;+\;\dots\Big)",
                     font_size=36, color=GOLD).to_edge(RIGHT, buff=0.4).shift(1.2 * UP)
        self.say("One: it generalises. Gravity, electromagnetism and matter all fit, schematically, into one Lagrangian. "
                 "Modern physics is written this way.", items[0].animate.set_color(GOLD), Write(sm))
        self.play(FadeOut(sm), items[0].animate.set_color(FG), run_time=0.5)
        # 2 : coordonnées quelconques
        pl = NumberPlane(x_range=[-3, 3, 0.5], y_range=[-3, 3, 0.5], x_length=5, y_length=5,
                         background_line_style=dict(stroke_color=BLUE, stroke_width=1.5, stroke_opacity=0.7)).shift(3.4 * RIGHT + 0.2 * DOWN)
        c = pl.get_center()

        def warp(p):
            x, y = (p - c)[:2] / (5 / 6)
            r, a = 0.35 * (x + 3.2), y * np.pi / 3
            return c + np.array([r * np.cos(a), r * np.sin(a), 0]) * (5 / 6) * 0.9
        self.say("Two: it works in any coordinates. Cartesian, polar, angles, anything. The equation keeps exactly the "
                 "same form; Newton's forces do not.", items[1].animate.set_color(GOLD), Create(pl))
        self.play(ApplyPointwiseFunction(warp, pl), run_time=2.5)
        self.play(FadeOut(pl), items[1].animate.set_color(FG), run_time=0.5)
        # 3, 4
        self.say("Three: a single function, L, is a complete and concise definition of the system. Four: constraints, "
                 "like a rod or a track, are easy to build in. We'll see that in a moment.",
                 items[2].animate.set_color(GOLD), items[3].animate.set_color(GOLD))
        self.play(items[2].animate.set_color(FG), items[3].animate.set_color(FG), run_time=0.4)
        # 5 : somme sur les chemins (spirale de Cornu)
        eps = np.linspace(-2.6, 2.6, 900)
        phase = 9.0 * eps ** 2                         # (S(ε) − S0)/ħ, ∝ ε² près du chemin stationnaire
        steps = np.exp(1j * phase) * (eps[1] - eps[0]) * 1.6
        pts = np.concatenate([[0], np.cumsum(steps)])
        pts = pts - (pts.max().real + pts.min().real) / 2 - 1j * (pts.imag.max() + pts.imag.min()) / 2
        pts = pts / max(np.ptp(pts.real), np.ptp(pts.imag)) * 4.6
        o = 3.3 * RIGHT + 0.5 * DOWN
        spiral = VGroup()
        for k in range(len(steps)):
            a, b = pts[k], pts[k + 1]
            col = interpolate_color(PURPLE, GOLD, np.exp(-abs(eps[k]) * 1.6))
            spiral.add(Line(o + np.array([a.real, a.imag, 0]), o + np.array([b.real, b.imag, 0]), color=col, stroke_width=3))
        tot = Arrow(spiral[0].get_start(), spiral[-1].get_end(), buff=0, color=FG, stroke_width=4)
        form = MathTex(r"\text{amplitude} = \sum_{\text{paths}} e^{\,iS/\hbar}", font_size=38).next_to(spiral, UP, buff=0.3)
        self.say("Five, and this is the deepest. In quantum mechanics, a particle explores every path at once. Each path "
                 "contributes a little arrow, turned by an angle equal to its action divided by Planck's constant.",
                 items[4].animate.set_color(GOLD), Write(form))
        d = self.voice("Add the arrows, path after path. Far from the classical path, the action changes fast, the arrows "
                       "spin and cancel out: those are the curls at the ends. Near the classical path, the action is "
                       "stationary, the arrows line up, and they make the whole sum. That is why the classical world "
                       "follows stationary action.")
        self.play(Create(spiral, lag_ratio=1), run_time=max(d - 2, 6), rate_func=linear)
        self.play(Create(tot), run_time=1.0)
        self.wait(1)
        self.play(FadeOut(VGroup(items, spiral, tot, form)), run_time=0.6)
