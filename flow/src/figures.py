"""Figures pédagogiques (style sombre de la vidéo) -> flow/figures/*.png

Référentiel « mon camp » (chaque joueur joue vers le haut) pour les champs ; absolu pour les indicateurs pré-enregistrés.
"""
import glob, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
sys.path.insert(0, os.path.dirname(__file__))
from flow import load_flows, W, EDGES, B_LOC
from hodge import Hodge, block_circulation
from reduce import view

BG, FG, MUTED, GRIDC = "#0E1116", "#E6E6E6", "#7A8291", "#262D38"
RED, BLUE, GOLD = "#E4572E", "#3F7FC8", "#F2B544"
DIV = LinearSegmentedColormap.from_list("div", [BLUE, "#2A303A", RED])
SEQ = LinearSegmentedColormap.from_list("seq", ["#151A22", "#5C4A22", GOLD, "#FFF1C9"])
WINS = [(0, 10), (10, 30), (30, 60), (60, 300)]
WNAMES = ["ouverture\n0-10", "développement\n10-30", "milieu\n30-60", "fin de partie\n≥ 60"]
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
H = Hodge()
plt.rcParams.update({"figure.facecolor": BG, "axes.facecolor": BG, "text.color": FG, "axes.labelcolor": FG,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.edgecolor": GRIDC, "font.size": 12,
                     "savefig.facecolor": BG})
FILES = "abcdefgh"


def board_axes(ax, n=8):
    ax.set_xticks(range(n)); ax.set_yticks(range(n))
    ax.set_xticklabels(FILES[:n] if n == 8 else []); ax.set_yticklabels(range(1, n + 1) if n == 8 else [])
    ax.tick_params(length=0, labelsize=9)
    for s in ax.spines.values():
        s.set_visible(False)


def window(f, a, b):
    """Champs moyens par transition (une partie, un demi-coup) sur la fenêtre [a, b[, toutes espèces."""
    ntr = f.N[a + 1:b + 1].sum()
    J = f.J()[a:b].sum((0, 1)) / (W * ntr)
    D = f.D[a:b].sum((0, 1)) / (W * ntr)                      # [64, 2] déplacements partant de chaque case
    rho = f.S[a:b].sum((0, 1)) / (W * f.N[a:b].sum())
    return J, D, rho


def edge_vectors(J):
    """Vecteur aux cases à partir du flux sur les liens : ½ Σ_e J_e (sortant) · direction unitaire."""
    V = np.zeros((64, 2))
    for k, (u, w) in enumerate(EDGES):
        d = np.array([w % 8 - u % 8, w // 8 - u // 8], float)
        d /= np.linalg.norm(d)
        V[u] += 0.5 * J[k] * d
        V[w] += 0.5 * J[k] * d
    return V


def load(name="mine"):
    out = {}
    for p in sorted(glob.glob("data/flow_*.npz"), key=lambda p: int(p.split("_")[-1].split(".")[0])):
        fl, _ = load_flows(p)
        out[int(p.split("_")[-1].split(".")[0])] = fl[name]
    return out


def fig_phases(F, elos=(800, 2400)):
    fig, axs = plt.subplots(len(elos), 4, figsize=(16, 8.6))
    X, Y = np.meshgrid(range(8), range(8))
    for j, (a, b) in enumerate(WINS):
        fields = {e: window(F[e], a, b) for e in elos}
        vmax = max(np.abs(fields[e][0] @ B_LOC).max() for e in elos)
        amax = max(np.abs(fields[e][1]).max() for e in elos)
        for i, e in enumerate(elos):
            J, D, rho = fields[e]
            ax = axs[i, j]
            div = (J @ B_LOC).reshape(8, 8)
            ax.imshow(div, origin="lower", cmap=DIV, norm=TwoSlopeNorm(0, -vmax, vmax))
            U, V = D[:, 0].reshape(8, 8), D[:, 1].reshape(8, 8)
            ax.quiver(X, Y, U, V, color=FG, scale=amax * 9, width=0.006, headwidth=4)
            board_axes(ax)
            if i == 0:
                ax.set_title(WNAMES[j], color=FG, fontsize=13)
            if j == 0:
                ax.set_ylabel(f"{e}-{e+200} Elo", fontsize=14)
    fig.suptitle("Où partent (rouge : source, div > 0) et où arrivent (bleu : puits, div < 0) les pièces ; "
                 "flèches = déplacement moyen", color=FG, fontsize=14)
    fig.text(0.5, 0.01, "Référentiel « mon camp » : chaque joueur joue vers le haut. Divergence exacte sur les liens.",
             ha="center", color=MUTED, fontsize=11)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(f"{OUT}/1_sources_puits_par_phase.png", dpi=110); plt.close(fig)


def fig_hodge(F, elos=(800, 2400), win=(60, 300)):
    fig, axs = plt.subplots(len(elos), 3, figsize=(15, 9.4))
    X, Y = np.meshgrid(range(8), range(8))
    parts = {e: H.decompose(window(F[e], *win)[0]) for e in elos}
    pmax = max(np.abs(parts[e][3]).max() for e in elos)
    cmax = max(np.abs(block_circulation(parts[e][1])).max() for e in elos)
    vmax = max(max(np.abs(edge_vectors(parts[e][0])).max(), np.abs(edge_vectors(parts[e][1])).max()) for e in elos)
    for i, e in enumerate(elos):
        g, c, h, phi, psi = parts[e]
        fr = (g ** 2).sum(), (c ** 2).sum()
        rot = fr[1] / (fr[0] + fr[1])
        ax = axs[i, 0]
        ax.imshow(phi.reshape(8, 8), origin="lower", cmap=SEQ, vmin=-pmax, vmax=pmax)
        Vg = edge_vectors(g)
        ax.quiver(X, Y, Vg[:, 0].reshape(8, 8), Vg[:, 1].reshape(8, 8), color=FG, scale=vmax * 9, width=0.006)
        board_axes(ax); ax.set_ylabel(f"{e}-{e+200} Elo", fontsize=14)
        ax.set_title(f"gradient : l'écoulement descend la « pente » φ\n{100*(1-rot):.0f} % de l'énergie", fontsize=12)
        ax = axs[i, 1]
        circ = block_circulation(c)
        ax.imshow(circ, origin="lower", cmap=DIV, norm=TwoSlopeNorm(0, -cmax, cmax), extent=(0, 7, 0, 7))
        Vc = edge_vectors(c)
        cv = max(np.abs(edge_vectors(parts[x][1])).max() for x in elos)
        ax.quiver(X, Y, Vc[:, 0].reshape(8, 8), Vc[:, 1].reshape(8, 8), color=FG, scale=cv * 9, width=0.006)
        ax.set_xlim(-0.5, 7.5); ax.set_ylim(-0.5, 7.5)
        board_axes(ax)
        ax.set_title(f"rotationnel : tourbillons (rouge ↺, bleu ↻)\n{100*rot:.0f} % de l'énergie", fontsize=12)
        ax = axs[i, 2]
        ax.barh([1, 0], [1 - rot, rot], color=[GOLD, RED], height=0.55)
        ax.set_yticks([1, 0]); ax.set_yticklabels(["gradient", "rotationnel"], color=FG)
        ax.set_xlim(0, 1); ax.set_xlabel("fraction de l'énergie du flux")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for y, v in ((1, 1 - rot), (0, rot)):
            ax.text(v + 0.02, y, f"{v:.2f}", va="center", color=FG)
    fig.suptitle("Fin de partie (≥ 60 demi-coups) : décomposition de Hodge du flux moyen", fontsize=15)
    fig.text(0.5, 0.01, "flux = gradient (descend un potentiel) + rotationnel (circule autour des triangles de cases) ; "
             "partie harmonique nulle (échiquier « plein »)", ha="center", color=MUTED, fontsize=11)
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(f"{OUT}/2_hodge_fin_de_partie.png", dpi=110); plt.close(fig)


def stats(e):
    return np.load(f"data/stats_{e}.npz")


def fig_captures(elos=(800, 2400), k=1):
    fig, axs = plt.subplots(1, 3, figsize=(14, 5.2))
    maps = []
    for e in elos:
        c = stats(e)["central"][0]; K = view(c, "Kw")[k]; maps.append((f"{e}-{e+200} Elo", K / K.sum()))
    c = stats(elos[0])["ctrl.central"][0]; K = view(c, "Kw")[k]; maps.append(("coups au hasard", K / K.sum()))
    vmax = max(m.max() for _, m in maps)
    for ax, (t, m) in zip(axs, maps):
        ent = -(m[m > 0] * np.log2(m[m > 0])).sum()
        ax.imshow(m.reshape(8, 8), origin="lower", cmap=SEQ, vmin=0, vmax=vmax)
        board_axes(ax); ax.set_title(f"{t}\nentropie {ent:.2f} bits (max 6)", fontsize=12)
    fig.suptitle(f"Où ont lieu les prises (puits), développement {WINS[k][0]}-{WINS[k][1]} demi-coups", fontsize=14)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(f"{OUT}/3_prises.png", dpi=110); plt.close(fig)


def fig_king(elos=(800, 2400), k=1):
    fig, axs = plt.subplots(1, 3, figsize=(14, 5.2))
    maps = []
    for e in elos:
        c = stats(e)["central"][0]; maps.append((f"{e}-{e+200} Elo", -view(c, "Zw")[k] / (W * view(c, "Nw")[k])))
    c = stats(elos[0])["ctrl.central"][0]
    maps.append(("coups au hasard", -view(c, "Zw")[k] / (W * view(c, "Nw")[k])))
    vmax = max(np.abs(m[3:12, 3:12]).max() for _, m in maps)
    for ax, (t, m) in zip(axs, maps):
        ax.imshow(m[3:12, 3:12], origin="lower", cmap=DIV, norm=TwoSlopeNorm(0, -vmax, vmax))
        ax.add_patch(plt.Rectangle((1.5, 1.5), 5, 5, fill=False, ec=GOLD, lw=1.5, ls="--"))
        ax.text(4, 4, "♚", ha="center", va="center", fontsize=22, color=FG)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        zone = m[5:10, 5:10].sum()
        ax.set_title(f"{t}\nconvergence dans le carré : {zone:+.3f}", fontsize=12)
    fig.suptitle("Autour du roi adverse : arrivées − départs des pièces du joueur au trait (rouge = accumulation), 10-30",
                 fontsize=13)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(f"{OUT}/4_roi_adverse.png", dpi=110); plt.close(fig)


def fig_trends():
    elos = sorted(int(p.split("_")[-1].split(".")[0]) for p in glob.glob("data/stats_*.npz"))
    x = np.array(elos) + 100
    panels = [("rot", 3, "fraction rotationnelle\nfin de partie (≥ 60)"),
              ("ent", 0, "entropie des prises (bits)\nouverture (0-10)"),
              ("conv", 1, "convergence vers le roi adverse\ndéveloppement (10-30)")]
    fig, axs = plt.subplots(1, 3, figsize=(16, 5))
    for ax, (key, k, title) in zip(axs, panels):
        c = np.array([stats(e)[f"{key}.c"][k] for e in elos])
        b = np.array([stats(e)[f"{key}.boot"][:, k] for e in elos])
        ctrl = np.array([stats(e)[f"ctrl.{key}.c"][k] for e in elos])
        lo, hi = np.percentile(b, [2.5, 97.5], axis=1)
        ax.fill_between(x, lo, hi, color=GOLD, alpha=0.25, lw=0)
        ax.plot(x, c, color=GOLD, lw=2, marker="o", ms=6, label="parties Lichess (IC 95 %)")
        ax.plot(x, ctrl, color=MUTED, lw=2, ls="--", label="coups au hasard (témoin)")
        ax.set_title(title, fontsize=13); ax.set_xlabel("Elo")
        ax.grid(color=GRIDC, lw=0.8); ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axs[0].legend(frameon=False, loc="lower left")
    fig.tight_layout()
    fig.savefig(f"{OUT}/5_tendances_elo.png", dpi=110); plt.close(fig)


def fig_streamlines(F, elos=(800, 2400), win=(10, 30)):
    from scipy.interpolate import RectBivariateSpline
    fig, axs = plt.subplots(1, len(elos), figsize=(13, 6.4))
    g = np.arange(8.0); fine = np.linspace(0, 7, 120)
    for ax, e in zip(axs, elos):
        J, D, rho = window(F[e], *win)
        U = RectBivariateSpline(g, g, D[:, 0].reshape(8, 8))(fine, fine)
        V = RectBivariateSpline(g, g, D[:, 1].reshape(8, 8))(fine, fine)
        ax.imshow(rho.reshape(8, 8), origin="lower", cmap=SEQ, extent=(-0.5, 7.5, -0.5, 7.5))
        sp = np.hypot(U, V)
        ax.streamplot(fine, fine, U, V, color=sp, cmap=LinearSegmentedColormap.from_list("w", ["#5A6272", FG]),
                      density=1.4, linewidth=1.2, arrowsize=1.1)
        board_axes(ax); ax.set_xlim(-0.5, 7.5); ax.set_ylim(-0.5, 7.5)
        ax.set_title(f"{e}-{e+200} Elo", fontsize=14)
    fig.suptitle("Lignes de courant du déplacement moyen, développement (10-30) ; fond = densité de pièces", fontsize=14)
    fig.text(0.5, 0.01, "Interpolation entre les 64 cases purement décorative (les échecs ne sont pas un fluide local).",
             ha="center", color=MUTED, fontsize=11)
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(f"{OUT}/6_lignes_de_courant.png", dpi=110); plt.close(fig)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    F = load("mine")
    fig_phases(F); fig_hodge(F); fig_captures(); fig_king(); fig_trends(); fig_streamlines(F)
    print("ok", sorted(os.listdir(OUT)))
