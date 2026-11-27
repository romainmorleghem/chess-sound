"""s10 · Recap and how much to trust it."""
from fc import Narrated, Board, square_arrows, DATA, FG, MUTED, GOLD, UP, DOWN, LEFT, RIGHT
from manim import FadeIn, FadeOut, Tex, VGroup, LaggedStart


class Outro(Narrated):
    def construct(self):
        self.chapter("Recap")
        items = VGroup(*[Tex(t, font_size=32) for t in (
            r"175\,194 blitz games $\to$ density, flux, divergence, computed exactly",
            r"chess is not a local fluid: the smooth picture is only for the eye",
            r"Hodge: every flow = slope + whirlpools",
            r"masters: fewer whirlpools in the endgame (0.45 $\to$ 0.34), random play 0.55",
            r"masters capture on fewer squares; beginners rush the enemy king",
            r"no laminar/turbulent transition: skill changes the \emph{shape} of the flow")]
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(0.2 * UP)
        self.say("Let's recap. We turned a hundred and seventy-five thousand games into a fluid, and measured it exactly. "
                 "It is not a local fluid, but it has slopes and whirlpools. Masters swirl less in the endgame: their "
                 "flow runs downhill, towards a goal. They capture on fewer squares, and beginners rush the enemy king.",
                 LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.5), run_time=6.0)
        trust = Tex(r"exact identities $\cdot$ 200 resamplings $\cdot$ random-play control", font_size=28,
                    color=MUTED).to_edge(DOWN, buff=0.5)
        self.say("Every identity was checked to the last digit, every number comes with a confidence interval, and "
                 "everything is compared with players who move at random.", FadeIn(trust))
        self.play(FadeOut(VGroup(items, trust)), run_time=0.6)
        b = Board(0.55).paint(DATA["rho_2400"][20], vmax=DATA["rho_2400"].max())
        arr = square_arrows(b, DATA["D_2400_1"])
        end = Tex("The Chessboard as a Fluid", font_size=60, color=FG).to_edge(UP, buff=0.5)
        self.say("Chess, it turns out, is a fluid with intentions.", FadeIn(b), FadeIn(arr), FadeIn(end))
        self.wait(1.5)
        self.play(FadeOut(VGroup(b, arr, end)), run_time=1.0)
