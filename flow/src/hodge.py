"""Décomposition de Hodge du flux sur le graphe (Jiang, Lim, Yao, Ye 2011, « HodgeRank »).

Sur un graphe, tout flux J (un nombre par lien orienté) se décompose de façon unique en trois parties
orthogonales :
    J = B φ        (gradient : l'écoulement « descend » un potentiel φ défini sur les cases)
      + Cᵀ ψ       (rotationnel : circulation autour des faces, ici les triangles de 3 cases voisines)
      + h          (harmonique : circulation autour des « trous » du graphe ; nulle si le complexe est plein)
B (liens × cases) : incidence, (B φ)_e = φ_u − φ_w pour e = (u, w) : le flux va du potentiel haut au bas.
C (faces × liens) : bord des triangles ; C B = 0 (« le bord d'un bord est nul »), d'où l'orthogonalité.
Toute la divergence est portée par la partie gradient : div(Cᵀψ) = Bᵀ Cᵀ ψ = 0.
"""
import numpy as np
import scipy.linalg as sla
from flow import EDGES, KEDGES, incidence


def triangles(edges):
    """Tous les triangles (3-cliques) i < j < k du graphe."""
    adj = {}
    for u, w in edges:
        adj.setdefault(u, set()).add(w)
        adj.setdefault(w, set()).add(u)
    out = []
    for u, w in edges:
        for k in adj[u] & adj[w]:
            if k > w:
                out.append((u, w, k))
    return sorted(out)


def face_matrix(edges, tris):
    """C[f, e] : bord orienté du triangle i -> j -> k -> i."""
    idx = {e: n for n, e in enumerate(edges)}
    C = np.zeros((len(tris), len(edges)))
    for f, (i, j, k) in enumerate(tris):
        C[f, idx[(i, j)]] = 1
        C[f, idx[(j, k)]] = 1
        C[f, idx[(i, k)]] = -1
    return C


class Hodge:
    def __init__(self, edges=EDGES):
        self.edges = list(edges)
        self.B = incidence(self.edges).astype(float)
        self.tris = triangles(self.edges)
        self.C = face_matrix(self.edges, self.tris)
        self.Bp = sla.pinv(self.B)            # φ = B⁺ J  (moindres carrés, potentiel de moyenne nulle)
        self.Cp = sla.pinv(self.C.T)          # ψ = (Cᵀ)⁺ J
        self.Pg = self.B @ self.Bp                  # projecteurs orthogonaux
        self.Pc = self.C.T @ self.Cp
        E, V = self.B.shape
        self.dim_cycles = E - V + 1                 # graphe connexe
        self.dim_curl = int(np.linalg.matrix_rank(self.C))
        self.dim_harm = self.dim_cycles - self.dim_curl

    def decompose(self, J):
        """J[..., E] -> (gradient, rotationnel, harmonique, φ, ψ)."""
        J = np.asarray(J, float)
        phi = J @ self.Bp.T
        psi = J @ self.Cp.T
        g = phi @ self.B.T
        c = psi @ self.C
        return g, c, J - g - c, phi, psi

    def fractions(self, J):
        """Fractions d'énergie ‖·‖² des trois parties (somment à 1)."""
        g, c, h, _, _ = self.decompose(J)
        tot = (np.asarray(J, float) ** 2).sum(-1)
        return np.stack([(g ** 2).sum(-1), (c ** 2).sum(-1), (h ** 2).sum(-1)], -1) / tot[..., None]


def block_circulation(J, edges=EDGES):
    """Tourbillon « carré » : circulation de J autour de chaque bloc 2×2 (sens trigonométrique), carte 7×7.
    C'est l'analogue discret de rot J = ∂x Jy − ∂y Jx au centre du bloc."""
    idx = {e: n for n, e in enumerate(edges)}
    J = np.asarray(J, float)
    out = np.zeros(J.shape[:-1] + (7, 7))
    for r in range(7):
        for f in range(7):
            a, b, c, d = 8 * r + f, 8 * r + f + 1, 8 * (r + 1) + f + 1, 8 * (r + 1) + f   # a1 b1 b2 a2
            circ = J[..., idx[(a, b)]] + J[..., idx[(b, c)]] - J[..., idx[(d, c)]] - J[..., idx[(a, d)]]
            out[..., r, f] = circ
    return out
