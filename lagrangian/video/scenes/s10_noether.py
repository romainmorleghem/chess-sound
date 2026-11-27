"""s10 · Noether: symmetry -> conservation law. Rotation -> angular momentum (Kepler's equal areas); table."""
from lc import Narrated, np, VGroup, Line, Dot, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, PURPLE, UP, DOWN, LEFT, RIGHT, ORIGIN, PI
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, VMobject, Polygon, ValueTracker, always_redraw,
                   linear, LaggedStart, SurroundingRectangle, Table)


class Noether(Narrated):
    def construct(self):
        self.chapter("10 · Noether's theorem")
        sym = VGroup(Tex(r"symmetry: a map $g : M\to M$ with $L(v) = L(g_*v)$ for all $v$", font_size=34),
                     MathTex(r"\{g_s\}\ \text{symmetries} \;\Longrightarrow\; I = \sum_i \frac{\partial L}{\partial \dot q^i}\,\frac{d g^i_s}{ds}\Big|_{s=0}\ \text{is conserved}",
                             font_size=38, color=GOLD)).arrange(DOWN, buff=0.5).to_edge(UP, buff=1.0)
        self.say("The crowning result, by Emmy Noether, in 1918. Call a transformation a symmetry if it leaves the "
                 "Lagrangian unchanged.", Write(sym[0]))
        self.say("Then every continuous family of symmetries hands you a conserved quantity, with an explicit formula.", Write(sym[1]))
        pf = VGroup(MathTex(r"0 = \frac{d}{ds}L\big(g_s(q), (g_s)_*\dot q\big)\Big|_{s=0} = \frac{dg_s}{ds}\frac{\partial L}{\partial q} + \frac{d\dot g_s}{ds}\frac{\partial L}{\partial\dot q}", font_size=32),
                    MathTex(r"= \frac{dg_s}{ds}\frac{d}{dt}\frac{\partial L}{\partial\dot q} + \frac{d}{dt}\Big(\frac{dg_s}{ds}\Big)\frac{\partial L}{\partial\dot q} = \frac{d}{dt}\Big(\frac{dg_s}{ds}\frac{\partial L}{\partial\dot q}\Big)", font_size=32)
                    ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).shift(0.9 * DOWN)
        self.say("The proof is two lines: differentiate the symmetry, use Euler-Lagrange, and recognise a total time "
                 "derivative.", Write(pf))
        self.play(FadeOut(VGroup(sym, pf)), run_time=0.5)
        # Kepler : aires égales
        e, a = 0.65, 2.4
        M = np.linspace(0, 2 * np.pi, 721)
        E_ = M.copy()
        for _ in range(40):
            E_ = M + e * np.sin(E_)
        xs, ys = a * (np.cos(E_) - e), a * np.sqrt(1 - e * e) * np.sin(E_)
        sun = 3.0 * LEFT + 0.3 * DOWN
        P = lambda i: sun + np.array([xs[i % 720], ys[i % 720], 0])
        orbit = VMobject(color=MUTED, stroke_width=2).set_points_as_corners([P(i) for i in range(721)])
        self.say("Example: the planets. Their Lagrangian is invariant under rotations around the sun. Noether's "
                 "conserved quantity is the angular momentum.", FadeIn(Dot(sun, color=GOLD, radius=0.16)), Create(orbit))
        wedges = VGroup()
        cols = [BLUE, TEAL, GREEN, GOLD, RED, PURPLE]
        for j, i0 in enumerate(range(0, 720, 120)):
            pts = [sun] + [P(i) for i in range(i0, i0 + 61, 3)]
            wedges.add(Polygon(*pts, stroke_width=0, fill_color=cols[j], fill_opacity=0.55))
        d = self.voice("Conserved angular momentum means: in equal times, the planet sweeps equal areas. Fast near "
                       "the sun, slow far away, but every coloured slice, taken over the same time, has the same area. "
                       "Kepler's second law, from a symmetry.")
        self.play(LaggedStart(*[FadeIn(w) for w in wedges], lag_ratio=0.5), run_time=max(d, 5))
        tbl = VGroup(*[VGroup(Tex(a_, font_size=30), MathTex(r"\longrightarrow", font_size=30), Tex(b_, font_size=30, color=GOLD)).arrange(RIGHT, buff=0.3)
                       for a_, b_ in (("translation in space", "momentum"), ("rotation", "angular momentum"),
                                      ("translation in time", "energy"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(3.2 * RIGHT + 0.3 * DOWN)
        self.say("The same machine gives everything: symmetry in space gives momentum, symmetry under rotation gives "
                 "angular momentum, symmetry in time gives energy. Symmetries and conservation laws are two faces "
                 "of one coin.", LaggedStart(*[FadeIn(r) for r in tbl], lag_ratio=0.4), run_time=2.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.6)
