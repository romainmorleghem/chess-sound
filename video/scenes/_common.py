"""Imported first by every scene: paths, style, narration, board helpers."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "video"), str(ROOT / "src"), str(ROOT / "data")]
SOUNDS = ROOT / "media" / "sounds"

from common import style  # noqa: E402
style.setup()
from manim import config as _cfg  # noqa: E402
_cfg.disable_caching = True

import numpy as np  # noqa: E402
import chess  # noqa: E402
from manim import (VGroup, Square, Dot, Line, ArcBetweenPoints, Text, Tex, MathTex, Rectangle,  # noqa: E402
                   UpdateFromAlphaFunc, interpolate_color, linear, UP, DOWN, LEFT, RIGHT, ORIGIN, PI)
from common.style import (BG, FG, MUTED, LIGHT_SQ, DARK_SQ, POS, NEG, NODE, BAND, ACCENT,  # noqa: E402,F401
                          PIECE_COLOR, PIECE_NAME, GLYPH, GOOD)
from common.narrative import Narrated, NarratedCamera, PAUSE  # noqa: E402,F401
from graphs import adjacency, laplacian, normalized_laplacian, coords, parse, name as sqname  # noqa: E402,F401
from modes import modes  # noqa: E402,F401


def snd(name):
    return str(SOUNDS / f"{name}.wav")


def mode_color(x):
    """x in [-1, 1] -> blue (−) / white (node) / red (+)."""
    x = float(np.clip(x, -1, 1))
    return interpolate_color(NODE, POS if x > 0 else NEG, abs(x) ** 0.8)


class Board(VGroup):
    """8×8 board, a1 bottom-left. Squares indexed like python-chess (a1=0 … h8=63)."""

    def __init__(self, size=0.72, labels=False):
        super().__init__()
        self.s = size
        self.squares = VGroup()
        for i in range(64):
            f, r = coords(i)
            sq = Square(size, stroke_width=0, fill_opacity=1,
                        fill_color=LIGHT_SQ if (f + r) % 2 else DARK_SQ)
            sq.move_to([(f - 3.5) * size, (r - 3.5) * size, 0])
            self.squares.add(sq)
        self.add(self.squares)
        if labels:
            lab = VGroup()
            for f in range(8):
                lab.add(Text("abcdefgh"[f], font_size=16, color=MUTED).move_to(
                    [(f - 3.5) * size, -4.25 * size, 0]))
            for r in range(8):
                lab.add(Text(str(r + 1), font_size=16, color=MUTED).move_to([-4.25 * size, (r - 3.5) * size, 0]))
            self.labels = lab
            self.add(lab)

    def pos(self, i):
        return self.squares[parse(i) if isinstance(i, str) else i].get_center()

    def paint(self, v, vmax=None):
        vmax = vmax or (np.abs(v).max() + 1e-12)
        for k, sq in enumerate(self.squares):
            sq.set_fill(mode_color(v[k] / vmax))
        return self

    def reset_colors(self):
        for i, sq in enumerate(self.squares):
            f, r = coords(i)
            sq.set_fill(LIGHT_SQ if (f + r) % 2 else DARK_SQ)
        return self

    def vibrate(self, v, cycles=2.0):
        """Animation: squares coloured by v·cos(2π·cycles·α) (a standing wave)."""
        vmax = np.abs(v).max() + 1e-12

        def upd(m, a):
            c = np.cos(2 * np.pi * cycles * a)
            for k, sq in enumerate(m.squares):
                sq.set_fill(mode_color(c * v[k] / vmax))
        return UpdateFromAlphaFunc(self, upd, rate_func=linear)


def glyph(p, white=True, size=None, color=None):
    t = Text(GLYPH[p], font="DejaVu Sans", font_size=size or 40,
             color=color or ("#F4F1EA" if white else "#14161A"))
    if white and color is None:
        t.set_stroke("#14161A", 0.6, background=True)
    elif color is None:
        t.set_stroke("#D8D4CC", 2.2, background=True)
    return t


def bands(board, piece, sources=None, color=BAND, width=2.0, opacity=0.8):
    """Rubber bands of `piece` from the given squares (default: all edges, once)."""
    A = adjacency(piece)
    g = VGroup()
    src = range(64) if sources is None else [parse(s) if isinstance(s, str) else s for s in sources]
    for i in src:
        for j in np.flatnonzero(A[i]):
            if sources is None and j < i:
                continue
            p, q = board.pos(i), board.pos(int(j))
            fi, ri = coords(i)
            fj, rj = coords(int(j))
            straight = piece in "NKP" or max(abs(fi - fj), abs(ri - rj)) == 1
            m = Line(p, q) if straight else ArcBetweenPoints(p, q, angle=0.35)
            g.add(m.set_stroke(color, width, opacity))
    return g


def beads(board, r=0.07, color=FG):
    return VGroup(*[Dot(board.pos(i), radius=r, color=color) for i in range(64)])


LETTER = {chess.PAWN: "P", chess.KNIGHT: "N", chess.BISHOP: "B", chess.ROOK: "R",
          chess.QUEEN: "Q", chess.KING: "K"}


class GameBoard(VGroup):
    """Board + pieces; `play(moves, step)` returns ONE animation driven by the clock, so the
    pieces stay in sync with the melody (note k sounds at k*step; the piece lands at k*step)."""

    def __init__(self, size=0.72):
        super().__init__()
        self.board = Board(size, labels=True)
        self.hl_from = Square(size, stroke_width=0, fill_color=BAND, fill_opacity=0).move_to(self.board.pos(0))
        self.hl_to = Square(size, stroke_width=0, fill_color=BAND, fill_opacity=0).move_to(self.board.pos(0))
        self.add(self.board, self.hl_from, self.hl_to)
        self.b = chess.Board()
        self.pieces = {}
        for sq, pc in self.b.piece_map().items():
            g = glyph(LETTER[pc.piece_type], pc.color, size=int(56 * size)).move_to(self.board.pos(sq))
            self.pieces[sq] = g
            self.add(g)
        self.caption = Text(" ", font_size=26, color=FG)

    def play(self, sans, step, lead=0.18):
        """Animation of length len(sans)*step + 1; returns (animation, run_time)."""
        b = chess.Board()
        owner = dict(self.pieces)          # square -> glyph
        tracks = {id(g): [] for g in self.pieces.values()}   # (t_end, p0, p1)
        death = {}
        marks = []
        for k, san in enumerate(sans):
            mv = b.parse_san(san)
            t = k * step
            g = owner.pop(mv.from_square)
            if b.is_en_passant(mv):
                cap_sq = mv.to_square + (-8 if b.turn else 8)
            else:
                cap_sq = mv.to_square
            if cap_sq in owner:
                death[id(owner.pop(cap_sq))] = t
            tracks[id(g)].append((t, self.board.pos(mv.from_square), self.board.pos(mv.to_square)))
            owner[mv.to_square] = g
            if b.is_castling(mv):
                rank = 0 if b.turn else 7
                rf, rt = (7, 5) if mv.to_square > mv.from_square else (0, 3)
                rg = owner.pop(chess.square(rf, rank))
                tracks[id(rg)].append((t, self.board.pos(chess.square(rf, rank)), self.board.pos(chess.square(rt, rank))))
                owner[chess.square(rt, rank)] = rg
            assert not mv.promotion, "promotion not drawn"
            marks.append((t, mv.from_square, mv.to_square))
            b.push(mv)
        glyphs = {id(g): g for g in self.pieces.values()}
        start = {id(g): g.get_center().copy() for g in self.pieces.values()}
        T = len(sans) * step + 1.0 + lead

        def upd(m, a):
            t = a * T - lead
            for gid, g in glyphs.items():
                p = start[gid]
                for te, p0, p1 in tracks[gid]:
                    if t >= te:
                        p = p1
                    elif t > te - lead:
                        x = (t - te + lead) / lead
                        x = x * x * (3 - 2 * x)
                        p = p0 + (p1 - p0) * x
                        break
                    else:
                        break
                g.move_to(p)
                d = death.get(gid)
                g.set_opacity(1.0 if d is None or t < d else max(0.0, 1 - (t - d) / 0.15))
            cur = [mk for mk in marks if mk[0] - lead <= t]
            if cur:
                _, f0, f1 = cur[-1]
                self.hl_from.move_to(self.board.pos(f0)).set_fill(opacity=0.25)
                self.hl_to.move_to(self.board.pos(f1)).set_fill(opacity=0.45)
        return UpdateFromAlphaFunc(self, upd, rate_func=linear), T, lead


class Spectrum(VGroup):
    """Log-frequency axis (100–1300 Hz) with vertical lines."""

    def __init__(self, width=10.0, fmin=100, fmax=1300):
        super().__init__()
        self.w, self.fmin, self.fmax = width, fmin, fmax
        self.axis = Line(LEFT * width / 2, RIGHT * width / 2, color=MUTED, stroke_width=2)
        self.add(self.axis)
        self.ticks = VGroup()
        for f in (110, 220, 440, 880):
            x = self.x(f)
            self.ticks.add(Line([x, -0.08, 0], [x, 0.08, 0], color=MUTED, stroke_width=2),
                           Text(f"{f} Hz", font_size=16, color=MUTED).move_to([x, -0.3, 0]))
        self.add(self.ticks)

    def x(self, f):
        return (np.log(f / self.fmin) / np.log(self.fmax / self.fmin) - 0.5) * self.w

    def lines(self, freqs, amps=None, y0=0.0, h=0.8, color=FG, width=3):
        amps = np.ones(len(freqs)) if amps is None else np.asarray(amps) / max(np.max(amps), 1e-12)
        g = VGroup()
        for f, a in zip(freqs, amps):
            if f <= 0 or a < 1e-3:
                continue
            x = self.x(f)
            g.add(Line([x, y0, 0], [x, y0 + h * a, 0], color=color, stroke_width=width))
        return g.shift([self.axis.get_center()[0], 0, 0])


def ring(pos, color=BAND, run_time=1.6):
    """Expanding circle: 'this square was struck'."""
    from manim import Circle, Create  # noqa: F401
    c = Circle(radius=0.15, color=color, stroke_width=4).move_to(pos)
    return c.animate(run_time=run_time, rate_func=linear).scale(9).set_stroke(opacity=0)


def strike(scene, sound, pos=None, dur=2.2, color=BAND, also=()):
    """Play a sound (with a ring on `pos`) and wait for it to ring out."""
    scene.add_sound(snd(sound))
    anims = list(also)
    if pos is not None:
        from manim import Circle
        c = Circle(radius=0.15, color=color, stroke_width=4).move_to(pos)
        scene.add(c)
        anims.append(c.animate(rate_func=linear).scale(9).set_stroke(opacity=0))
    if anims:
        scene.play(*anims, run_time=dur)
        if pos is not None:
            scene.remove(c)
    else:
        scene.wait(dur)
