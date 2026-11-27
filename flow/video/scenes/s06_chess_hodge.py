"""s06 · Chess decomposed (masters, endgame): slope map, whirlpools, fractions; per piece."""
from fc import Narrated, Board, edge_arrows, square_arrows, edge_vectors, DATA, np, FG, MUTED, GOLD, RED, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Write, Text, Tex, VGroup, LaggedStart, Rectangle
from common.style import GLYPH


class ChessHodge(Narrated):
    def construct(self):
        self.chapter("6 · Chess, decomposed")
        k = 3
        phi, g, c = DATA[f"phi_2400_{k}"], DATA[f"g_2400_{k}"], DATA[f"c_2400_{k}"]
        b1 = Board(0.5).paint(phi - phi.min()).shift(3.4 * LEFT + 0.2 * DOWN)
        b2 = Board(0.5).shift(3.4 * RIGHT + 0.2 * DOWN)
        a1 = square_arrows(b1, edge_vectors(g), color="#14161A")
        a2 = square_arrows(b2, edge_vectors(c), color=RED)
        t1 = Text("slope: from your camp to theirs", font_size=22, color=GOLD).next_to(b1, UP, buff=0.2)
        t2 = Text("whirlpools", font_size=22, color=RED).next_to(b2, UP, buff=0.2)
        self.say("Now the real data: masters, in the endgame, after move thirty. Hodge splits their flow. "
                 "The slope part is simple: an altitude that falls from your own camp to the enemy camp, "
                 "and the pieces run down it.", FadeIn(b1), FadeIn(a1), FadeIn(t1))
        fr = 1 - 0.344
        self.say("The rest is whirlpools: pieces that go and come back by different routes, mostly near the home ranks.",
                 FadeIn(b2), FadeIn(a2), FadeIn(t2))
        self.play(FadeOut(VGroup(b1, b2, a1, a2, t1, t2)), run_time=0.5)
        names = ["pawn", "knight", "bishop", "rook", "queen", "king"]
        keep = [0, 3, 5]
        rows = VGroup()
        for idx in keep:
            v8, v24 = DATA["species_rot_800"][idx], DATA["species_rot_2400"][idx]
            g_ = Text(GLYPH["PNBRQK"[idx]], font="DejaVu Sans", font_size=40, color=FG)
            bar8 = Rectangle(width=6 * v8, height=0.32, stroke_width=0, fill_color=MUTED, fill_opacity=0.9)
            bar24 = Rectangle(width=6 * v24, height=0.32, stroke_width=0, fill_color=RED, fill_opacity=0.9)
            bars = VGroup(VGroup(bar8, Text(f"{v8:.2f}", font_size=20, color=FG).next_to(bar8, RIGHT, buff=0.1)),
                          VGroup(bar24, Text(f"{v24:.2f}", font_size=20, color=FG).next_to(bar24, RIGHT, buff=0.1))
                          ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            rows.add(VGroup(g_, Text(names[idx], font_size=24, color=FG), bars).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT).shift(0.3 * DOWN)
        leg = Tex(r"rotational fraction, endgame \quad grey: 800-1000 Elo \quad red: 2400-2600", font_size=28, color=MUTED).next_to(rows, UP, buff=0.5)
        self.say("Who makes the whirlpools? Look piece by piece. The king is almost a pure slope: in the endgame it "
                 "marches towards a goal. Rooks are whirlpools at every level: they patrol, up and down the files.",
                 FadeIn(leg), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.5)
        self.say("And the pawns, which carry most of the flow, are less swirly with masters.")
        self.play(FadeOut(VGroup(rows, leg)), run_time=0.6)
