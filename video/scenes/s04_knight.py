"""s04 · The knight's modes; the highest one is the checkerboard (bipartite)."""
from _common import (Narrated, Board, modes, strike, glyph, np, adjacency, normalized_laplacian, coords,
                     FG, MUTED, BAND, UP, DOWN, LEFT, RIGHT)
from manim import FadeIn, FadeOut, Text, VGroup, Tex, LaggedStart, MathTex


class Knight(Narrated):
    def construct(self):
        self.chapter("4 · The knight's modes")
        w, V, lab = modes("N")
        board = Board(0.7).shift(2.5 * LEFT)
        info = Text("", font_size=30).shift(3.2 * RIGHT)
        self.play(FadeIn(board), run_time=0.6)
        self.say("Here is the lowest note of the knight. Half the board swings up while the other half "
                 "swings down, with a quiet line of nodes in between.")
        for k, txt in ((1, None), (3, "Higher modes have more nodes, like the harmonics of the string."),
                       (10, "Higher still. The pattern gets finer and finer.")):
            f = 220 * np.sqrt(w[k])
            new = Text(f"mode {k}\nλ = {w[k]:.3f}\nf = {f:.0f} Hz", font_size=30, color=FG, line_spacing=1.2).shift(3.2 * RIGHT)
            if txt:
                d = self.voice(txt)
            self.add(new); self.remove(info); info = new
            self.add_sound(f"{__import__('_common').SOUNDS}/Nmode{k}.wav")
            self.play(board.vibrate(V[:, k], cycles=4), run_time=2.6)
        self.play(FadeOut(board), FadeOut(info), run_time=0.5)

        grid = VGroup()
        for k in range(1, 17):
            b = Board(0.17).paint(V[:, k])
            t = Text(f"{220*np.sqrt(w[k]):.0f} Hz", font_size=14, color=MUTED).next_to(b, DOWN, buff=0.08)
            grid.add(VGroup(b, t))
        grid.arrange_in_grid(2, 8, buff=(0.25, 0.35)).shift(0.3 * DOWN)
        self.say("The knight has sixty-four modes, with forty-eight different frequencies, from 235 to 794 hertz. "
                 "Here are the first sixteen.", LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.08), run_time=2.5)
        self.play(FadeOut(grid), run_time=0.6)

        # bipartite: the knight always changes colour
        b2 = Board(0.62).shift(3.2 * LEFT)
        kn = glyph("N", size=44).move_to(b2.pos("a1"))
        self.play(FadeIn(b2), FadeIn(kn), run_time=0.5)
        d = self.voice("A knight has a peculiar habit: every jump changes the colour of its square. "
                       "Light, dark, light, dark.")
        path = ["b3", "c1", "e2", "g3", "h5"]
        rt = (d + 0.3) / len(path)
        for s in path:
            self.play(kn.animate.move_to(b2.pos(s)), run_time=rt)
        A = adjacency("N")
        dg = A.sum(1).astype(float)
        wn, Vn = np.linalg.eigh(normalized_laplacian(A))
        rw = Vn[:, -1] / np.sqrt(dg)
        rw *= np.sign(rw[0])
        b3 = Board(0.62).shift(3.2 * RIGHT).paint(rw)
        cap = Tex(r"top mode of $I - D^{-1/2} A D^{-1/2}$", font_size=28, color=MUTED).next_to(b3, DOWN, buff=0.2)
        self.say("So with the version of the Laplacian that describes a knight wandering at random, the highest "
                 "mode is exactly the checkerboard: every bead swings against all its neighbours.",
                 FadeIn(b3), FadeIn(cap), speech=None)
        self.play(b3.vibrate(rw, cycles=4), run_time=2.5)
        self.play(FadeOut(VGroup(b2, kn, b3, cap)), run_time=0.6)
