"""s10 · Which game is the most melodious? Simplicity and roughness vs random games."""
import json
from _common import Narrated, ROOT, np, FG, MUTED, BAND, POS, NEG, GOOD, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Text, VGroup, Rectangle, Line, MathTex, Tex, LaggedStart, Write

ORDER = ["kasparov_topalov", "opera", "toujours_jeune", "immortelle", "deep_blue", "siecle"]
SHORT = {"kasparov_topalov": "Kasparov–Topalov 1999", "opera": "Opera Game 1858",
         "toujours_jeune": "Evergreen Game 1852", "immortelle": "Immortal Game 1851",
         "deep_blue": "Deep Blue–Kasparov 1997", "siecle": "Game of the Century 1956"}


class Beauty(Narrated):
    def bars(self, key, title, color, x0, sign=1):
        js = {k: json.load(open(ROOT / "melodies" / f"{k}.json")) for k in ORDER}
        g = VGroup(Text(title, font_size=26, color=color).move_to([x0, 2.4, 0]))
        axis = Line([x0, 2.0, 0], [x0, -2.9, 0], color=MUTED, stroke_width=2)
        g.add(axis)
        for r, k in enumerate(ORDER):
            z = js[k]["z"][key] * sign
            y = 1.6 - 0.85 * r
            w = abs(z) * 1.1
            bar = Rectangle(width=max(w, 0.02), height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.85)
            bar.move_to([x0 + np.sign(z) * w / 2, y, 0])
            g.add(bar, Text(f"{z:+.2f}", font_size=20, color=FG).next_to(bar, RIGHT if z >= 0 else LEFT, buff=0.1))
        return g

    def construct(self):
        self.chapter("10 · The most melodious game?")
        r1 = MathTex(r"\tfrac{3}{2}", r"\ \text{fifth}", r"\qquad \tfrac{5}{4}", r"\ \text{third}",
                     r"\qquad \sqrt2", r"\ \text{tritone}", font_size=40).shift(1.4 * UP)
        self.say("Can we measure musical beauty? Two classic ideas. First, simplicity: two notes in a row sound "
                 "well together when their frequencies are in a simple ratio, like three to two.", Write(r1))
        r2 = Tex(r"roughness: the beating of nearby frequencies (Sethares, 1993)", font_size=32, color=MUTED)
        self.say("Second, roughness: the unpleasant beating you hear when two close frequencies overlap.", FadeIn(r2))
        r3 = Tex(r"compared with 300 games of random legal moves", font_size=32, color=BAND).shift(1.4 * DOWN)
        self.say("And to be fair, we compare each game with three hundred games of random legal moves, "
                 "of the same length.", FadeIn(r3))
        self.play(FadeOut(VGroup(r1, r2, r3)), run_time=0.5)
        names = VGroup(*[Text(SHORT[k], font_size=22, color=FG).move_to([-4.6, 1.6 - 0.85 * r, 0]) for r, k in enumerate(ORDER)])
        b1 = self.bars("simplicite", "simplicity (σ)", GOOD, -0.6)
        b2 = self.bars("rugosite", "smoothness (σ)", BAND, 3.9, sign=-1)
        self.say("Here is the result, in standard deviations from random play. Kasparov's immortal against "
                 "Topalov has the simplest intervals. The Evergreen Game is the smoothest.",
                 FadeIn(names), FadeIn(b1), FadeIn(b2), run_time=2.0)
        self.say("And Fischer's Game of the Century, the most famous of all, comes last in simplicity.")
        self.say("But honestly, every difference is under two standard deviations: no game is clearly more "
                 "musical than chance. The great masters were not composing. Beautiful chess and beautiful music "
                 "are two different things.")
        self.play(FadeOut(VGroup(names, b1, b2)), run_time=0.6)
