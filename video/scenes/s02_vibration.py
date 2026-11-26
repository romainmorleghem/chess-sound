"""s02 · How things vibrate: string harmonics, Chladni colours."""
from _common import (Narrated, Board, modes, strike, mode_color, np, FG, MUTED, POS, NEG, NODE, BAND,
                     UP, DOWN, LEFT, RIGHT, linear)
from manim import (FadeIn, FadeOut, Write, Create, MathTex, Tex, Text, VGroup, Dot, Line, Square,
                   UpdateFromAlphaFunc)


class Vibration(Narrated):
    def string(self, n=9):
        xs = np.linspace(-4.5, 4.5, n + 2)
        dots = VGroup(*[Dot([x, 1.2, 0], radius=0.09, color=FG) for x in xs])
        dots[0].set_color(MUTED); dots[-1].set_color(MUTED)
        lines = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center(), color=BAND, stroke_width=3)
                         for i in range(n + 1)])
        return xs, dots, lines

    def wiggle(self, xs, dots, lines, k, cycles, amp=0.9):
        n = len(xs) - 2
        u = np.sin(k * np.pi * np.arange(n + 2) / (n + 1))

        def upd(m, a):
            c = np.cos(2 * np.pi * cycles * a)
            for i, d in enumerate(dots):
                d.move_to([xs[i], 1.2 + amp * c * u[i], 0])
            for i, l in enumerate(lines):
                l.put_start_and_end_on(dots[i].get_center(), dots[i + 1].get_center())
        return UpdateFromAlphaFunc(VGroup(dots, lines), upd, rate_func=linear)

    def construct(self):
        self.chapter("2 · How things vibrate")
        xs, dots, lines = self.string()
        self.say("Before the chessboard, a guitar string: beads in a row, joined by springs.",
                 FadeIn(dots), Create(lines))
        self.say("Pluck it, and it vibrates in special shapes called modes.")
        for k, txt in ((1, "The fundamental: one belly."), (2, "Then two bellies, an octave higher."),
                       (3, "Then three. These are the harmonics.")):
            d = self.voice(txt)
            self.add_sound(f"{__import__('_common').SOUNDS}/string{k}.wav")
            self.play(self.wiggle(xs, dots, lines, k, cycles=2 * k), run_time=max(d + 0.3, 2.0))
        self.say("Each mode keeps its shape and just swings, at its own frequency. "
                 "And any vibration of the string is a mix of modes.")
        self.play(FadeOut(VGroup(dots, lines)), run_time=0.6)

        w, V, lab = modes("N")
        board = Board(0.62).shift(2.6 * LEFT)
        board.paint(V[:, 3])
        legend = VGroup()
        for col, t in ((POS, "moves up"), (NEG, "moves down"), (NODE, "node: stays still")):
            legend.add(VGroup(Square(0.4, fill_color=col, fill_opacity=1, stroke_width=0),
                              Text(t, font_size=26, color=FG)).arrange(RIGHT, buff=0.25))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(3.3 * RIGHT)
        self.say("For a plate, the modes are pictures. Sprinkle sand on a vibrating metal plate, and it gathers where nothing moves, on the nodes: "
                 "these are Chladni figures.", FadeIn(board))
        self.say("On our board we'll do the same with colours: red where the bead swings up, blue where it "
                 "swings down, white on the nodes.", FadeIn(legend))
        d = self.voice("And then we let it swing.")
        self.play(board.vibrate(V[:, 3], cycles=3), run_time=max(d + 0.5, 3.0))
        self.play(FadeOut(board), FadeOut(legend), run_time=0.6)
