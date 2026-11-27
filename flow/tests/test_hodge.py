"""Test 4 : Hodge — reconstruction et orthogonalité à la précision machine ; dimensions des sous-espaces."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import numpy as np
from flow import EDGES, KEDGES, Flow, random_game
from hodge import Hodge, block_circulation


def test_dimensions():
    h = Hodge()
    assert len(h.edges) == 210 and len(h.tris) == 196          # 49 blocs 2×2 × 4 triangles
    assert h.dim_cycles == 147 and h.dim_curl == 147 and h.dim_harm == 0   # échiquier « plein » : pas d'harmonique
    assert np.allclose(h.C @ h.B, 0)                           # le bord d'un bord est nul
    hk = Hodge(EDGES + KEDGES)
    # chaque lien cavalier a-b forme un triangle avec deux liens « roi » (ex. g1-g2-f3) : complexe encore plein
    assert len(hk.tris) > 196 and hk.dim_harm == 0


def _check(h, J):
    g, c, r, phi, psi = h.decompose(J)
    scale = np.abs(J).max()
    assert np.abs(g + c + r - J).max() <= 1e-10 * scale                  # reconstruction
    assert abs((g * c).sum()) <= 1e-9 * (J ** 2).sum()                     # orthogonalité
    assert abs((g * r).sum()) <= 1e-9 * (J ** 2).sum() and abs((c * r).sum()) <= 1e-9 * (J ** 2).sum()
    assert np.abs(c @ h.B).max() <= 1e-10 * scale                          # le rotationnel ne diverge pas
    assert np.allclose(g @ h.B, J @ h.B)                                   # toute la divergence est dans le gradient
    assert np.allclose(h.fractions(J).sum(), 1)


def test_random_and_game_fluxes():
    rng = np.random.default_rng(0)
    for edges in (EDGES, EDGES + KEDGES):
        h = Hodge(edges)
        for _ in range(5):
            _check(h, rng.normal(size=len(edges)))
    f = Flow(tmax=200)
    for _ in range(50):
        f.add_game(random_game(rng, 200))
    h = Hodge()
    _check(h, f.J().sum(1)[10].astype(float))


def test_pure_parts():
    h = Hodge()
    phi = np.arange(64.0)
    g, c, r, _, _ = h.decompose(phi @ h.B.T)
    assert np.allclose(c, 0) and np.allclose(r, 0)            # un gradient pur n'a pas de tourbillon
    J = np.zeros(210)
    J = h.C[0]                                                # circulation autour d'un triangle
    g, c, r, _, _ = h.decompose(J)
    assert np.allclose(g, 0) and np.allclose(c, J)
    circ = block_circulation(h.C[0] + 0 * J)
    assert abs(circ.sum()) > 0
