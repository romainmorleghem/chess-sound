"""s03 · The maths, step by step: Hooke -> one equation per bead -> L = D − A -> u = v cos ωt ->
eigenvalue problem -> worked example (4 beads) -> 64×64 -> superposition -> f = 220√λ."""
from _common import (Narrated, Board, glyph, laplacian, adjacency, np, FG, MUTED, BAND, POS, NEG, ACCENT,
                     UP, DOWN, LEFT, RIGHT, linear)
from manim import (Group, FadeIn, FadeOut, Write, Create, MathTex, Tex, Text, VGroup, Dot, Line, Arrow, Matrix,
                   ImageMobject, SurroundingRectangle, UpdateFromAlphaFunc, TransformMatchingTex, Indicate)
from manim.constants import RESAMPLING_ALGORITHMS


def chain(n, x0=-3.0, dx=2.0, y=0.0):
    dots = VGroup(*[Dot([x0 + i * dx, y, 0], radius=0.12, color=FG) for i in range(n)])
    lines = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center(), color=BAND, stroke_width=4)
                     for i in range(n - 1)])
    return dots, lines


def swing(dots, lines, v, cycles, y=0.0, amp=0.8, edges=None):
    base = [d.get_center().copy() for d in dots]
    edges = edges or [(i, i + 1) for i in range(len(dots) - 1)]

    def upd(m, a):
        c = np.cos(2 * np.pi * cycles * a)
        for i, d in enumerate(dots):
            d.move_to(base[i] + [0, amp * c * v[i], 0])
        for l, (i, j) in zip(lines, edges):
            l.put_start_and_end_on(dots[i].get_center(), dots[j].get_center())
    return UpdateFromAlphaFunc(VGroup(dots, lines), upd, rate_func=linear)


class Maths(Narrated):
    def construct(self):
        self.chapter("3 · The maths, step by step")

        # --- step 1: one band, Hooke's law -------------------------------------------------------
        st = Text("step 1 · one rubber band", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        dots, lines = chain(2, x0=-1.5, dx=3.0, y=1.0)
        labs = VGroup(MathTex("u_i", font_size=36).next_to(dots[0], DOWN), MathTex("u_j", font_size=36).next_to(dots[1], DOWN))
        self.say("Let's do the maths, one step at a time. Call u the height of a bead above its rest position.",
                 FadeIn(st), FadeIn(dots), Create(lines), FadeIn(labs))
        hooke = MathTex(r"\text{pull on } i \;=\; -(u_i - u_j)", font_size=42).shift(1.2 * DOWN)
        self.say("A rubber band pulls back in proportion to how much it is stretched: that's Hooke's law. "
                 "If bead i sits higher than bead j, the band pulls it down by u i minus u j.",
                 Write(hooke), swing(dots, lines, [1, 0], cycles=1, y=1.0, amp=0.6), run_time=3.0)
        self.play(FadeOut(VGroup(dots, lines, labs, hooke)), run_time=0.5)

        # --- step 2: one bead, all its bands (knight on a1) --------------------------------------
        st2 = Text("step 2 · one bead, all its bands", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        P = {"a1": [-2.5, -0.2, 0], "b3": [-0.9, 2.0, 0], "c2": [0.4, 0.6, 0]}
        dd = {k: Dot(p, radius=0.12, color=FG) for k, p in P.items()}
        ll = VGroup(Line(P["a1"], P["b3"], color=BAND, stroke_width=4), Line(P["a1"], P["c2"], color=BAND, stroke_width=4))
        nm = VGroup(*[Text(k, font_size=24, color=MUTED).next_to(dd[k], DOWN + LEFT * 0.3, buff=0.12) for k in P])
        eq = MathTex(r"\ddot u_{a1}", r"=", r"-(u_{a1}-u_{b3}) - (u_{a1}-u_{c2})", font_size=40).shift(2.0 * DOWN)
        eq2 = MathTex(r"\ddot u_{a1}", r"=", r"-", r"2", r"\,u_{a1} + u_{b3} + u_{c2}", font_size=40).move_to(eq, aligned_edge=LEFT)
        self.say("Now a real bead: the corner a1, tied by the knight's two bands to b3 and c2.",
                 FadeOut(st), FadeIn(st2), *[FadeIn(d) for d in dd.values()], Create(ll), FadeIn(nm))
        self.say("Newton says acceleration equals force. The force is the sum of the pulls of its bands.",
                 Write(eq), speech=None)
        self.say("Expand it. The bead itself appears with a 2: the number of bands it carries. "
                 "Each neighbour appears with a plus one.", TransformMatchingTex(eq, eq2))
        self.play(Indicate(eq2[3], color=POS, scale_factor=1.6), run_time=1.0)
        self.play(FadeOut(VGroup(*dd.values(), ll, nm, eq2)), run_time=0.5)

        # --- step 3: a chain of 4 beads, the matrices ----------------------------------------------
        st3 = Text("step 3 · one equation per bead = one matrix", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        dots, lines = chain(4, x0=-3.0, dx=2.0, y=2.0)
        idx = VGroup(*[MathTex(str(i + 1), font_size=30, color=MUTED).next_to(dots[i], UP, buff=0.15) for i in range(4)])
        self.say("To see the whole picture, take a smaller net: four beads in a row. Write one such equation "
                 "for each bead, and stack them.", FadeOut(st2), FadeIn(st3), FadeIn(dots), Create(lines), FadeIn(idx))
        D = Matrix([[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]], h_buff=0.6).scale(0.6)
        A = Matrix([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]], h_buff=0.6).scale(0.6)
        L = Matrix([[1, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 1]], h_buff=0.75).scale(0.6)
        row = VGroup(MathTex("L", "=", font_size=40), L, MathTex("=", font_size=40), D,
                     MathTex("-", font_size=40), A).arrange(RIGHT, buff=0.25).shift(0.4 * DOWN)
        lD = MathTex(r"D:\ \text{bands per bead}", font_size=28, color=MUTED).next_to(row, DOWN, buff=0.35).shift(1.6 * RIGHT)
        lA = MathTex(r"A:\ \text{who is tied to whom}", font_size=28, color=MUTED).next_to(lD, DOWN, buff=0.15, aligned_edge=LEFT)
        self.say("The numbers on the diagonal, the band counts, form the matrix D. The plus ones, one for each "
                 "pair of tied beads, form the adjacency matrix A.", FadeIn(row[3]), FadeIn(lD), FadeIn(row[5]), FadeIn(lA), FadeIn(row[4]))
        self.say("Their difference, L equals D minus A, is the Laplacian of the network. All the physics of "
                 "the net fits in this one table of numbers.", FadeIn(row[0]), FadeIn(row[1]), FadeIn(row[2]), FadeIn(L),
                 speech=None)
        law = MathTex(r"\ddot u = -L\,u", font_size=46, color=BAND).next_to(row, DOWN, buff=1.5)
        self.say("And Newton's law for all the beads at once becomes: u double dot equals minus L u.", Write(law))
        self.play(FadeOut(VGroup(row, lD, lA, law)), run_time=0.5)

        # --- step 4: the guess u = v cos(ωt) -> eigenvalue problem --------------------------------
        st4 = Text("step 4 · look for shapes that keep their shape", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        g1 = MathTex(r"u(t) = v\,\cos(\omega t)", font_size=44).shift(0.2 * DOWN)
        g2 = MathTex(r"-\omega^2 v\cos(\omega t) = -L\,v\cos(\omega t)", font_size=44).next_to(g1, DOWN, buff=0.4)
        g3 = MathTex(r"L\,v = \omega^2\, v", font_size=54, color=BAND).next_to(g2, DOWN, buff=0.5)
        self.say("Now the key idea. Look for motions where every bead swings in step: a fixed shape v, "
                 "multiplied by cos omega t.", FadeOut(st3), FadeIn(st4), Write(g1))
        self.say("Plug it into the equation. The cosine appears on both sides and cancels.", Write(g2), speech=None)
        self.say("What's left is the question: which shapes v does L simply multiply by a number? "
                 "This is called an eigenvalue problem. The shapes v are the eigenvectors, the modes. "
                 "The numbers lambda equal omega squared are the eigenvalues. So the frequency is the square root "
                 "of lambda.", Write(g3))
        self.play(FadeOut(VGroup(g1, g2, g3)), run_time=0.5)

        # --- step 5: solve the 4-bead example --------------------------------------------------------
        st5 = Text("step 5 · solve it for the 4 beads", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        self.play(FadeOut(st4), FadeIn(st5), FadeOut(VGroup(dots, lines, idx)), run_time=0.6)
        w, V = np.linalg.eigh(laplacian(adjacency_path(4)).astype(float))
        panels, anims = VGroup(), []
        for k in range(4):
            d, l = chain(4, x0=-0.9, dx=0.6, y=0)
            v = V[:, k] * np.sign(V[0, k] + 1e-9)
            lab = MathTex(rf"\lambda_{k+1} = {['0', r'2-\sqrt2', '2', r'2+\sqrt2'][k]}", font_size=30)
            lab2 = MathTex(rf"\approx {max(w[k], 0):.2f}", font_size=26, color=MUTED)
            grp = VGroup(VGroup(d, l), VGroup(lab, lab2).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.9)
            panels.add(grp)
        panels.arrange(RIGHT, buff=0.8).shift(0.3 * DOWN)
        for k, grp in enumerate(panels):
            v = V[:, k] * np.sign(V[0, k] + 1e-9)
            anims.append(swing(grp[0][0], grp[0][1], v, cycles=max(1, 2 * np.sqrt(max(w[k], 0))), amp=0.6))
        self.say("For four beads you can solve it by hand. There are exactly four modes.", FadeIn(panels))
        self.say("The first one, lambda equals zero, is all beads moving together: nothing stretches, "
                 "nothing rings. It makes no sound. The others swing faster and faster, with more and more "
                 "sign changes, exactly like the harmonics of the string.", *anims, run_time=6.0)
        self.play(FadeOut(panels), run_time=0.5)

        # --- step 6: 64 beads, the computer ---------------------------------------------------------
        st6 = Text("step 6 · the chessboard: a 64 × 64 matrix", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        Lk = laplacian(adjacency("N")).astype(float)
        rgb = np.full((64, 64, 3), 22, np.uint8)
        rgb[Lk > 0] = (242, 181, 68)
        rgb[Lk < 0] = (63, 127, 200)
        img = ImageMobject(rgb)
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.set(height=4.6).shift(3.3 * LEFT + 0.4 * DOWN)
        cap = Tex(r"knight: $L = D - A$ \\ \small gold = band counts (2 to 8), blue = $-1$", font_size=28,
                  color=MUTED).next_to(img, DOWN, buff=0.2)
        arr = Arrow(LEFT, RIGHT, color=FG).shift(0.4 * DOWN + 0.3 * LEFT)
        out = MathTex(r"64 \text{ pairs } (\lambda_k, v_k)", r"\\ \text{in a millisecond}", font_size=38).shift(3.4 * RIGHT + 0.4 * DOWN)
        self.say("For the chessboard it's the same recipe, with sixty-four beads. The knight's Laplacian is a "
                 "table of sixty-four by sixty-four numbers.", FadeOut(st5), FadeIn(st6), FadeIn(img), FadeIn(cap))
        self.say("Nobody solves that by hand, but a computer finds the sixty-four eigenvalues and modes in a "
                 "millisecond. That's all the maths we need.", Create(arr), Write(out))
        self.play(FadeOut(Group(img, cap, arr, out)), run_time=0.5)

        # --- step 7: superposition, and the unit of frequency -----------------------------------------
        st7 = Text("step 7 · from numbers to sound", font_size=26, color=ACCENT).to_edge(UP, buff=0.9)
        s1 = MathTex(r"u(t) = \sum_k c_k\, v_k \cos(\omega_k t)", font_size=46).shift(0.6 * UP)
        s2 = MathTex(r"f_k = 220\,\text{Hz} \times \sqrt{\lambda_k}", font_size=46, color=BAND).shift(0.9 * DOWN)
        s3 = Tex(r"pawn: 113 Hz \quad \dots \quad queen: 1206 Hz", font_size=32, color=MUTED).next_to(s2, DOWN, buff=0.4)
        self.say("Because the equation is linear, any motion of the net is a mix of its modes, each swinging "
                 "at its own frequency. That's what your ear hears: a chord of the modes.",
                 FadeOut(st6), FadeIn(st7), Write(s1))
        self.say("The rubber bands have no units, so we choose one: 220 hertz times the square root of lambda. "
                 "Same rule for every piece, and every note lands in the audible range.", Write(s2), FadeIn(s3))
        self.play(FadeOut(VGroup(st7, s1, s2, s3)), run_time=0.6)


def adjacency_path(n):
    A = np.zeros((n, n), int)
    for i in range(n - 1):
        A[i, i + 1] = A[i + 1, i] = 1
    return A
