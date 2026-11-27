"""Outils de la pièce artistique : champ continu (interpolation décorative) et lignes de courant « à la 3b1b »."""
from fc import np, FLOW, ManimColor
from manim import StreamLines, ArrowVectorField, VGroup, Square, RoundedRectangle
from scipy.interpolate import RectBivariateSpline

ART = np.load(FLOW / "video" / "art.npz")
PALETTE = [ManimColor(c) for c in ("#2E3A8C", "#3F7FC8", "#3FC8B4", "#9BE07A", "#F2B544", "#E4572E")]
SIZE = 0.82                      # taille d'une case (unités manim)


def field(V, size=SIZE, center=np.zeros(3), scale=1.0, gamma=0.5):
    """V[64, 2] aux cases -> fonction continue p -> vecteur (spline bicubique ; décoratif).
    Vitesses compressées : |v| -> |v|^gamma (direction conservée) pour que tout l'échiquier « coule »."""
    g = np.arange(8.0)
    U = RectBivariateSpline(g, g, V[:, 0].reshape(8, 8))      # [rang, colonne]
    W_ = RectBivariateSpline(g, g, V[:, 1].reshape(8, 8))

    def f(p):
        x = (p[0] - center[0]) / size + 3.5
        y = (p[1] - center[1]) / size + 3.5
        x, y = min(max(x, 0), 7), min(max(y, 0), 7)
        v = np.array([U(y, x)[0, 0], W_(y, x)[0, 0], 0.0]) * scale
        n = np.linalg.norm(v)
        return v * (n ** (gamma - 1)) if n > 1e-9 else v
    return f


def stream(V, vmax, size=SIZE, center=np.zeros(3), density=0.17, width=2.4, scale=None):
    """Lignes de courant sur l'échiquier ; couleur = vitesse (même échelle vmax pour comparer)."""
    scale = scale or 1.0 / vmax
    half = 4 * size
    return StreamLines(field(V, size, center, scale), x_range=[center[0] - half, center[0] + half, density],
                       y_range=[center[1] - half, center[1] + half, density], colors=PALETTE,
                       min_color_scheme_value=0.0, max_color_scheme_value=1.0, stroke_width=width,
                       virtual_time=3.0, max_anchors_per_line=60, padding=0.3, n_repeats=1, noise_factor=density / 2)


def arrows(V, vmax, size=SIZE, center=np.zeros(3), step=0.41):
    half = 4 * size - step / 2
    return ArrowVectorField(field(V, size, center, 1.0 / vmax), x_range=[center[0] - half, center[0] + half, step],
                            y_range=[center[1] - half, center[1] + half, step], colors=PALETTE,
                            min_color_scheme_value=0.0, max_color_scheme_value=1.0, length_func=lambda n: 0.38 * min(n, 1.2))


def ghost_board(size=SIZE, center=np.zeros(3), opacity=0.18):
    g = VGroup()
    for i in range(64):
        f, r = i % 8, i // 8
        if (f + r) % 2:
            g.add(Square(size, stroke_width=0, fill_color="#8A93A6", fill_opacity=opacity * 0.5).move_to(
                center + np.array([(f - 3.5) * size, (r - 3.5) * size, 0])))
    g.add(RoundedRectangle(corner_radius=0.05, width=8 * size + 0.1, height=8 * size + 0.1, stroke_color="#8A93A6",
                           stroke_width=1.5, stroke_opacity=opacity * 2).move_to(center))
    return g


def vmax_of(keys):
    return max(np.linalg.norm(ART[k], axis=1).max() for k in keys)
