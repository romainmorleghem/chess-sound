"""s00 · Cold open: 175,000 games averaged; the pieces melt and flow; title."""
from fc import Narrated, Board, square_arrows, DATA, np, FG, MUTED, BG, UP, DOWN, LEFT, RIGHT, linear
from manim import FadeIn, FadeOut, Write, Tex, Text, Rectangle, UpdateFromAlphaFunc, config, VGroup


class ColdOpen(Narrated):
    def construct(self):
        rho = DATA["rho_2400"]
        b = Board(0.62).paint(rho[0], vmax=rho.max())
        t_lab = Text("half-move 0", font_size=26, color=MUTED).next_to(b, DOWN, buff=0.3)
        self.play(FadeIn(b), FadeIn(t_lab), run_time=1.0)
        d = self.voice("Take a hundred and seventy-five thousand games of blitz chess, and stack them on top of each other.")

        def upd(m, a):
            t = int(a * 80)
            m.paint(rho[t], vmax=rho.max())
            t_lab.become(Text(f"half-move {t}", font_size=26, color=MUTED).next_to(b, DOWN, buff=0.3))
        self.play(UpdateFromAlphaFunc(b, upd, rate_func=linear), run_time=d + 2.5)
        self.say("On average, the pieces don't jump. They melt out of their camp, and spread, like a liquid.")
        arr = square_arrows(b, DATA["D_2400_1"])
        self.say("And this liquid flows: here is its mean current.", FadeIn(arr))
        self.say("So let's treat the chessboard as a fluid, with the real tools of fluid mechanics: density, flux, "
                 "divergence, whirlpools. And ask: do masters and beginners flow differently?")
        veil = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, stroke_width=0,
                         fill_color=BG, fill_opacity=0.82)
        title = Tex("The Chessboard as a Fluid", font_size=84, color=FG)
        sub = Tex("slopes and whirlpools, from beginners to masters", font_size=38, color=MUTED).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(veil), run_time=0.8)
        self.play(Write(title), FadeIn(sub, shift=0.2 * UP), run_time=2.0)
        self.wait(1.5)
        self.play(FadeOut(VGroup(veil, title, sub, b, arr, t_lab)), run_time=1.0)
