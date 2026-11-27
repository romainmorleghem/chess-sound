"""Socle commun des scènes chess-flow : chemins, style et voix de chess-sound, échiquier et champs."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]          # dépôt chess-sound
FLOW = ROOT / "flow"
sys.path[:0] = [str(ROOT / "video"), str(FLOW / "src")]
from common import style  # noqa: E402
style.setup()
from manim import config as _cfg  # noqa: E402
_cfg.disable_caching = True

import numpy as np  # noqa: E402
from manim import (VGroup, Square, Line, Arrow, Text, Tex, MathTex, Dot, RoundedRectangle, UpdateFromAlphaFunc,  # noqa: E402,F401
                   interpolate_color, linear, ManimColor, UP, DOWN, LEFT, RIGHT, ORIGIN, PI)
from common.style import BG, FG, MUTED, BAND, ACCENT, GOOD  # noqa: E402,F401
from common.narrative import Narrated, PAUSE  # noqa: E402,F401
from flow import EDGES  # noqa: E402

DATA = np.load(FLOW / "video" / "data.npz")
RED, BLUE, GOLD = ManimColor("#E4572E"), ManimColor("#3F7FC8"), ManimColor("#F2B544")
MID = ManimColor("#2A303A")
SEQ0 = ManimColor("#151A22")
LIGHT_SQ, DARK_SQ = ManimColor("#3A4252"), ManimColor("#232A35")


def col_div(x):
    x = float(np.clip(x, -1, 1))
    return interpolate_color(MID, RED if x > 0 else BLUE, abs(x) ** 0.7)


def col_seq(x):
    x = float(np.clip(x, 0, 1))
    if x < 0.6:
        return interpolate_color(SEQ0, GOLD, x / 0.6)
    return interpolate_color(GOLD, ManimColor("#FFF1C9"), (x - 0.6) / 0.4)


class Board(VGroup):
    """8×8, a1 en bas à gauche (index python-chess)."""

    def __init__(self, size=0.6, labels=False):
        super().__init__()
        self.s = size
        self.frame = RoundedRectangle(corner_radius=0.05, width=8 * size + 0.14, height=8 * size + 0.14,
                                      stroke_color=MUTED, stroke_width=2, stroke_opacity=0.6)
        self.squares = VGroup()
        for i in range(64):
            f, r = i % 8, i // 8
            sq = Square(size, stroke_width=0, fill_opacity=1, fill_color=LIGHT_SQ if (f + r) % 2 else DARK_SQ)
            sq.move_to([(f - 3.5) * size, (r - 3.5) * size, 0])
            self.squares.add(sq)
        self.add(self.frame, self.squares)
        if labels:
            for f in range(8):
                self.add(Text("abcdefgh"[f], font_size=14, color=MUTED).move_to([(f - 3.5) * size, -4.3 * size, 0]))
            for r in range(8):
                self.add(Text(str(r + 1), font_size=14, color=MUTED).move_to([-4.3 * size, (r - 3.5) * size, 0]))

    def pos(self, i):
        if isinstance(i, str):
            i = "abcdefgh".index(i[0]) + 8 * (int(i[1]) - 1)
        return self.squares[i].get_center()

    def paint(self, v, kind="seq", vmax=None):
        v = np.asarray(v, float).ravel()
        if kind == "seq":
            vmax = vmax or v.max() or 1
            for k, sq in enumerate(self.squares):
                sq.set_fill(col_seq(v[k] / vmax))
        else:
            vmax = vmax or np.abs(v).max() or 1
            for k, sq in enumerate(self.squares):
                sq.set_fill(col_div(v[k] / vmax))
        return self

    def plain(self):
        for i, sq in enumerate(self.squares):
            sq.set_fill(LIGHT_SQ if (i % 8 + i // 8) % 2 else DARK_SQ)
        return self


def square_arrows(board, V, vmax=None, color=FG, maxlen=0.9):
    """Une flèche par case (vecteur V[64, 2] en cases)."""
    V = np.asarray(V, float)
    vmax = vmax or np.linalg.norm(V, axis=1).max() or 1
    g = VGroup()
    for i in range(64):
        n = np.linalg.norm(V[i])
        if n / vmax < 0.08:
            continue
        d = np.array([V[i, 0], V[i, 1], 0]) / n
        L = maxlen * board.s * min(n / vmax, 1)
        c = board.pos(i)
        g.add(Arrow(c - d * L / 2, c + d * L / 2, buff=0, color=color, stroke_width=3,
                    max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=12))
    return g


def edge_arrows(board, J, vmax=None, color=FG, maxlen=0.75, thresh=0.06):
    """Flux net sur les liens : une flèche au milieu de chaque lien, dans le sens du flux, longueur ∝ |J|."""
    J = np.asarray(J, float)
    vmax = vmax or np.abs(J).max() or 1
    g = VGroup()
    for k, (u, w) in enumerate(EDGES):
        a = abs(J[k]) / vmax
        if a < thresh:
            continue
        p, q = board.pos(u), board.pos(w)
        d = (q - p) / np.linalg.norm(q - p) * (1 if J[k] > 0 else -1)
        m = (p + q) / 2
        L = maxlen * board.s * min(a, 1)
        g.add(Arrow(m - d * L / 2, m + d * L / 2, buff=0, color=color, stroke_width=2.5,
                    max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=14))
    return g


def links(board, opacity=0.25):
    return VGroup(*[Line(board.pos(u), board.pos(w), color=MUTED, stroke_width=1, stroke_opacity=opacity)
                    for u, w in EDGES])


def edge_vectors(J):
    V = np.zeros((64, 2))
    for k, (u, w) in enumerate(EDGES):
        d = np.array([w % 8 - u % 8, w // 8 - u // 8], float); d /= np.linalg.norm(d)
        V[u] += 0.5 * J[k] * d; V[w] += 0.5 * J[k] * d
    return V
