import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from graphs import adjacency, laplacian, normalized_laplacian, parse, symmetry_group


def distinct(x, tol=1e-8):
    x = np.sort(x)
    return np.concatenate([[x[0]], x[1:][np.diff(x) > tol]])


def eig(p, norm=False):
    A = adjacency(p)
    return np.linalg.eigvalsh(normalized_laplacian(A) if norm else laplacian(A))


def test_degrees_examples():
    assert adjacency("N")[parse("a1")].sum() == 2
    assert set(np.flatnonzero(adjacency("N")[parse("a1")])) == {parse("b3"), parse("c2")}
    assert adjacency("R")[parse("a1")].sum() == 14
    d = adjacency("Q").sum(1)
    assert d.min() == 21 and d.max() == 27


def test_rook():
    ev = np.round(eig("R"), 8)
    vals, counts = np.unique(ev, return_counts=True)
    assert list(vals) == [0, 8, 16] and list(counts) == [1, 14, 49]


def test_bishop_two_components():
    assert np.sum(np.abs(eig("B")) < 1e-9) == 2


def test_knight():
    A = adjacency("N")
    w = np.linalg.eigvalsh(normalized_laplacian(A))
    assert abs(w.max() - 2) < 1e-9  # biparti
    assert len(distinct(eig("N"))) == 48


def test_king_formula():
    j = np.arange(1, 9)
    c = 1 + 2 * np.cos(np.pi * j / 9)
    expected = np.sort((np.outer(c, c) - 1).ravel())
    assert np.allclose(np.sort(np.linalg.eigvalsh(adjacency("K"))), expected)
    assert len(distinct(eig("K"))) == 48


def test_queen():
    assert len(distinct(eig("Q"))) == 45


def test_symmetric_and_symmetries():
    for p in "RBNKQP":
        A = adjacency(p)
        assert (A == A.T).all() and A.trace() == 0
    for p in "RBNKQ":
        assert len(symmetry_group(adjacency(p))) == 8
    assert sorted(symmetry_group(adjacency("P"))) == sorted(["e", "r180", "sf", "sr"])
