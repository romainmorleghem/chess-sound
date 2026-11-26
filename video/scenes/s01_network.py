"""s01 · Beads and rubber bands: each piece builds a network on the 64 squares."""
from _common import (Narrated, Board, glyph, bands, beads, adjacency, PIECE_NAME, PIECE_COLOR, BAND, FG, MUTED,
                     UP, DOWN, LEFT, RIGHT)
from manim import FadeIn, FadeOut, Create, Text, VGroup, LaggedStart, Transform


class Network(Narrated):
    def construct(self):
        self.chapter("1 · Beads and rubber bands")
        board = Board(0.72)
        bd = beads(board)
        self.say("Put a small bead on each of the sixty-four squares.", FadeIn(board), LaggedStart(*[FadeIn(b) for b in bd], lag_ratio=0.02))
        kn = glyph("N", size=50).move_to(board.pos("a1")).set_opacity(0.85)
        e1 = bands(board, "N", ["a1"], width=4)
        self.say("Now take a knight. Wherever it can jump in one move, stretch a rubber band.",
                 FadeIn(kn), Create(e1))
        self.say("From the corner, a knight has only two moves: two rubber bands.")
        e2 = bands(board, "N", ["d4"], width=4)
        self.say("From the centre, eight.", kn.animate.move_to(board.pos("d4")), FadeOut(e1), Create(e2), run_time=1.2)
        allN = bands(board, "N", width=1.8)
        n_edges = int(adjacency("N").sum() // 2)
        cnt = Text(f"{n_edges} rubber bands", font_size=30, color=BAND).to_edge(RIGHT, buff=0.8)
        self.say("Do this from every square. What you get is an object you could build: "
                 f"a net of {n_edges} rubber bands. This is the knight's instrument.",
                 FadeOut(kn), FadeOut(e2), Create(allN, lag_ratio=0.01), FadeIn(cnt), run_time=3.0)
        self.play(FadeOut(allN), FadeOut(cnt), run_time=0.6)
        rk = glyph("R", size=50).move_to(board.pos("a1")).set_opacity(0.85)
        er = bands(board, "R", ["a1"], width=3)
        self.say("A rook in the corner already has fourteen bands: it reaches every square of its row and column.",
                 FadeIn(rk), Create(er))
        self.play(FadeOut(rk), FadeOut(er), run_time=0.5)

        # the six instruments, side by side
        small = VGroup()
        for p in "RBNKQP":
            b = Board(0.2)
            net = bands(b, p, width=0.7, color=PIECE_COLOR[p], opacity=0.7)
            ne = int(adjacency(p).sum() // 2)
            lab = Text(f"{PIECE_NAME[p]}  ·  {ne}", font_size=22, color=PIECE_COLOR[p]).next_to(b, DOWN, buff=0.15)
            small.add(VGroup(b, net, lab))
        small.arrange_in_grid(2, 3, buff=(0.7, 0.5)).move_to(0.2 * DOWN)
        self.play(FadeOut(VGroup(board, bd)), run_time=0.5)
        self.say("Same sixty-four beads, six different nets: one instrument per piece. "
                 "The pawn is a special case: it only moves forward, but a rubber band has no direction. "
                 "So we made a choice: one band for every push and every capture, of white or black pawns.",
                 LaggedStart(*[FadeIn(s) for s in small], lag_ratio=0.3), run_time=3.0)
        self.play(FadeOut(small), run_time=0.8)
