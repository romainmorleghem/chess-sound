"""Tests 1 à 3 du cahier des charges : mini-parties calculées à la main, continuité exacte, conservation."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
import chess
import pytest
from flow import Flow, EIDX, KIDX, W, san_moves, random_game, species

sq = chess.parse_square
WP, WN, WR, WQ, WK = (species(chess.WHITE, p) for p in (1, 2, 4, 5, 6))
BP, BR = species(chess.BLACK, 1), species(chess.BLACK, 4)


def run(text, fen=chess.STARTING_FEN, **kw):
    f = Flow(tmax=20, **kw)
    f.add_game(san_moves(text, fen), start_fen=fen)
    return f


def step(f, t, s, a, b):
    """Nombre de pas (unités W) de la case a vers la case b au demi-coup t."""
    x, y = sq(a), sq(b)
    e = EIDX[(min(x, y), max(x, y))]
    return f.F[t, s, e, 0 if x < y else 1]


# ---------- test 1 : mini-parties, résultat attendu à la main ----------
def test_simple_push():
    f = run("1.e4")
    assert step(f, 0, WP, "e2", "e3") == W and step(f, 0, WP, "e3", "e4") == W
    d = f.div()[0, WP]
    assert d[sq("e2")] == W and d[sq("e3")] == 0 and d[sq("e4")] == -W   # source du flux en e2, puits en e4
    assert f.S[1, WP, sq("e4")] == W and f.S[1, WP, sq("e2")] == 0


def test_capture():
    f = run("1.e4 d5 2.exd5")
    assert step(f, 2, WP, "e4", "d5") == W
    assert f.snk[2, BP, sq("d5")] == W and f.snk[2].sum() == W


def test_en_passant():
    f = run("1.e4 a6 2.e5 d5 3.exd6")
    assert step(f, 4, WP, "e5", "d6") == W
    assert f.snk[4, BP, sq("d5")] == W and f.snk[4, BP, sq("d6")] == 0   # puits sur la case du pion pris


def test_short_castle():
    f = run("1.e4 e5 2.Nf3 Nc6 3.Bc4 Bc5 4.O-O")
    assert step(f, 6, WK, "e1", "f1") == W and step(f, 6, WK, "f1", "g1") == W
    assert step(f, 6, WR, "h1", "g1") == W and step(f, 6, WR, "g1", "f1") == W
    assert f.S[7, WK, sq("g1")] == W and f.S[7, WR, sq("f1")] == W


def test_long_castle():
    f = run("1.d4 d5 2.Nc3 Nc6 3.Bf4 Bf5 4.Qd2 Qd7 5.O-O-O")
    for a, b in (("e1", "d1"), ("d1", "c1")):
        assert step(f, 8, WK, a, b) == W
    for a, b in (("a1", "b1"), ("b1", "c1"), ("c1", "d1")):
        assert step(f, 8, WR, a, b) == W
    J = f.J()[8].sum(0)                      # toutes espèces : roi et tour se croisent sur c1-d1
    assert J[EIDX[(sq("c1"), sq("d1"))]] == 0


def test_promotion_with_capture():
    fen = "r3k3/1P6/8/8/8/8/8/4K3 w - - 0 1"
    f = run("1.bxa8=Q", fen)
    assert step(f, 0, WP, "b7", "a8") == W
    assert f.snk[0, WP, sq("a8")] == W and f.src[0, WQ, sq("a8")] == W and f.snk[0, BR, sq("a8")] == W
    assert f.S[1, WQ, sq("a8")] == W and f.S[1, WP].sum() == 0 and f.S[1, BR].sum() == 0


def test_knight_two_L_paths():
    f = run("1.Nf3")
    long_first = [("g1", "g2"), ("g2", "g3"), ("g3", "f3")]
    short_first = [("g1", "f1"), ("f1", "f2"), ("f2", "f3")]
    for a, b in long_first + short_first:
        assert step(f, 0, WN, a, b) == W // 2          # chaque chemin en L pèse 1/2
    d = f.div()[0, WN]
    assert d[sq("g1")] == W and d[sq("f3")] == -W and d[sq("g2")] == 0 and d[sq("f2")] == 0
    g = run("1.Nf3", knight="direct")
    assert g.FK[0, WN, KIDX[(sq("g1"), sq("f3"))], 0] == W and g.F[0, WN].sum() == 0


def test_mine_frame_flips_black():
    f = run("1.e4 e5", frame="mine")
    P = species(chess.BLACK, chess.PAWN, "mine")
    assert step(f, 1, P, "e2", "e3") == W and step(f, 1, P, "e3", "e4") == W   # ...e5 vu par les Noirs = e2-e4
    assert f.D[1, P, sq("e2"), 1] == 2 * W                                    # composante verticale : +2


# ---------- tests 2 et 3 : continuité exacte et conservation, sur des parties aléatoires ----------
@pytest.mark.parametrize("frame", ["abs", "mine"])
@pytest.mark.parametrize("knight", ["L", "direct"])
def test_continuity_and_conservation(frame, knight):
    rng = np.random.default_rng(1)
    f = Flow(tmax=400, frame=frame, knight=knight)
    flags = dict(ep=0, castle=0, promo=0)
    final_pieces = 0
    for k in range(150):
        moves = random_game(rng, 400)
        b = chess.Board()
        for m in moves:
            flags["ep"] += b.is_en_passant(m); flags["castle"] += b.is_castling(m); flags["promo"] += bool(m.promotion)
            b.push(m)
        final_pieces += len(b.piece_map()) * W
        if k < 10:                                            # partie par partie
            g = Flow(tmax=400, frame=frame, knight=knight)
            g.add_game(moves)
            assert not np.any(g.residual())
        f.add_game(moves)
    assert all(v > 0 for v in flags.values()), flags          # les cas spéciaux sont bien couverts
    assert not np.any(f.residual())                          # test 2 : continuité, en entiers, agrégée
    alive = f.N > 0
    assert np.array_equal(f.S.sum((1, 2))[alive], f.NP[alive])  # test 3 : Σρ = pièces restantes (32 - prises)
    assert f.exit.sum() == final_pieces                      # sortie de l'ensemble = pièces en fin de partie
