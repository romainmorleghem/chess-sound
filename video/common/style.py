"""Visual identity (same dark look as Ising / Routes to Chaos)."""
from manim import config, TexTemplate, ManimColor

BG = ManimColor("#0E1116")
FG = ManimColor("#E6E6E6")
MUTED = ManimColor("#7A8291")
GRID = ManimColor("#262D38")

LIGHT_SQ = ManimColor("#3A4252")   # board, light squares
DARK_SQ = ManimColor("#232A35")    # board, dark squares
POS = ManimColor("#E4572E")        # mode amplitude > 0 (red)
NEG = ManimColor("#3F7FC8")        # mode amplitude < 0 (blue)
NODE = ManimColor("#F2F2F2")       # node (white)
BAND = ManimColor("#F2B544")       # rubber bands
ACCENT = ManimColor("#C792EA")
GOOD = ManimColor("#6CCB8B")

# one colour per instrument (same order as src/graphs.PIECES)
PIECE_COLOR = {"R": ManimColor("#4C9BE8"), "B": ManimColor("#F2B544"), "N": ManimColor("#6CCB8B"),
               "K": ManimColor("#E85D75"), "Q": ManimColor("#C792EA"), "P": ManimColor("#FF8A4C")}
PIECE_NAME = {"R": "rook", "B": "bishop", "N": "knight", "K": "king", "Q": "queen", "P": "pawn"}
GLYPH = {"K": "♚", "Q": "♛", "R": "♜", "B": "♝", "N": "♞", "P": "♟"}

TEX = TexTemplate()
TEX.add_to_preamble(r"\usepackage{amsmath,amssymb}")


def setup():
    config.background_color = BG
    config.tex_template = TEX
