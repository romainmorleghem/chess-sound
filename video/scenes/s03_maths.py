"""s03 · The maths, to the essentials: Newton + Hooke on bead a1 -> u'' = −L u with L = D − A (the knight's
64×64 matrices) -> u = v cos ωt gives L v = ω² v -> 64 modes, λ = 0 silent -> superposition, f = F0 √λ."""
from _common import (Narrated, Board, bands, laplacian, adjacency, modes, np, FG, MUTED, BAND, POS, NEG, ACCENT,
                     UP, DOWN, LEFT, RIGHT)
from manim import (Group, FadeIn, FadeOut, Write, Create, MathTex, Tex, Text, VGroup, Dot, ImageMobject,
                   TransformMatchingTex, Indicate, SurroundingRectangle, Line)
from manim.constants import RESAMPLING_ALGORITHMS
from modes import F0


def heat(M, pos_rgb=(242, 181, 68), neg_rgb=(63, 127, 200), h=3.0):
    rgb = np.full(M.shape + (3,), 30, np.uint8)
    mx = max(M.max(), 1)
    for i, j in zip(*np.nonzero(M > 0)):
        a = 0.45 + 0.55 * M[i, j] / mx
        rgb[i, j] = (np.array(pos_rgb) * a + 30 * (1 - a)).astype(np.uint8)
    rgb[M < 0] = neg_rgb
    img = ImageMobject(rgb)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img.set(height=h)


class Maths(Narrated):
    def construct(self):
        self.chapter("3 · The maths")

        # 1. one bead: Newton + Hooke ------------------------------------------------------------------
        board = Board(0.5).shift(4.2 * LEFT + 0.3 * DOWN)
        e1 = bands(board, "N", ["a1"], width=4)
        hi = VGroup(*[Dot(board.pos(s), radius=0.1, color=BAND) for s in ("a1", "b3", "c2")])
        eq = MathTex(r"\ddot u_{a1}", r"=", r"-(u_{a1}-u_{b3}) - (u_{a1}-u_{c2})", font_size=40)
        eq2 = MathTex(r"\ddot u_{a1}", r"=", r"-", r"2", r"\,u_{a1}", r"+ u_{b3} + u_{c2}", font_size=40)
        VGroup(eq, eq2).move_to(2.3 * RIGHT + 1.0 * UP)
        self.say("Let u be how far each bead is pushed out of the board. Take the corner bead, a1. "
                 "Each of its two bands pulls it back towards its neighbour, in proportion to the stretch: "
                 "that's Hooke's law, and Newton turns force into acceleration.",
                 FadeIn(board), Create(e1), FadeIn(hi), Write(eq), run_time=2.5)
        self.say("Expand: the bead appears with a 2, its number of bands, and each neighbour with a plus one.",
                 TransformMatchingTex(eq, eq2))
        self.play(Indicate(eq2[3], color=POS, scale_factor=1.7), run_time=0.9)

        # 2. all beads: L = D − A (real 64×64 knight matrices) ------------------------------------------
        A = adjacency("N")
        Dm = np.diag(A.sum(1))
        iD, iA, iL = heat(Dm, h=2.7), heat(-A, h=2.7), heat(laplacian(A), h=2.7)
        row = Group(iD, MathTex("-", font_size=56), iA, MathTex("=", font_size=56), iL).arrange(RIGHT, buff=0.35)
        row.move_to(0.7 * DOWN)
        labs = VGroup(MathTex("D", font_size=40, color=BAND).next_to(iD, UP, buff=0.15),
                      MathTex("A", font_size=40, color=NEG).next_to(iA, UP, buff=0.15),
                      MathTex("L", font_size=40, color=FG).next_to(iL, UP, buff=0.15))
        subs = VGroup(Tex("bands per bead", font_size=24, color=MUTED).next_to(iD, DOWN, buff=0.15),
                      Tex("who is tied to whom", font_size=24, color=MUTED).next_to(iA, DOWN, buff=0.15),
                      Tex("the Laplacian", font_size=24, color=MUTED).next_to(iL, DOWN, buff=0.15))
        law = MathTex(r"\ddot u = -L\,u", font_size=48, color=BAND).move_to(2.4 * UP)
        self.say("Write that line for all sixty-four beads and stack them. The band counts form a diagonal "
                 "matrix D, the ties form the adjacency matrix A, and their difference L, the Laplacian, "
                 "holds all the physics of the net.",
                 FadeOut(VGroup(eq2, board, e1, hi)), FadeIn(row), FadeIn(labs), FadeIn(subs), run_time=2.5)
        self.say("Here they are for the knight, sixty-four by sixty-four: gold for the band counts, "
                 "blue for the ties. Newton's law for the whole board reads: u double dot equals minus L u.",
                 Write(law))
        self.play(FadeOut(Group(row, labs, subs, law)), run_time=0.6)

        # 3. the guess -> eigenvalue problem ------------------------------------------------------------
        w, V, _ = modes("N")
        g1 = MathTex(r"u(t) = v\,\cos(\omega t)", font_size=44)
        g2 = MathTex(r"\Longrightarrow\quad L\,v = \omega^2 v", font_size=44, color=BAND)
        g3 = MathTex(r"\lambda = \omega^2 \quad\Longrightarrow\quad f \propto \sqrt{\lambda}", font_size=40)
        col = VGroup(g1, g2, g3).arrange(DOWN, buff=0.55, aligned_edge=LEFT).shift(2.6 * RIGHT)
        vb = Board(0.5).paint(V[:, 3]).shift(3.6 * LEFT)
        self.say("Now the key move. Look for motions where every bead swings in step: one fixed shape v, "
                 "times cos omega t.", Write(g1), FadeIn(vb))
        d = self.voice("Plug it in, the cosines cancel, and what remains is an eigenvalue problem: which shapes "
                       "does L only stretch, by a factor omega squared?")
        self.play(Write(g2), vb.vibrate(V[:, 3], cycles=3), run_time=d + 0.4)
        self.say("Those shapes are the modes. The stretch factors lambda are the eigenvalues, and each mode "
                 "rings at a frequency proportional to the square root of lambda.", Write(g3))
        self.play(FadeOut(VGroup(g1, g2, g3, vb)), run_time=0.5)

        # 4. solving, λ = 0, superposition, the unit ------------------------------------------------------
        s1 = MathTex(r"64\times 64\ \text{symmetric} \;\Rightarrow\; 64\ \text{modes } (\lambda_k, v_k)",
                     font_size=40).shift(1.8 * UP)
        s0 = Tex(r"$\lambda_0 = 0$: the whole net moves as one, nothing stretches: silent", font_size=32,
                 color=MUTED).next_to(s1, DOWN, buff=0.35)
        s2 = MathTex(r"u(t) = \sum_k c_k\, v_k \cos(\omega_k t + \varphi_k)", font_size=44).next_to(s0, DOWN, buff=0.6)
        s3 = MathTex(rf"f_k = {F0:.0f}\,\text{{Hz}} \times \sqrt{{\lambda_k}}", font_size=48,
                     color=BAND).next_to(s2, DOWN, buff=0.6)
        self.say("A computer finds all sixty-four modes of a matrix like this in a millisecond. "
                 "The first one, lambda zero, is the whole net moving as one block: nothing stretches, "
                 "so it makes no sound.", Write(s1), FadeIn(s0))
        self.say("And since the equations are linear, any motion is a mix of modes, each at its own pitch. "
                 "That chord is what your ear hears.", Write(s2))
        self.say(f"Rubber bands have no units, so we pick one: {F0:.0f} hertz times the square root of lambda, "
                 "the same rule for every piece.", Write(s3))
        self.play(FadeOut(VGroup(s1, s0, s2, s3)), run_time=0.6)
