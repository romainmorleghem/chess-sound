"""s08 · Two more fingerprints: where captures happen (entropy), rushing the enemy king (convergence)."""
from fc import Narrated, Board, DATA, np, FG, MUTED, GOLD, RED, BLUE, UP, DOWN, LEFT, RIGHT, col_div
from manim import FadeIn, FadeOut, Text, Tex, VGroup, Square, LaggedStart, DashedVMobject


def ent(p):
    p = p[p > 0]
    return -(p * np.log2(p)).sum()


class Fingerprints(Narrated):
    def construct(self):
        self.chapter("8 · Two more fingerprints")
        maps = [("800-1000 Elo", DATA["capt_800"]), ("2400-2600 Elo", DATA["capt_2400"]), ("random moves", DATA["capt_ctrl"])]
        vmax = max(m.max() for _, m in maps)
        g = VGroup()
        for t, m in maps:
            b = Board(0.36).paint(m, vmax=vmax)
            g.add(VGroup(Text(t, font_size=22, color=FG).next_to(b, UP, buff=0.15), b,
                         Text(f"{ent(m):.2f} bits", font_size=22, color=GOLD).next_to(b, DOWN, buff=0.15)))
        g.arrange(RIGHT, buff=0.6).shift(0.2 * DOWN)
        cap = Text("where captures happen (sinks), half-moves 10 to 30", font_size=24, color=MUTED).to_edge(UP, buff=1.0)
        self.say("Two more fingerprints. First, the sinks: where pieces die. Beginners capture all over the board. "
                 "Masters capture on a few classic squares, the centre and the squares of the knights and bishops. "
                 "Their entropy, a measure of spread, drops by half a bit per thousand Elo.",
                 FadeIn(cap), LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.3), run_time=2.5)
        self.play(FadeOut(VGroup(g, cap)), run_time=0.5)
        maps = [("800-1000 Elo", DATA["king_800"]), ("2400-2600 Elo", DATA["king_2400"]), ("random moves", DATA["king_ctrl"])]
        vmax = max(np.abs(m).max() for _, m in maps)
        g = VGroup()
        for t, m in maps:
            sqs = VGroup()
            for r in range(9):
                for f in range(9):
                    s = Square(0.36, stroke_width=0, fill_opacity=1, fill_color=col_div(m[r, f] / vmax))
                    s.move_to([(f - 4) * 0.36, (r - 4) * 0.36, 0]); sqs.add(s)
            k = Text("♚", font="DejaVu Sans", font_size=26, color=FG).move_to(sqs[40])
            zone = DashedVMobject(Square(5 * 0.36, color=GOLD, stroke_width=2)).move_to(sqs[40])
            z = m[2:7, 2:7].sum()
            g.add(VGroup(Text(t, font_size=22, color=FG).next_to(sqs, UP, buff=0.15), sqs, k, zone,
                         Text(f"{z:+.3f} per move", font_size=22, color=GOLD).next_to(sqs, DOWN, buff=0.15)))
        g.arrange(RIGHT, buff=0.6).shift(0.2 * DOWN)
        cap = Text("around the enemy king: arrivals minus departures (red = pile-up), half-moves 10 to 30",
                   font_size=22, color=MUTED).to_edge(UP, buff=1.0)
        self.say("Second, the enemy king. Centre the board on it and measure the pile-up of attackers. Beginners rush "
                 "the king, more than random moves would. Masters do it less than random: they build first.",
                 FadeIn(cap), LaggedStart(*[FadeIn(x) for x in g], lag_ratio=0.3), run_time=2.5)
        self.play(FadeOut(VGroup(g, cap)), run_time=0.6)
