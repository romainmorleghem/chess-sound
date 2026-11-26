"""s07 · Can you hear the shape of a chess piece? Kac, Gordon-Webb-Wolpert, then a listening quiz."""
from _common import Narrated, glyph, strike, PIECE_NAME, PIECE_COLOR, FG, MUTED, BAND, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Text, VGroup, Tex, ReplacementTransform


class Quiz(Narrated):
    def construct(self):
        self.chapter("7 · Can you hear the shape of a piece?")
        k1 = Tex(r"Kac, 1966: can one hear the shape of a drum?", font_size=38).shift(1.5 * UP)
        k2 = Tex(r"Gordon, Webb \& Wolpert, 1992: no. Two different drums, same sound.", font_size=32,
                 color=MUTED).next_to(k1, DOWN, buff=0.4)
        k3 = Tex(r"Chess pieces: yes. Six different spectra.", font_size=38, color=BAND).next_to(k2, DOWN, buff=0.6)
        self.say("Back to Mark Kac's question. For drums, the answer turned out to be no: in 1992, three "
                 "mathematicians built two drums of different shapes that sound exactly the same.", FadeIn(k1), FadeIn(k2))
        self.say("For chess pieces, the answer is yes. The six spectra are all different, so in principle "
                 "your ear can tell them apart.", FadeIn(k3))
        self.play(FadeOut(VGroup(k1, k2, k3)), run_time=0.5)
        self.say("Let's test it. Three sounds. Each time, guess the piece.")
        for k, p in enumerate("NQK"):
            q = Text("?", font_size=140, color=FG)
            num = Text(f"sound {k+1}", font_size=28, color=MUTED).next_to(q, UP, buff=0.4)
            self.play(FadeIn(q), FadeIn(num), run_time=0.4)
            strike(self, f"quiz{k}", None, dur=2.4)
            self.wait(2.0)
            ans = VGroup(glyph(p, size=120, color=PIECE_COLOR[p]),
                         Text(PIECE_NAME[p], font_size=36, color=PIECE_COLOR[p])).arrange(DOWN)
            self.play(ReplacementTransform(q, ans), run_time=0.6)
            self.wait(1.0)
            self.play(FadeOut(ans), FadeOut(num), run_time=0.4)
        self.say("The queen is the easy one: way up high. The knight and the king are closer, "
                 "but the king goes deeper.")
