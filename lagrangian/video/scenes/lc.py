"""Socle commun : chemins, style et voix (réutilise video/common de chess-sound), petits objets physiques."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "video"))
from common import style  # noqa: E402
style.setup()
from manim import config as _cfg  # noqa: E402
_cfg.disable_caching = True

import numpy as np  # noqa: E402
from scipy.integrate import solve_ivp  # noqa: E402,F401
from manim import (VGroup, Dot, Line, Arrow, Circle, Text, Tex, MathTex, Axes, DashedLine, ManimColor,  # noqa: E402,F401
                   UP, DOWN, LEFT, RIGHT, ORIGIN, PI)
from common.style import BG, FG, MUTED, BAND, ACCENT, GOOD, POS, NEG  # noqa: E402,F401
from common.narrative import Narrated, NarratedCamera, PAUSE  # noqa: E402,F401

GOLD, RED, BLUE, GREEN, PURPLE = BAND, POS, NEG, GOOD, ACCENT
TEAL = ManimColor("#3FC8B4")


def ball(color=GOLD, r=0.13):
    return Dot(radius=r, color=color).set_z_index(3)


def ceiling(width=2.2, at=ORIGIN):
    base = Line(LEFT * width / 2, RIGHT * width / 2, color=MUTED, stroke_width=3).move_to(at)
    hatch = VGroup(*[Line(ORIGIN, 0.18 * (UP + RIGHT), color=MUTED, stroke_width=2).move_to(base.point_from_proportion(k / 10) + 0.09 * UP)
                     for k in range(11)])
    return VGroup(base, hatch)


def pendulum_sol(theta0=1.0, g=9.81, l=1.0, T=10.0, n=1200):
    s = solve_ivp(lambda t, y: [y[1], -g / l * np.sin(y[0])], (0, T), [theta0, 0.0], t_eval=np.linspace(0, T, n),
                  rtol=1e-9, atol=1e-11)
    return s.t, s.y[0], s.y[1]

# prononciation (Kokoro / espeak) : g doux de « Lagrangian », Lagrange à la française, Noether
from common import narrative as _nar  # noqa: E402
_nar.PRONOUNCE.update({r"\bLagrangians\b": "Lagranjians", r"\bLagrangian\b": "Lagranjian",
                       r"\bLagrange\b": "Lagrahnj", r"\bNoether\b": "Nerter"})
