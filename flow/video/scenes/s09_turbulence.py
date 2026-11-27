"""s09 · Laminar or turbulent? Turbulence intensity ≈ 7-10 everywhere; flat whirlpool spectrum; honest answer."""
from fc import Narrated, DATA, np, FG, MUTED, GOLD, RED, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Write, Create, Text, Tex, MathTex, VGroup, Axes, Dot, LaggedStart


class Turbulence(Narrated):
    def construct(self):
        self.chapter("9 · Laminar or turbulent?")
        t = Tex(r"laminar: the flow follows its mean \qquad turbulent: fluctuations dominate", font_size=32).to_edge(UP, buff=1.0)
        self.say("Last question, the one every fluid invites: is it laminar, smooth and orderly, or turbulent?", FadeIn(t))
        ti = lambda c: np.sqrt(1 / c ** 2 - 1)
        c8, c24, cc = DATA["coh_800"], DATA["coh_2400"], DATA["coh_ctrl"]
        eq = MathTex(r"\text{turbulence intensity} = \frac{\text{fluctuations}}{\text{mean flow}}", font_size=38).shift(1.4 * UP)
        vals = Tex(rf"beginners {ti(c8[1]):.0f} \quad masters {ti(c24[1]):.0f} \quad random {ti(cc[1]):.0f}",
                   font_size=40, color=GOLD).next_to(eq, DOWN, buff=0.4)
        self.say("Measure the turbulence intensity: how big the fluctuations are compared with the mean flow. "
                 f"About {ti(c8[1]):.0f} for beginners, {ti(c24[1]):.0f} for masters, {ti(cc[1]):.0f} for random moves. "
                 "Every chess player is wildly turbulent: individual moves are ten times bigger than the average current.",
                 Write(eq), FadeIn(vals))
        LC = DATA["LC"]
        ax = Axes(x_range=[-1, 1.2, 1], y_range=[-6, -2, 1], x_length=6, y_length=3, tips=False,
                  axis_config=dict(color=MUTED)).shift(2.0 * DOWN + 0.5 * LEFT)
        xl = Tex(r"scale: large $\leftarrow$ \quad $\rightarrow$ small", font_size=24, color=MUTED).next_to(ax, DOWN, buff=0.15)
        yl = Text("whirlpool energy", font_size=20, color=MUTED).next_to(ax, LEFT, buff=0.2).rotate(np.pi / 2)
        dots = VGroup()
        edges = np.geomspace(LC.min(), LC.max() * 1.0001, 8)
        for tag, col in (("800", MUTED), ("2400", RED), ("ctrl", FG)):
            e = DATA[f"spec_c_{tag}_1"]
            pts = []
            for a, b in zip(edges, edges[1:]):
                m = (LC >= a) & (LC < b)
                v = e[m].mean() if m.any() else np.nan
                if v > 0:
                    pts.append(ax.c2p(np.log10(np.sqrt(a * b)), np.log10(v)))
            from manim import VMobject
            ln = VMobject(color=col, stroke_width=4).set_points_as_corners(pts)
            dots.add(ln, *[Dot(p, radius=0.05, color=col) for p in pts])
        leg = VGroup(*[Text(s, font_size=20, color=c) for s, c in (("beginners", MUTED), ("masters", RED), ("random", FG))]
                     ).arrange(DOWN, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.4)
        self.say("In real turbulence, energy cascades from big whirlpools to small ones, following a power law. "
                 "Here, the whirlpool energy is flat across scales, for everyone, random moves included: no cascade.",
                 Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(dots), FadeIn(leg), run_time=2.0)
        self.play(FadeOut(VGroup(t, eq, vals, ax, xl, yl, dots, leg)), run_time=0.5)
        msg = Tex(r"No laminar / turbulent transition with skill.\\[4pt]"
                  r"The real difference: \textbf{whirlpools} vs \textbf{slopes}.", font_size=46, color=GOLD)
        self.say("So the honest answer: there is no transition from turbulent to laminar as players improve. "
                 "Skill doesn't calm the flow. It changes its shape: fewer whirlpools, more slope.", Write(msg))
        self.play(FadeOut(msg), run_time=0.6)
