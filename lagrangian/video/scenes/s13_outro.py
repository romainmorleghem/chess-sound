"""s11 · Recap."""
from lc import Narrated, VGroup, FG, MUTED, GOLD, UP, DOWN, LEFT
from manim import FadeIn, FadeOut, Tex, MathTex, LaggedStart, Write


class Outro(Narrated):
    def construct(self):
        self.chapter("Recap")
        items = VGroup(*[Tex(t, font_size=32) for t in (
            r"$L = T - V$, \quad $S = \int L\,dt$",
            r"physical paths make $S$ stationary: $\delta S = 0$",
            r"$\Longleftrightarrow$ Euler-Lagrange: $\frac{d}{dt}\frac{\partial L}{\partial\dot q} = \frac{\partial L}{\partial q}$",
            r"any coordinates, constraints for free, all of physics, the door to quantum mechanics",
            r"symmetries of $L$ $\longleftrightarrow$ conservation laws (Noether)")]).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        self.say("Let's recap. Kinetic minus potential gives the Lagrangian; summed along a path, the action. Real "
                 "motions make the action stationary, which is the Euler-Lagrange equation. It works in any coordinates, "
                 "handles constraints for free, extends to all of physics and to the quantum world. And every symmetry "
                 "of L is a conservation law.", LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.6), run_time=7)
        self.play(FadeOut(items), run_time=0.6)
        end = VGroup(Tex(r"Nature is economical.", font_size=56, color=GOLD),
                     Tex(r"Of all the paths it could take, it takes the one where the action stands still.", font_size=30, color=MUTED)).arrange(DOWN, buff=0.4)
        self.say("Of all the paths it could take, nature takes the one where the action stands still.", Write(end[0]), FadeIn(end[1]))
        self.wait(1.5)
        self.play(FadeOut(end), run_time=1)
