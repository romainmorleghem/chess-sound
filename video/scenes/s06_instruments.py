"""s06 · The six spectra, piece by piece."""
from _common import (Narrated, Spectrum, glyph, strike, np, PIECE_COLOR, PIECE_NAME, FG, MUTED, BAND,
                     UP, DOWN, LEFT, RIGHT)
from manim import FadeIn, FadeOut, Create, Text, VGroup, MathTex, Write, LaggedStart, Line
from synth import Instrument

_F = {p: Instrument(p).freqs[Instrument(p).freqs > 0] for p in "RBNKQP"}
TEXT = {
    "R": "The rook first. Every square is like every other for a rook, and its Laplacian has only three "
         "eigenvalues: zero, eight and sixteen. So the rook doesn't play a melody, it plays a chord of two notes, "
         f"{_F['R'][0]:.0f} and {_F['R'][1]:.0f} hertz.",
    "B": "The bishop never changes colour, so it builds two separate nets, the light squares and the dark ones. "
         "And they are mirror images of each other: it's the same instrument twice. Every note is doubled.",
    "N": f"The knight: forty-eight different notes, spread between {_F['N'].min():.0f} and {_F['N'].max():.0f} hertz.",
    "K": "The king moves one step at a time, a soft and loose net. It goes down to "
         f"{_F['K'].min():.0f} hertz, and its notes even have an exact formula.",
    "Q": "The queen is tied to twenty-one to twenty-seven beads each. A very stiff instrument: all its notes are "
         f"above {_F['Q'].min():.0f} hertz.",
    "P": f"And the pawn, with our convention: the loosest net of all, and the deepest note, {_F['P'].min():.0f} hertz.",
}


class Instruments(Narrated):
    def construct(self):
        self.chapter("6 · Six instruments")
        sp = Spectrum(width=10.5).shift(3.1 * DOWN + 0.7 * RIGHT)
        self.play(FadeIn(sp), run_time=0.6)
        ys = {p: 2.4 - 0.95 * k for k, p in enumerate("RBNKQP")}
        for p in "RBNKQP":
            I = Instrument(p)
            m = I.freqs > 0
            mult = np.array([U.shape[1] for _, U in I.levels])[m]
            lines = VGroup()
            for f, mu in zip(I.freqs[m], mult):
                x = sp.x(f) + sp.axis.get_center()[0]
                lines.add(Line([x, ys[p] - 0.3, 0], [x, ys[p] + 0.3, 0],
                               color=PIECE_COLOR[p], stroke_width=2 + 0.25 * min(mu, 16)))
            lab = VGroup(glyph(p, size=34, color=PIECE_COLOR[p]),
                         Text(PIECE_NAME[p], font_size=24, color=PIECE_COLOR[p])).arrange(RIGHT, buff=0.15)
            lab.move_to([-6.0, ys[p], 0])
            self.say(TEXT[p], FadeIn(lab), Create(lines, lag_ratio=0.05), run_time=1.5)
            if p == "R":
                tri = MathTex(rf"\frac{{{_F['R'][1]:.0f}}}{{{_F['R'][0]:.0f}}} = \sqrt{{2}}", r"\ \text{: the tritone}", font_size=36,
                              color=BAND).move_to([-1.6, ys[p], 0])
                self.say("Their ratio is exactly the square root of two. In music that's the tritone, the interval "
                         "nicknamed the devil in music.", Write(tri))
                lines.set_color(FG)
                strike(self, "R_chord", None, dur=3.0, also=[lines.animate.set_color(PIECE_COLOR[p])])
                self.play(FadeOut(tri), run_time=0.4)
            elif p == "K":
                fk = MathTex(r"\lambda_{jk} = 9 - (1+2\cos\tfrac{\pi j}{9})(1+2\cos\tfrac{\pi k}{9})",
                             font_size=30, color=PIECE_COLOR["K"]).move_to([-1.9, ys["B"], 0])
                self.play(FadeIn(fk), run_time=0.6)
                lines.set_color(FG)
                strike(self, "K_d4", None, also=[lines.animate.set_color(PIECE_COLOR[p])])
                self.play(FadeOut(fk), run_time=0.4)
            else:
                lines.set_color(FG)
                strike(self, f"{p}_d4", None, also=[lines.animate.set_color(PIECE_COLOR[p])])
        self.say("Six pieces, six spectra. Thick lines are notes shared by several modes.")
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.chapter_tag], run_time=0.8)
