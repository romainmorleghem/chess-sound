"""s03 · Divergence = the balance of one square; continuity equation, sources and sinks; exact check."""
from fc import Narrated, Board, DATA, np, FG, MUTED, BAND, GOLD, RED, BLUE, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Write, Create, Text, MathTex, Tex, VGroup, Arrow, Square, LaggedStart


class Divergence(Narrated):
    def construct(self):
        self.chapter("3 · Divergence")
        sq = Square(1.4, color=FG, stroke_width=3).shift(3.5 * LEFT + 0.6 * UP)
        outs = VGroup(*[Arrow(sq.get_center() + 0.75 * d, sq.get_center() + 1.75 * d, buff=0, color=RED, stroke_width=5)
                        for d in (np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0.7, 0.7, 0]))])
        ins = VGroup(*[Arrow(sq.get_center() + 1.75 * d, sq.get_center() + 0.75 * d, buff=0, color=BLUE, stroke_width=5)
                       for d in (np.array([-1, 0, 0]), np.array([0, -1, 0]))])
        dv = MathTex(r"\operatorname{div} J(x) = \text{out} - \text{in}", font_size=40).shift(2.2 * RIGHT + 1.6 * UP)
        self.say("Now the key idea of fluid mechanics: the balance of one square. Add up everything that leaves it, "
                 "subtract everything that comes in. That's the divergence.", Create(sq), FadeIn(outs), FadeIn(ins), Write(dv))
        s1 = Tex(r"div $> 0$: a \textbf{source}, the square empties", font_size=32, color=RED).next_to(dv, DOWN, buff=0.4)
        s2 = Tex(r"div $< 0$: a \textbf{sink}, the square fills up", font_size=32, color=BLUE).next_to(s1, DOWN, buff=0.2)
        self.say("Positive divergence: more leaves than arrives, the square is a source. Negative: it's a sink, "
                 "pieces pile up there.", FadeIn(s1), FadeIn(s2))
        eq = MathTex(r"\rho(x,t{+}1) - \rho(x,t) = -\operatorname{div} J + \text{sources} - \text{sinks}",
                     font_size=38, color=GOLD).shift(1.4 * DOWN)
        srcs = Tex(r"sinks: captures, games that end \quad source: promotion", font_size=28, color=MUTED).next_to(eq, DOWN, buff=0.3)
        self.say("The change of density on a square is minus its divergence, plus what is created, minus what is "
                 "destroyed. Pieces are destroyed by captures, created by promotion, and leave when a game ends. "
                 "This is the continuity equation, the bookkeeping of the fluid.", Write(eq), FadeIn(srcs))
        ok = Tex(r"checked on all 175\,194 games: error $= 0$ exactly", font_size=32, color=GOLD).next_to(srcs, DOWN, buff=0.35)
        self.say("And we checked it on every single game, in whole numbers: the error is exactly zero.", FadeIn(ok))
        self.play(FadeOut(VGroup(sq, outs, ins, dv, s1, s2, eq, srcs, ok)), run_time=0.6)
        boards = VGroup()
        names = ["0-10", "10-30", "30-60", "≥ 60"]
        for k in range(4):
            v = DATA[f"div_2400_{k}"]
            bb = Board(0.32).paint(v, kind="div")
            boards.add(VGroup(bb, Text(names[k], font_size=20, color=MUTED).next_to(bb, DOWN, buff=0.15)))
        boards.arrange(RIGHT, buff=0.45).shift(0.2 * DOWN)
        cap = Text("masters: divergence by phase of the game (red = source, blue = sink)", font_size=22, color=FG).next_to(boards, UP, buff=0.4)
        self.say("Here is the divergence of the masters' pieces, phase by phase. The home ranks are sources: pieces "
                 "leave. The centre and the enemy camp are sinks: that's where they go, and where they die.",
                 LaggedStart(*[FadeIn(x) for x in boards], lag_ratio=0.3), FadeIn(cap), run_time=2.5)
        self.play(FadeOut(VGroup(boards, cap)), run_time=0.6)
