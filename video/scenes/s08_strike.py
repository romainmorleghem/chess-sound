"""s08 · Striking the instrument: a kick = a mix of modes; amplitude v_k[i]/ω_k; degenerate energies;
corner vs centre; rook gestures; the music rules."""
from _common import (Narrated, Board, glyph, strike, modes, np, Spectrum, FG, MUTED, BAND, POS, ACCENT,
                     UP, DOWN, LEFT, RIGHT, parse, snd)
from manim import FadeIn, FadeOut, Write, Text, VGroup, MathTex, Tex, Create, LaggedStart, Line
from synth import Instrument


class Strike(Narrated):
    def construct(self):
        self.chapter("8 · Striking the instrument")
        w, V, lab = modes("N")
        i = parse("a1")
        e = np.zeros(64); e[i] = 1
        kick = Board(0.3).paint(e)
        terms = VGroup(kick, MathTex("=", font_size=40))
        for k in (1, 2, 3):
            terms.add(VGroup(MathTex(rf"{V[i, k]:+.2f}", font_size=30), Board(0.3).paint(V[:, k])).arrange(DOWN, buff=0.15))
            terms.add(MathTex("+", font_size=40))
        terms.add(MathTex(r"\cdots", font_size=40))
        terms.arrange(RIGHT, buff=0.3).shift(1.2 * UP)
        self.say("To play a move, we strike the piece's instrument on the arrival square: a sudden kick to "
                 "one single bead.", FadeIn(kick))
        f1 = MathTex(r"e_i = \sum_k v_k[i]\; v_k", font_size=42).next_to(terms, DOWN, buff=0.6)
        self.say("Like any shape, this kick is a mix of modes. How much of mode k? Simply v k at that square: "
                 "how much that mode moves there.", FadeIn(terms[1:]), Write(f1),
                 speech=None)
        f2 = MathTex(r"u(t) = \sum_k \frac{v_k[i]}{\omega_k}\; v_k \,\sin(\omega_k t)", font_size=42).next_to(f1, DOWN, buff=0.4)
        self.say("Then each mode rings on its own. Its loudness is v k at the struck square, divided by omega: "
                 "high modes are harder to excite.", Write(f2))
        self.say("So if you strike right on a node of a mode, that note stays silent. It's the same reason a "
                 "guitar plucked exactly in the middle loses half of its harmonics.")
        f3 = MathTex(r"a_\lambda = \frac{\lVert P_\lambda\, e_i \rVert}{\omega}", font_size=40, color=BAND).next_to(f2, DOWN, buff=0.4)
        self.say("When several modes share a note, we add their energies. That's the length of the kick "
                 "projected onto all of them, which doesn't depend on how we chose the modes.", Write(f3))
        self.play(FadeOut(VGroup(terms, f1, f2, f3)), run_time=0.5)

        # corner vs centre
        b = Board(0.55).shift(4.0 * LEFT)
        kn = glyph("N", size=38).move_to(b.pos("a1"))
        sp = Spectrum(width=7.0).shift(2.6 * RIGHT + 1.6 * DOWN)
        I = Instrument("N")
        la = sp.lines(I.freqs, I.amplitudes("a1"), y0=sp.axis.get_center()[1], h=2.6, color=BAND)
        self.say("Strike the knight in the corner. Few bands, a few low notes stand out.", FadeIn(b), FadeIn(kn), FadeIn(sp), Create(la))
        strike(self, "N_a1", b.pos("a1"))
        ld = sp.lines(I.freqs, I.amplitudes("d4"), y0=sp.axis.get_center()[1], h=2.6, color=POS)
        self.say("Now in the centre: same instrument, a different, brighter sound.",
                 kn.animate.move_to(b.pos("d4")), FadeOut(la), Create(ld))
        strike(self, "N_d4", b.pos("d4"), color=POS)
        self.say("And every note fades out, the high ones faster than the low ones, as on a real instrument.")
        self.play(FadeOut(VGroup(b, kn, sp, ld)), run_time=0.5)

        rules = VGroup(
            Tex(r"rook: all squares alike $\Rightarrow$ strike the move itself, $e_{\text{to}} - e_{\text{from}}$", font_size=30),
            Tex(r"capture: a harder strike", font_size=30),
            Tex(r"castling: king and rook together", font_size=30),
            Tex(r"check: a dissonant semitone", font_size=30),
            Tex(r"checkmate: a final major chord", font_size=30),
            Tex(r"White on the left, Black on the right", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.say("A few more rules, and we can play whole games. The rook is special: all its squares are alike, "
                 "so it would always sound the same. For the rook, we strike the move itself, from departure to arrival.",
                 FadeIn(rules[0]))
        self.say("Captures strike harder. Castling plays king and rook together. A check adds a dissonant semitone, "
                 "and checkmate resolves on a major chord. White plays on the left, Black on the right.",
                 LaggedStart(*[FadeIn(r) for r in rules[1:]], lag_ratio=0.4), run_time=3.0)
        self.play(FadeOut(rules), run_time=0.6)
