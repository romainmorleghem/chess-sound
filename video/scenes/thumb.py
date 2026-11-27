"""YouTube thumbnail (1280×720): manim -s -r 1280,720 thumb.py Thumbnail"""
from _common import Board, glyph, modes, np, FG, MUTED, BAND, POS, NEG, BG, UP, DOWN, LEFT, RIGHT
from manim import Scene, Text, VGroup, Arc, Line, BOLD, Circle, interpolate_color
from synth import Instrument


class Thumbnail(Scene):
    def construct(self):
        w, V, _ = modes("N")
        board = Board(0.68).paint(V[:, 10]).shift(3.75 * LEFT)
        halo = VGroup(*[Circle(radius=3.4 + 0.12 * k, stroke_width=10, stroke_opacity=0.05,
                               color=BAND).move_to(board) for k in range(6)])
        kn = Text("♞", font="DejaVu Sans", font_size=300, color="#F7F4EC")
        kn.set_stroke("#0E1116", 10, background=True).move_to(board).shift(0.15 * UP)
        waves = VGroup()
        for k in range(4):
            a = Arc(radius=1.35 + 0.45 * k, start_angle=-0.55, angle=1.1, stroke_width=11 - 2 * k,
                    color=BAND, stroke_opacity=1 - 0.2 * k).move_arc_center_to(kn.get_center() + 0.35 * RIGHT)
            waves.add(a)
        t1 = Text("WHAT DOES A", font="DejaVu Sans", weight=BOLD, font_size=62, color=FG)
        t2 = Text("KNIGHT", font="DejaVu Sans", weight=BOLD, font_size=128, color=BAND)
        t3 = Text("SOUND LIKE?", font="DejaVu Sans", weight=BOLD, font_size=62, color=FG)
        txt = VGroup(t1, t2, t3).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        txt.scale_to_fit_width(6.4).move_to(3.55 * RIGHT + 0.8 * UP)
        for t in txt:
            t.set_stroke(BG, 6, background=True)
        I = Instrument("N")
        a = I.amplitudes("d4"); m = I.freqs > 0
        f, a = I.freqs[m], a[m] / a[m].max()
        x = np.log(f / f.min()) / np.log(f.max() / f.min())
        bars = VGroup()
        for xi, ai in zip(x, a):
            col = interpolate_color(NEG, POS, xi)
            bars.add(Line([0, 0, 0], [0, 0.15 + 1.5 * ai, 0], stroke_width=7, color=col).shift(RIGHT * 5.2 * xi))
        bars.scale_to_fit_width(6.2).move_to(3.55 * RIGHT + 2.6 * DOWN, aligned_edge=DOWN)
        self.add(board, waves, kn, txt, bars)
