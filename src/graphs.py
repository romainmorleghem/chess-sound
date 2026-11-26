"""Graphes de déplacement des pièces d'échecs sur l'échiquier vide.

Convention des cases : index = 8*rang + colonne (a1=0, b1=1, ..., h1=7, a2=8, ..., h8=63),
identique à python-chess.
"""
import numpy as np

N = 8
FILES = "abcdefgh"
PIECES = ["R", "B", "N", "K", "Q", "P"]
NAMES_FR = {"R": "Tour", "B": "Fou", "N": "Cavalier", "K": "Roi", "Q": "Dame", "P": "Pion"}


def sq(f, r):
    return 8 * r + f


def coords(i):
    return i % 8, i // 8


def name(i):
    f, r = coords(i)
    return f"{FILES[f]}{r + 1}"


def parse(s):
    return sq(FILES.index(s[0]), int(s[1]) - 1)


def _inside(f, r):
    return 0 <= f < N and 0 <= r < N


ORTHO = [(1, 0), (-1, 0), (0, 1), (0, -1)]
DIAG = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
KNIGHT = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]


def _slider(dirs):
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        f, r = coords(i)
        for df, dr in dirs:
            g, s = f + df, r + dr
            while _inside(g, s):
                A[i, sq(g, s)] = 1
                g, s = g + df, s + dr
    return A


def _stepper(dirs):
    A = np.zeros((64, 64), dtype=int)
    for i in range(64):
        f, r = coords(i)
        for df, dr in dirs:
            if _inside(f + df, r + dr):
                A[i, sq(f + df, r + dr)] = 1
    return A


def _pawn():
    """Pion : graphe symétrisé (convention choisie).

    Arêtes = union des coups des pions blancs et noirs : poussée d'une case,
    double poussée depuis la case de départ, prises en diagonale vers l'avant
    (comptées comme si une pièce adverse était là). On oublie le sens (l'arête
    a2-a3 relie a2 et a3 dans les deux sens).
    """
    A = np.zeros((64, 64), dtype=int)

    def add(a, b):
        A[a, b] = A[b, a] = 1

    for color, fwd, start in ((0, 1, 1), (1, -1, 6)):
        for r in range(1, 7):  # un pion n'est jamais sur sa 1re rangée
            for f in range(8):
                i = sq(f, r)
                add(i, sq(f, r + fwd))
                if r == start:
                    add(i, sq(f, r + 2 * fwd))
                for df in (-1, 1):
                    if _inside(f + df, r + fwd):
                        add(i, sq(f + df, r + fwd))
    return A


def adjacency(piece):
    piece = piece.upper()
    if piece == "R":
        return _slider(ORTHO)
    if piece == "B":
        return _slider(DIAG)
    if piece == "Q":
        return _slider(ORTHO + DIAG)
    if piece == "N":
        return _stepper(KNIGHT)
    if piece == "K":
        return _stepper(ORTHO + DIAG)
    if piece == "P":
        return _pawn()
    raise ValueError(piece)


def laplacian(A):
    return np.diag(A.sum(1)) - A


def normalized_laplacian(A):
    d = A.sum(1).astype(float)
    dinv = np.where(d > 0, 1 / np.sqrt(np.maximum(d, 1e-300)), 0.0)
    return np.eye(len(A)) - dinv[:, None] * A * dinv[None, :]


# --- Symétries de l'échiquier (groupe D4) -----------------------------------
# chaque élément = fonction (f, r) -> (f', r')
D4 = {
    "e": lambda f, r: (f, r),
    "r90": lambda f, r: (7 - r, f),
    "r180": lambda f, r: (7 - f, 7 - r),
    "r270": lambda f, r: (r, 7 - f),
    "sf": lambda f, r: (7 - f, r),       # miroir colonnes (a<->h)
    "sr": lambda f, r: (f, 7 - r),       # miroir rangées (1<->8)
    "sd": lambda f, r: (r, f),           # diagonale a1-h8
    "sa": lambda f, r: (7 - r, 7 - f),   # diagonale a8-h1
}
D4_CLASS = {"e": 0, "r90": 1, "r270": 1, "r180": 2, "sf": 3, "sr": 3, "sd": 4, "sa": 4}
# table des caractères de D4 (classes : e, rot±90, rot180, miroirs axiaux, miroirs diagonaux)
D4_IRREPS = {
    "A1": (1, 1, 1, 1, 1),
    "A2": (1, 1, 1, -1, -1),
    "B1": (1, -1, 1, 1, -1),
    "B2": (1, -1, 1, -1, 1),
    "E": (2, 0, -2, 0, 0),
}


def perm_matrix(g):
    P = np.zeros((64, 64))
    for i in range(64):
        P[sq(*D4[g](*coords(i))), i] = 1
    return P


def symmetry_group(A):
    """Éléments de D4 qui préservent le graphe."""
    out = []
    for g in D4:
        P = perm_matrix(g)
        if np.array_equal(P @ A @ P.T, A):
            out.append(g)
    return out
