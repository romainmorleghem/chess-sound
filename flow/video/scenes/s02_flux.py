"""s02 · Flux on the links: unit steps, knight's two L-paths, net flux J; real mean flux."""
from fc import (Narrated, Board, links, edge_arrows, DATA, np, FG, MUTED, BAND, GOLD, UP, DOWN, LEFT, RIGHT)
from manim import FadeIn, FadeOut, Create, Write, Text, MathTex, VGroup, Line, Arrow, Dot, Indicate
from common.style import GLYPH


def glyph(p, size=34):
    t = Text(GLYPH[p], font="DejaVu Sans", font_size=size, color="#F4F1EA")
    return t.set_stroke("#14161A", 0.8, background=True)


def step(board, a, b, color=GOLD, opacity=1.0, width=6):
    return Arrow(board.pos(a), board.pos(b), buff=0.08, color=color, stroke_width=width, stroke_opacity=opacity,
                 max_tip_length_to_length_ratio=0.3)


class Flux(Narrated):
    def construct(self):
        self.chapter("2 · Flux")
        b = Board(0.6, labels=True).shift(2.6 * LEFT)
        ln = links(b, 0.35)
        self.say("Next, how pieces move. Think of the board as a network: each square is tied to its eight neighbours.",
                 FadeIn(b), Create(ln))
        r = glyph("R").move_to(b.pos("a1"))
        st = VGroup(step(b, "a1", "a2"), step(b, "a2", "a3"), step(b, "a3", "a4"))
        self.say("A rook going from a1 to a4 crosses three links, one step at a time.", FadeIn(r), Create(st), r.animate.move_to(b.pos("a4")))
        n = glyph("N").move_to(b.pos("g1"))
        p1 = VGroup(step(b, "g1", "g2", opacity=0.55), step(b, "g2", "g3", opacity=0.55), step(b, "g3", "f3", opacity=0.55))
        p2 = VGroup(step(b, "g1", "f1", opacity=0.55), step(b, "f1", "f2", opacity=0.55), step(b, "f2", "f3", opacity=0.55))
        half = Text("½ + ½", font_size=26, color=GOLD).next_to(b.pos("h2"), RIGHT, buff=0.5)
        self.say("A knight jumps, so its path is not unique. We split it: half along each of the two L-shaped routes.",
                 FadeIn(n), Create(p1), Create(p2), FadeIn(half), n.animate.move_to(b.pos("f3")))
        eq = MathTex(r"J(x \to y) = \#\text{steps } x \to y \;-\; \#\text{steps } y \to x", font_size=36).shift(3.4 * RIGHT + 1.5 * UP)
        eq.scale_to_fit_width(6.2)
        self.say("Count the steps across every link, in all games, and subtract the steps going backwards: "
                 "that's the net flux J on the link.", Write(eq))
        self.play(FadeOut(VGroup(r, st, n, p1, p2, half)), run_time=0.5)
        ea = edge_arrows(b, DATA["J_2400_1"], color=GOLD)
        cap = Text("masters, half-moves 10 to 30", font_size=22, color=MUTED).next_to(b, DOWN, buff=0.5)
        self.say("Here is the real thing for masters, in the development phase: a current of pieces climbing from "
                 "their own camp towards the centre.", FadeIn(ea), FadeIn(cap))
        self.say("Everything is counted in whole numbers, so nothing is approximated.")
        self.play(FadeOut(VGroup(b, ln, ea, cap, eq)), run_time=0.6)
