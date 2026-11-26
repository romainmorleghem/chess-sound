"""s09 · Openings and famous games as melodies, with the board playing the moves in sync."""
from _common import Narrated, GameBoard, snd, FG, MUTED, BAND, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Text, VGroup, Tex
from melody import san_list
from games import OPENINGS, GAMES


class Melodies(Narrated):
    def game(self, key, sans, step, title, sub, intro):
        gb = GameBoard(0.68).shift(2.6 * LEFT)
        t = VGroup(Text(title, font_size=34, color=FG), Text(sub, font_size=24, color=MUTED, line_spacing=1.1)
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        t.next_to(gb, RIGHT, buff=0.7).align_to(gb, UP).shift(0.3 * DOWN)
        self.play(FadeIn(gb), FadeIn(t), run_time=0.6)
        self.say(intro)
        anim, T, lead = gb.play(sans, step)
        self.add_sound(snd(f"mel_{key}"), time_offset=lead)
        self.play(anim, run_time=T + 1.5)
        self.wait(0.8)
        self.play(FadeOut(gb), FadeOut(t), run_time=0.6)

    def construct(self):
        self.chapter("9 · Games as melodies")
        self.game("italienne", san_list(OPENINGS["italienne"][1]), 0.5, "Italian Game",
                  "1.e4 e5 2.Nf3 Nc6 3.Bc4", "Let's start with an opening: the Italian game. Listen, and watch.")
        self.game("gambit_evans", san_list(OPENINGS["gambit_evans"][1]), 0.5, "Evans Gambit",
                  "... 3...Bc5 4.b4!", "The Evans gambit: the same start, then White throws a pawn at the bishop.")
        g = GAMES["opera"]
        self.game("opera", san_list(g["moves"]), 0.34, "The Opera Game",
                  "Morphy vs Duke of Brunswick\n& Count Isouard, Paris 1858",
                  "Now a whole game. Paris, 1858, in a box at the opera: Paul Morphy against a duke and a count. "
                  "Seventeen moves, two sacrifices, and checkmate.")
        g = GAMES["immortelle"]
        self.game("immortelle", san_list(g["moves"]), 0.34, "The Immortal Game",
                  "Anderssen vs Kieseritzky\nLondon 1851",
                  "And the Immortal Game, London, 1851. Anderssen gives away a bishop, both rooks and his queen, "
                  "and mates with his last three minor pieces.")
