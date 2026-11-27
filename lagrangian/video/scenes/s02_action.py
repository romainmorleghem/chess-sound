"""s02 · Lagrangian and action; the stationary-action demo S(ε) on a vertical throw."""
from lc import Narrated, np, Axes, VGroup, Dot, Line, FG, MUTED, GOLD, RED, BLUE, GREEN, TEAL, UP, DOWN, LEFT, RIGHT
from manim import (FadeIn, FadeOut, Create, Write, MathTex, Tex, Text, ValueTracker, always_redraw, linear,
                   there_and_back, SurroundingRectangle, DecimalNumber)

g, T, m = 9.81, 1.0, 1.0
ts = np.linspace(0, T, 400)
y0 = 0.5 * g * ts * (T - ts)
v0 = 0.5 * g * (T - 2 * ts)
eta, deta = np.sin(np.pi * ts / T), np.pi / T * np.cos(np.pi * ts / T)


def path(eps):
    return y0 + eps * eta, v0 + eps * deta


def lag(eps):
    y, v = path(eps)
    return 0.5 * m * v ** 2 - m * g * y


def action(eps):
    return np.trapezoid(lag(eps), ts)


class Action(Narrated):
    def construct(self):
        self.chapter("2 · The Lagrangian and the action")
        L = MathTex(r"L", r"=", r"E_c", r"-", r"E_p", font_size=60).shift(1.5 * UP + 3 * LEFT)
        S = MathTex(r"S", r"=", r"\int_{t_0}^{t_1} L\,dt", font_size=60).shift(1.5 * UP + 3 * RIGHT)
        self.say("Here is the new idea. At each instant, take the kinetic energy minus the potential energy. "
                 "Not the sum: the difference. This is the Lagrangian, L.", Write(L))
        self.say("Add it up along the whole path, from start to finish: that's the action, S. One single number for "
                 "a whole trajectory.", Write(S))
        ff = MathTex(r"L = \tfrac12 m(\dot x^2 + \dot y^2) - m g y", font_size=44, color=GOLD).shift(0.2 * DOWN)
        self.say("For a ball in free fall: one half m v squared, minus m g y.", Write(ff))
        self.play(FadeOut(VGroup(L, S, ff)), run_time=0.6)
        # démo : lancer vertical, chemins y_ε = y + ε sin(πt/T)
        a1 = Axes(x_range=[0, 1, 0.5], y_range=[-0.4, 2.2, 1], x_length=5.6, y_length=2.6, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.3 * LEFT + 1.4 * UP)
        a2 = Axes(x_range=[0, 1, 0.5], y_range=[-20, 14, 10], x_length=5.6, y_length=2.4, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.3 * LEFT + 2.0 * DOWN)
        a3 = Axes(x_range=[-1.4, 1.4, 0.7], y_range=[-2, 5, 1], x_length=5.0, y_length=4.4, tips=False,
                  axis_config=dict(color=MUTED, include_ticks=False)).shift(3.6 * RIGHT + 0.2 * DOWN)
        labs = VGroup(MathTex("y(t)", font_size=28, color=MUTED).next_to(a1, UP, buff=0.05),
                      MathTex("L(t)", font_size=28, color=MUTED).next_to(a2, UP, buff=0.05),
                      MathTex(r"S(\varepsilon)", font_size=34, color=FG).next_to(a3, UP, buff=0.1),
                      MathTex(r"\varepsilon", font_size=30, color=MUTED).next_to(a3.x_axis, RIGHT),
                      MathTex(r"t", font_size=28, color=MUTED).next_to(a1.x_axis, RIGHT),
                      MathTex(r"t", font_size=28, color=MUTED).next_to(a2.x_axis, RIGHT))
        e = ValueTracker(0.0)
        S0 = action(0)
        curveS = a3.plot(lambda x: action(x) - S0 - 1.0, x_range=[-1.4, 1.4], color=MUTED, stroke_width=3)
        true = a1.plot_line_graph(ts, y0, add_vertex_dots=False, line_color=GOLD, stroke_width=3)
        cur = always_redraw(lambda: a1.plot_line_graph(ts, path(e.get_value())[0], add_vertex_dots=False,
                                                       line_color=FG if abs(e.get_value()) > 0.02 else GOLD, stroke_width=4))

        def area():
            Lt = lag(e.get_value())
            pts = [a2.c2p(t, v) for t, v in zip(ts[::4], Lt[::4])]
            poly = VGroup(*[Line(a2.c2p(t, 0), a2.c2p(t, v), stroke_width=2,
                                 color=GREEN if v > 0 else RED, stroke_opacity=0.45) for t, v in zip(ts[::8], Lt[::8])])
            return VGroup(poly, a2.plot_line_graph(ts, Lt, add_vertex_dots=False, line_color=FG, stroke_width=3))
        ar = always_redraw(area)
        dot = always_redraw(lambda: Dot(a3.c2p(e.get_value(), action(e.get_value()) - S0 - 1.0), color=GOLD, radius=0.09))
        val = always_redraw(lambda: VGroup(MathTex(r"\varepsilon =", font_size=30),
                                           DecimalNumber(e.get_value(), num_decimal_places=2, font_size=30)).arrange(RIGHT).next_to(a3, DOWN, buff=0.15))
        self.say("Let's see it in action. A ball thrown straight up, which comes back down after one second. "
                 "Top left, its height over time. Bottom left, the Lagrangian along the way.",
                 Create(a1), Create(a2), FadeIn(labs[0]), FadeIn(labs[1]), FadeIn(labs[4]), FadeIn(labs[5]), FadeIn(true), FadeIn(ar))
        self.add(cur)
        self.say("Now deform the path, keeping the same start and the same end: add epsilon times a bump. "
                 "For each path, compute the action, the signed area under L.",
                 Create(a3), FadeIn(labs[2]), FadeIn(labs[3]), FadeIn(dot), FadeIn(val))
        d = self.voice("Watch the action as epsilon changes. Any deformation, up or down, increases it.")
        self.play(e.animate.set_value(1.4), run_time=max(d / 2, 2.5), rate_func=linear)
        self.play(e.animate.set_value(-1.4), run_time=max(d / 2, 3.5), rate_func=linear)
        self.add(curveS)
        self.play(e.animate.set_value(0), run_time=2)
        tag = Tex(r"stationary: $\dfrac{dS}{d\varepsilon}\Big|_{\varepsilon=0}=0$", font_size=32, color=GOLD).move_to(a3.c2p(0, 3.6))
        self.say("The real path sits exactly at the bottom: there, the action does not change to first order. "
                 "That's the principle. Strictly speaking it is not always a minimum, only a stationary point; "
                 "least action is a nickname.", FadeIn(tag))
        self.play(FadeOut(VGroup(a1, a2, a3, labs, true, cur, ar, dot, val, curveS, tag)), run_time=0.6)
