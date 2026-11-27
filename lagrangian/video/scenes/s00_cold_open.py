"""s00 · Cold open: a thrown ball, the paths it could have taken, the one it takes; title."""
from lc import Narrated, np, Axes, VGroup, Dot, FG, MUTED, GOLD, RED, UP, DOWN, LEFT, RIGHT, ball
from manim import FadeIn, FadeOut, Create, Write, Tex, Text, MoveAlongPath, linear, LaggedStart


class ColdOpen(Narrated):
    def construct(self):
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 2, 1], x_length=10, y_length=4.4, tips=False,
                  axis_config=dict(color=MUTED, stroke_width=2, include_ticks=False)).shift(0.4 * DOWN)
        g, T, L = 9.81, 1.2, 4.0
        true = ax.plot_parametric_curve(lambda t: [L * t / T, 0.5 * g * t * (T - t) * 0.55], t_range=[0, T], color=GOLD, stroke_width=5)
        wrong = VGroup()
        rng = np.random.default_rng(3)
        for k in range(9):
            a, b = rng.normal(0, 0.9), rng.normal(0, 0.5)
            wrong.add(ax.plot_parametric_curve(
                lambda t, a=a, b=b: [L * t / T + 0.6 * b * np.sin(2 * np.pi * t / T),
                                     0.5 * g * t * (T - t) * 0.55 + a * np.sin(np.pi * t / T) + 0.3 * b * np.sin(3 * np.pi * t / T)],
                t_range=[0, T], color=MUTED, stroke_width=2, stroke_opacity=0.6))
        start, end = Dot(ax.c2p(0, 0), color=FG), Dot(ax.c2p(L, 0), color=FG)
        self.play(Create(ax), FadeIn(start), FadeIn(end), run_time=1.0)
        self.say("Throw a ball from here to there. It could, in principle, follow any of these paths.",
                 LaggedStart(*[Create(w) for w in wrong], lag_ratio=0.15), run_time=2.5)
        b = ball()
        d = self.voice("But it always picks the same one. Why this one?")
        self.play(Create(true), MoveAlongPath(b, true), run_time=max(d, 2.2), rate_func=linear)
        self.say("Newton's answer: forces push it, moment by moment. Two centuries of mathematicians found another "
                 "answer, stranger and far more powerful: of all possible paths, nature picks the one that makes a "
                 "single number, the action, stationary.", wrong.animate.set_stroke(opacity=0.25), run_time=1.5)
        names = Text("Euler · Lagrange · Hamilton · Noether", font_size=30, color=MUTED)
        title = Tex(r"The Principle of \emph{Least} Action", font_size=76, color=FG)
        sub = Tex("an introduction to Lagrangian mechanics", font_size=38, color=GOLD)
        grp = VGroup(title, sub, names).arrange(DOWN, buff=0.35)
        self.play(FadeOut(VGroup(ax, wrong, true, b, start, end)), run_time=0.8)
        d = self.voice("This is the principle of least action, and it is the backbone of all of modern physics.")
        self.play(Write(title), FadeIn(sub, shift=0.2 * UP), run_time=2)
        self.play(FadeIn(names), run_time=0.8)
        self.wait(max(0.5, d - 2.5) + 1)
        self.play(FadeOut(grp), run_time=0.8)
