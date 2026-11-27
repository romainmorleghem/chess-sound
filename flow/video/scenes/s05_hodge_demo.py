"""s05 · Slopes and whirlpools: synthetic potential flow, vortex, mix, and Hodge recovering both exactly."""
from fc import Narrated, Board, links, edge_arrows, square_arrows, edge_vectors, np, FG, MUTED, GOLD, RED, BLUE, UP, DOWN, LEFT, RIGHT, EDGES
from manim import FadeIn, FadeOut, Write, Create, Text, MathTex, Tex, VGroup, LaggedStart
from hodge import Hodge

H = Hodge()
EI = {e: k for k, e in enumerate(EDGES)}


def loop_flux(path):
    J = np.zeros(len(EDGES))
    for a, b in zip(path, path[1:] + path[:1]):
        J[EI[(min(a, b), max(a, b))]] += 1 if a < b else -1
    return J


def sq(name):
    return "abcdefgh".index(name[0]) + 8 * (int(name[1]) - 1)


class HodgeDemo(Narrated):
    def construct(self):
        self.chapter("5 · Slopes and whirlpools")
        phi = -np.array([i // 8 for i in range(64)], float)          # altitude décroît vers le haut
        phi += -0.25 * np.abs(np.array([i % 8 for i in range(64)]) - 3.5)
        Jg = H.B @ phi
        ring = [sq(s) for s in ("c3", "d3", "e3", "f3", "f4", "f5", "f6", "e6", "d6", "c6", "c5", "c4")]
        Jc = 1.2 * loop_flux(ring)
        bg = Board(0.38).paint(phi - phi.min()).shift(4.4 * LEFT + 0.5 * UP)
        bc = Board(0.38).shift(0.5 * UP)
        vm = max(np.abs(edge_vectors(Jg)).max(), np.abs(edge_vectors(Jc)).max(), np.abs(edge_vectors(Jg + Jc)).max())
        ag = square_arrows(bg, edge_vectors(Jg), vmax=vm, color="#14161A")
        ac = square_arrows(bc, edge_vectors(Jc), color=FG)
        tg = Text("slope (gradient)", font_size=24, color=GOLD).next_to(bg, UP, buff=0.2)
        tc = Text("whirlpool (rotational)", font_size=24, color=RED).next_to(bc, UP, buff=0.2)
        self.say("Fluids come in two pure kinds. The first is a slope: give every square an altitude, and let the "
                 "flow run downhill, like water down a mountain.", FadeIn(bg), FadeIn(ag), FadeIn(tg))
        self.say("The second is a whirlpool: the flow goes round and round. It never piles up anywhere, so its "
                 "divergence is zero everywhere.", FadeIn(bc), FadeIn(ac), FadeIn(tc))
        bm = Board(0.38).shift(4.4 * RIGHT + 0.5 * UP)
        am = square_arrows(bm, edge_vectors(Jg + Jc), vmax=vm, color=FG)
        tm = Text("a real flow: both", font_size=24, color=FG).next_to(bm, UP, buff=0.2)
        self.say("A real flow mixes the two, and to the eye, they're tangled.", FadeIn(bm), FadeIn(am), FadeIn(tm))
        thm = MathTex(r"J", r"=", r"\underbrace{B\,\varphi}_{\text{gradient}}", r"+",
                      r"\underbrace{C^{\top}\psi}_{\text{rotational}}", r"+", r"\underbrace{h}_{=\,0}", font_size=38).to_edge(DOWN, buff=0.5)
        self.say("But a theorem, the Hodge decomposition, untangles them. Any flow on the board splits, in exactly "
                 "one way, into a slope part, a whirlpool part, and a third part that would circle around holes. "
                 "The chessboard has no holes, so that part is zero.", Write(thm))
        g, c, h, _, _ = H.decompose(Jg + Jc)
        err = max(np.abs(g - Jg).max(), np.abs(c - Jc).max())
        chk = Tex(rf"recovered exactly: error $\approx 10^{{{int(np.floor(np.log10(err + 1e-300)))}}}$", font_size=30,
                  color=GOLD).next_to(thm, UP, buff=0.3).shift(3.2 * LEFT)
        self.say("Feed it the tangled flow: it gives back the slope and the whirlpool, to machine precision.", FadeIn(chk))
        fr = H.fractions(Jg + Jc)
        en = Tex(rf"energy: {100*fr[0]:.0f}\,\% slope, {100*fr[1]:.0f}\,\% whirlpool", font_size=30, color=FG).next_to(thm, UP, buff=0.3).shift(3.2 * RIGHT)
        self.say("And we can measure how much of the flow's energy is whirlpool. That single number, the rotational "
                 "fraction, will be our fingerprint of a player.", FadeIn(en))
        self.play(FadeOut(VGroup(bg, bc, bm, ag, ac, am, tg, tc, tm, thm, chk, en)), run_time=0.6)
