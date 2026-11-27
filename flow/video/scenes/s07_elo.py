"""s07 · The main result: rotational fraction vs Elo (endgame), CI band, random control, robustness."""
from fc import Narrated, DATA, np, FG, MUTED, GOLD, RED, UP, DOWN, LEFT, RIGHT, ORIGIN
from manim import (FadeIn, FadeOut, Write, Create, Text, Tex, VGroup, Axes, Polygon, Dot, DashedVMobject,
                   LaggedStart)


class Elo(Narrated):
    def construct(self):
        self.chapter("7 · Beginners vs masters")
        c, lo, hi, ctrl = DATA["trend_rot_3"]
        x = DATA["elos"] + 100
        ax = Axes(x_range=[800, 2600, 400], y_range=[0.3, 0.6, 0.1], x_length=8.5, y_length=4.6,
                  axis_config=dict(color=MUTED, include_numbers=True, font_size=22),
                  tips=False).shift(0.9 * LEFT + 0.3 * DOWN)
        xl = Text("Elo", font_size=22, color=MUTED).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = Text("rotational fraction (endgame)", font_size=22, color=MUTED).next_to(ax, UP, buff=0.2)
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(x, hi)], *[ax.c2p(a, b) for a, b in zip(x[::-1], lo[::-1])],
                       stroke_width=0, fill_color=GOLD, fill_opacity=0.25)
        line = ax.plot_line_graph(x, c, line_color=GOLD, add_vertex_dots=True, vertex_dot_style=dict(color=GOLD), stroke_width=4)
        cl = DashedVMobject(ax.plot_line_graph(x, ctrl, line_color=MUTED, add_vertex_dots=False, stroke_width=3)["line_graph"])
        lc = Text("random legal moves", font_size=22, color=MUTED).next_to(ax.c2p(2500, ctrl[-1]), RIGHT, buff=0.15)
        lh = Text("Lichess games", font_size=22, color=GOLD).next_to(ax.c2p(2500, c[-1]), RIGHT, buff=0.15)
        self.say("Here is the main result. The rotational fraction of the endgame flow, from beginners to masters.",
                 Create(ax), FadeIn(xl), FadeIn(yl))
        self.say(f"Beginners: {c[0]:.2f}. Masters: {c[-1]:.2f}. It falls steadily with skill. The golden band is the "
                 "95 percent confidence interval, from two hundred resamplings of the games.",
                 FadeIn(band), Create(line), FadeIn(lh), run_time=2.5)
        self.say(f"And a player making random legal moves sits at {ctrl.mean():.2f}, flat. So it's not the rules: "
                 "it's the players.", Create(cl), FadeIn(lc))
        chk = VGroup(*[Tex(t, font_size=26, color=FG) for t in (
            r"\textbullet\ same opening mix at every level",
            r"\textbullet\ noise bias removed (two independent halves)",
            r"\textbullet\ fixed windows of half-moves",
            r"\textbullet\ board seen from either side")]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        chk.move_to(ORIGIN)
        self.play(FadeOut(VGroup(ax, xl, yl, band, line, cl, lc, lh)), run_time=0.5)
        self.say("And it survives every check we threw at it: the same openings at every level, statistical noise "
                 "removed, fixed windows of moves, and both ways of looking at the board.",
                 LaggedStart(*[FadeIn(t) for t in chk], lag_ratio=0.4), run_time=2.5)
        self.play(FadeOut(chk), run_time=0.6)
        msg = Tex(r"Masters are not less agitated.\\ They are more \textbf{directed}.", font_size=54, color=GOLD)
        self.say("In fluid language: the masters' flow is closer to a potential flow, running down a slope. "
                 "Masters are not less agitated. They are more directed.", Write(msg))
        self.play(FadeOut(msg), run_time=0.6)
