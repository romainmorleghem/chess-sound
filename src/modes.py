"""Modes propres des pièces + base adaptée aux symétries (D4) pour les modes dégénérés."""
import numpy as np
from graphs import (adjacency, laplacian, normalized_laplacian, perm_matrix, symmetry_group,
                    D4_CLASS, D4_IRREPS, coords, PIECES, NAMES_FR)

TOL = 1e-7


def irrep_projectors(group):
    """Projecteurs sur les composantes isotypiques (D4 complet ou sous-groupe de Klein)."""
    mats = {g: perm_matrix(g) for g in group}
    if len(group) == 8:
        return {name: (chi[0] / 8) * sum(chi[D4_CLASS[g]] * mats[g] for g in group)
                for name, chi in D4_IRREPS.items()}
    # sous-groupe {e, r180, sf, sr} (pion) : 4 caractères (signe sous sf, signe sous sr)
    out = {}
    for a in (1, -1):
        for b in (1, -1):
            chi = {"e": 1, "sf": a, "sr": b, "r180": a * b}
            out[f"({'+' if a > 0 else '-'}{'+' if b > 0 else '-'})"] = sum(chi[g] * mats[g] for g in group) / 4
    return out


def levels(w, tol=TOL):
    """Regroupe les valeurs propres triées en niveaux (indices de début/fin)."""
    groups, start = [], 0
    for k in range(1, len(w) + 1):
        if k == len(w) or w[k] - w[k - 1] > tol:
            groups.append((start, k))
            start = k
    return groups


def modes(piece, norm=False):
    """Retourne (valeurs propres, vecteurs propres en colonnes, étiquettes de symétrie).

    Dans chaque niveau dégénéré, on diagonalise simultanément des opérateurs qui
    commutent avec L : projecteurs des représentations irréductibles, miroirs a<->h
    et 1<->8, et une pondération radiale invariante (pour départager le reste).
    Chaque mode est alors pair ou impair sous les miroirs, et appartient à une seule
    représentation de D4.
    """
    A = adjacency(piece)
    L = normalized_laplacian(A) if norm else laplacian(A)
    w, V = np.linalg.eigh(L)
    group = symmetry_group(A)
    proj = irrep_projectors(group)
    Rf, Rr = perm_matrix("sf"), perm_matrix("sr")
    fr = np.array([coords(i) for i in range(64)], float) - 3.5
    radial = np.diag((fr ** 2).sum(1) / (2 * 3.5 ** 2))  # 0 au centre, 1 aux coins
    names = list(proj)
    X = sum(10 * (k + 1) * proj[n] for k, n in enumerate(names)) + Rf + 0.5 * Rr + 0.1 * radial
    labels = [None] * 64
    for a, b in levels(w):
        U = V[:, a:b]
        m, Q = np.linalg.eigh(U.T @ X @ U)
        U = U @ Q
        for j in range(b - a):
            u = U[:, j]
            k = int(np.argmax([u @ proj[n] @ u for n in names]))
            pf = int(np.sign(np.round(u @ Rf @ u, 6))) if abs(u @ Rf @ u) > 0.5 else 0
            pr = int(np.sign(np.round(u @ Rr @ u, 6))) if abs(u @ Rr @ u) > 0.5 else 0
            # signe fixé : plus grande composante positive
            if u[np.argmax(np.abs(u))] < 0:
                u = -u
            U[:, j] = u
            labels[a + j] = dict(irrep=names[k], sf=pf, sr=pr, mult=b - a)
        V[:, a:b] = U
    return w, V, labels


def summary(piece):
    w, _, _ = modes(piece)
    lv = levels(w)
    mult = [b - a for a, b in lv]
    return dict(piece=piece, distinct=len(lv), zeros=int(np.sum(np.abs(w) < TOL)),
                lmin=w[w > TOL].min(), lmax=w.max(), max_mult=max(mult))


# ----------------------------------------------------------------- figures --
def board_image(ax, v, title=None, vmax=None):
    import matplotlib.pyplot as plt
    img = v.reshape(8, 8)  # img[rang, colonne]
    vmax = vmax or np.abs(v).max()
    ax.imshow(img, origin="lower", cmap="RdBu_r", vmin=-vmax, vmax=vmax)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    if title:
        ax.set_title(title, fontsize=8)


def fig_modes(piece, n=16, path=None, norm=False):
    import matplotlib.pyplot as plt
    w, V, lab = modes(piece, norm)
    cols = 8
    rows = int(np.ceil(n / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 1.6, rows * 2.1))
    for k, ax in enumerate(axs.ravel()):
        if k >= n:
            ax.axis("off"); continue
        f = 220 * np.sqrt(max(w[k], 0))
        ttl = f"λ={w[k]:.3f}  {lab[k]['irrep']}" + (f" ×{lab[k]['mult']}" if lab[k]['mult'] > 1 else "")
        board_image(ax, V[:, k], ttl.replace("  ", "\n") + f"  {f:.0f} Hz")
    fig.suptitle(f"{NAMES_FR[piece]} — {n} premiers modes (L = D − A)", fontsize=11)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def fig_spectra(path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 3.6))
    for row, p in enumerate(PIECES):
        w, _, _ = modes(p)
        for a, b in levels(w):
            if w[a] < TOL:
                continue
            f = 220 * np.sqrt(w[a])
            ax.plot([f, f], [row - 0.35 * min(1, 0.3 + 0.1 * (b - a)), row + 0.35 * min(1, 0.3 + 0.1 * (b - a))],
                    color=f"C{row}", lw=1.2 + 0.08 * (b - a))
    ax.set_xscale("log")
    ticks = [110, 220, 440, 880, 1760]
    ax.set_xticks(ticks); ax.set_xticklabels(["La2\n110", "La3\n220", "La4\n440", "La5\n880", "La6\n1760"])
    ax.set_yticks(range(len(PIECES))); ax.set_yticklabels([NAMES_FR[p] for p in PIECES])
    ax.set_xlim(100, 1400)
    ax.set_title("Spectres : chaque trait = une fréquence propre (f = 220·√λ Hz) ; trait épais = mode dégénéré")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)


def fig_knight_checkerboard(path):
    import matplotlib.pyplot as plt
    A = adjacency("N")
    d = A.sum(1).astype(float)
    w, V = np.linalg.eigh(normalized_laplacian(A))
    v = V[:, -1]
    rw = v / np.sqrt(d)  # vecteur de la marche au hasard D^-1/2 v
    cb = np.array([(-1) ** sum(coords(i)) for i in range(64)], float)
    ov_sym = abs(v @ cb) / (np.linalg.norm(v) * np.linalg.norm(cb))
    ov_rw = abs(rw @ cb) / (np.linalg.norm(rw) * np.linalg.norm(cb))
    fig, axs = plt.subplots(1, 2, figsize=(6, 3.3))
    board_image(axs[0], v * np.sign(v[0]), f"vecteur propre de I−D^-½AD^-½\nλ={w[-1]:.3f}, recouvrement {ov_sym:.3f}")
    board_image(axs[1], rw * np.sign(rw[0]), f"D^-½·v (marche au hasard)\nrecouvrement {ov_rw:.3f}")
    fig.suptitle("Cavalier : le mode le plus aigu est le damier")
    fig.tight_layout(); fig.savefig(path, dpi=120); plt.close(fig)
    return ov_sym, ov_rw


if __name__ == "__main__":
    import pathlib, matplotlib
    matplotlib.use("Agg")
    out = pathlib.Path(__file__).resolve().parents[1] / "figures"
    out.mkdir(exist_ok=True)
    print(f"{'pièce':9s} {'distinctes':>10s} {'λ=0':>4s} {'λmin>0':>8s} {'λmax':>7s} {'mult max':>8s}")
    for p in PIECES:
        s = summary(p)
        print(f"{NAMES_FR[p]:9s} {s['distinct']:10d} {s['zeros']:4d} {s['lmin']:8.4f} {s['lmax']:7.3f} {s['max_mult']:8d}")
        fig_modes(p, 16, out / f"modes_{p}.png")
    fig_spectra(out / "spectres.png")
    print("cavalier, recouvrement damier (sym, marche) : %.4f %.4f" % fig_knight_checkerboard(out / "cavalier_damier.png"))
