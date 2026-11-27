"""Résumé compact par partie -> sommes pondérées (centrale, ECO, moitiés, bootstrap de Poisson).

Chaque partie g donne un vecteur x_g ; les indicateurs sont des fonctions (non linéaires) de sommes Σ_g w_g x_g.
Bootstrap SUR LES PARTIES : w_g ~ Poisson(1), R tirages (équivalent asymptotique du tirage avec remise).
Blocs de x_g :
  Jt [TA, E]   flux net toutes espèces, par demi-coup t < TA (indicateur 1)
  At [TA]      parties vivantes (transition t existe : t < T_g)
  Jw [4, E]    flux net par fenêtre (indicateur 2, Hodge)      Nw [4] transitions dans la fenêtre
  Sw [4, 64]   pièces présentes avant chaque transition ; Dw [4, 64, 2] déplacements ; D2w [4, 64] carrés (indicateur 3)
  Kw [4, 64]   prises (puits de capture, hors promotion) (indicateur 4)
  Zw [4, 15, 15] départs − arrivées du camp au trait, relatifs au roi adverse, « vers l'avant » = vers lui (indicateur 5)
"""
import numpy as np
import chess
from flow import EIDX, W, game_record

TA = 120
WINDOWS = [(0, 10), (10, 30), (30, 60), (60, 10 ** 6)]
E = len(EIDX)
BLOCKS = [("Jt", (TA, E)), ("At", (TA,)), ("Jw", (4, E)), ("Nw", (4,)), ("Sw", (4, 64)), ("Dw", (4, 64, 2)),
          ("D2w", (4, 64)), ("Kw", (4, 64)), ("Zw", (4, 15, 15))]
OFF, DIM = {}, 0
for name, shape in BLOCKS:
    OFF[name] = (DIM, shape)
    DIM += int(np.prod(shape))


def win(t):
    for k, (a, b) in enumerate(WINDOWS):
        if a <= t < b:
            return k
    return None


def view(v, name):
    o, shape = OFF[name]
    return v[..., o:o + int(np.prod(shape))].reshape(v.shape[:-1] + shape)


def reduce_record(rec, out=None):
    x = np.zeros(DIM, np.float32) if out is None else out
    T = rec["T"]
    Jt, At, Jw, Nw = view(x, "Jt"), view(x, "At"), view(x, "Jw"), view(x, "Nw")
    Sw, Dw, D2w, Kw, Zw = view(x, "Sw"), view(x, "Dw"), view(x, "D2w"), view(x, "Kw"), view(x, "Zw")
    At[:min(T, TA)] = 1
    for t in range(T):
        Nw[win(t)] += 1
    for t, c, p, a, b, w in rec["steps"] + rec["knL"]:
        e = EIDX[(min(a, b), max(a, b))]
        s = w if a < b else -w
        if t < TA:
            Jt[t, e] += s
        Jw[win(t), e] += s
    kings = {}
    for t, c, p, sq in rec["occ"]:
        if t < T:
            Sw[win(t), sq] += W
        if p == chess.KING:
            kings[(t, c)] = sq
    for t, c, p, a, b in rec["disp"]:
        k = win(t)
        df, dr = b % 8 - a % 8, b // 8 - a // 8
        Dw[k, a, 0] += W * df; Dw[k, a, 1] += W * dr; D2w[k, a] += W * (df * df + dr * dr)
        ek = kings[(t, not c)]
        sgn = 1 if c == chess.WHITE else -1          # « vers l'avant » = vers le camp adverse
        for sq, v in ((a, 1), (b, -1)):
            rf = (sq % 8 - ek % 8) * sgn + 7
            rr = (sq // 8 - ek // 8) * sgn + 7
            Zw[k, rr, rf] += W * v
    for t, c, p, sq, w in rec["snk"]:
        mover = chess.WHITE if t % 2 == 0 else chess.BLACK
        if c != mover:                                  # prise (la promotion retire un pion du camp au trait)
            Kw[win(t), sq] += w
    return x
