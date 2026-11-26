"""s11 · Recap and ending."""
from _common import Narrated, Board, modes, strike, glyph, np, FG, MUTED, BAND, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Tex, VGroup, LaggedStart, Write


class Outro(Narrated):
    def construct(self):
        self.chapter("Recap")
        items = VGroup(
            Tex(r"a piece $\to$ a net of rubber bands on 64 beads", font_size=34),
            Tex(r"a net $\to$ its Laplacian $L = D - A$", font_size=34),
            Tex(r"modes $L v = \lambda v$ $\to$ notes $f = 500\sqrt{\lambda}$ Hz", font_size=34),
            Tex(r"rook: a tritone \quad bishop: a doubled instrument \quad knight: a checkerboard on top", font_size=30, color=MUTED),
            Tex(r"a move $\to$ a strike \quad a game $\to$ a melody", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        self.say("Let's recap. A chess piece is a net of rubber bands. The net has a Laplacian. Its modes are "
                 "notes. The rook plays a tritone, the bishop is a doubled instrument, and the knight's highest "
                 "mode is the chessboard itself. A move is a strike, and a game becomes a melody.",
                 LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.5), run_time=6.0)
        self.play(FadeOut(items), run_time=0.6)
        w, V, lab = modes("N")
        b = Board(0.6).paint(V[:, 1])
        self.say("So, can you hear the shape of a chess piece? Yes. Listen.", FadeIn(b))
        self.add_sound(__import__("_common").snd("N_d4"))
        self.play(b.vibrate(V[:, 1], cycles=3), run_time=2.4)
        end = Tex("The Sound of Chess Pieces", font_size=60, color=FG)
        self.play(FadeOut(b), FadeIn(end), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(end), run_time=1.0)
