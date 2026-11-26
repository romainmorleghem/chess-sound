"""s00 · Cold open: the sound of a knight, of a queen; Kac's question; title."""
from _common import Narrated, Board, glyph, strike, PAUSE, UP, DOWN, FG, MUTED, BG
from manim import FadeIn, FadeOut, Write, Tex, Rectangle, ReplacementTransform, config


class ColdOpen(Narrated):
    def construct(self):
        board = Board(0.72)
        kn = glyph("N", size=58).move_to(board.pos("d4"))
        self.play(FadeIn(board), FadeIn(kn), run_time=1.0)
        self.say("This is the sound of a knight.")
        strike(self, "N_d4", board.pos("d4"))
        q = glyph("Q", size=58).move_to(board.pos("d4"))
        self.say("And this is a queen.", ReplacementTransform(kn, q), run_time=0.8)
        strike(self, "Q_d4", board.pos("d4"))
        self.say("Not a recording, and not a synthesizer preset. These sounds were computed from the rules "
                 "of chess, and nothing else.")
        self.say("In 1966, the mathematician Mark Kac asked a famous question: can one hear the shape of a drum?")
        veil = Rectangle(width=config.frame_width + 1, height=config.frame_height + 1, stroke_width=0,
                         fill_color=BG, fill_opacity=0.8)
        title = Tex("The Sound of Chess Pieces", font_size=84, color=FG)
        sub = Tex("from eigenmodes to the Opera game", font_size=38, color=MUTED).next_to(title, DOWN, buff=0.35)
        d = self.voice("Today, a smaller question: can you hear the shape of a chess piece?")
        self.play(FadeIn(veil), run_time=1.0)
        self.play(Write(title), FadeIn(sub, shift=0.2 * UP), run_time=2.0)
        self.wait(max(0.3, d + PAUSE - 3.0) + 1.0)
        self.play(FadeOut(veil), FadeOut(title), FadeOut(sub), FadeOut(board), FadeOut(q), run_time=1.0)
