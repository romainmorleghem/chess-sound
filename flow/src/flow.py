"""L'échiquier comme un fluide : comptage EXACT des flux sur les liens, sources et puits.

Graphe des liens : les 64 cases, reliées à leurs 8 voisines (210 liens). Chaque lien e = (u, w) avec u < w
est orienté de u vers w ; F[t, s, e, 0] compte les pas u -> w, F[t, s, e, 1] les pas w -> u.
Flux net J_e = F[..., 0] - F[..., 1] ; divergence (flux sortant net) div J(x) = Σ_e B[e, x] J_e,
avec B[e, u] = +1, B[e, w] = -1 (matrice d'incidence).

Un coup a -> b est décomposé en pas unitaires le long du chemin (tour, fou, dame, roi, pion).
Cavalier : moyenne des deux chemins en L (1/2 chacun) ; variante knight="direct" : un lien non local a -> b.
Pour rester en ENTIERS, tout est compté en demi-unités : W = 2 (une pièce = 2, un demi-chemin = 1).

Temps : t = nombre de demi-coups joués. La position t existe pour t = 0 .. T_g (T_g = longueur de la partie g).
Sommes d'ensemble (non normalisées) : S[t, s, x] = Σ_{parties vivantes en t} W·1[pièce s en x].
Équation de continuité exacte (en entiers) :
    S[t+1] - S[t] = -div J[t] + src[t] - snk[t] - exit[t]
où exit[t] = occupation des parties qui se terminent en t (puits « fin de partie »).
La densité du projet est ρ(x, t) = S[t] / (W · N(t)).
"""
import numpy as np
import chess

W = 2
NS_ABS, NS_MINE = 12, 6
PT_NAMES = "PNBRQK"


def _king_edges():
    out = []
    for x in range(64):
        fx, rx = x % 8, x // 8
        for y in range(x + 1, 64):
            fy, ry = y % 8, y // 8
            if max(abs(fx - fy), abs(rx - ry)) == 1:
                out.append((x, y))
    return out


def _knight_edges():
    out = []
    for x in range(64):
        fx, rx = x % 8, x // 8
        for y in range(x + 1, 64):
            fy, ry = y % 8, y // 8
            if sorted((abs(fx - fy), abs(rx - ry))) == [1, 2]:
                out.append((x, y))
    return out


EDGES = _king_edges()                       # 210 liens locaux
EIDX = {e: k for k, e in enumerate(EDGES)}
KEDGES = _knight_edges()                    # 168 liens « cavalier » (variante non locale)
KIDX = {e: k for k, e in enumerate(KEDGES)}


def incidence(edges=EDGES):
    B = np.zeros((len(edges), 64), dtype=np.int64)
    for k, (u, w) in enumerate(edges):
        B[k, u], B[k, w] = 1, -1
    return B


B_LOC, B_KN = incidence(EDGES), incidence(KEDGES)


def species(color, ptype, frame="abs"):
    """abs : 0-5 = P N B R Q K blancs, 6-11 = noirs. mine : 0-5 (type seul, Noirs retournés)."""
    if frame == "mine":
        return ptype - 1
    return (0 if color == chess.WHITE else 6) + ptype - 1


def _sq(x, color, frame):
    """Case dans le référentiel : « mine » retourne l'échiquier pour les Noirs (rangée r -> 7 - r)."""
    return x ^ 56 if (frame == "mine" and color == chess.BLACK) else x


def line_path(a, b):
    """Cases a, ..., b le long d'une ligne droite ou diagonale (pas unitaires)."""
    fa, ra, fb, rb = a % 8, a // 8, b % 8, b // 8
    df, dr = np.sign(fb - fa), np.sign(rb - ra)
    n = max(abs(fb - fa), abs(rb - ra))
    assert (fb - fa, rb - ra) == (df * n, dr * n), (chess.square_name(a), chess.square_name(b))
    return [chess.square(fa + k * df, ra + k * dr) for k in range(n + 1)]


def knight_paths(a, b):
    """Les deux chemins en L de a à b (jambe longue puis courte, et l'inverse), en pas orthogonaux."""
    fa, ra, fb, rb = a % 8, a // 8, b % 8, b // 8
    df, dr = fb - fa, rb - ra
    c1 = chess.square(fb, ra) if abs(df) == 2 else chess.square(fa, rb)      # coin : jambe longue d'abord
    c2 = chess.square(fa, rb) if abs(df) == 2 else chess.square(fb, ra)      # jambe courte d'abord
    p1 = line_path(a, c1)[:-1] + line_path(c1, b)
    p2 = line_path(a, c2)[:-1] + line_path(c2, b)
    return p1, p2


def move_events(board, move, knight="L"):
    """Événements d'un coup (avant board.push(move)), en demi-unités W.

    Retourne dict(steps=[(color, ptype, x, y, w)], kn=[(color, ptype, a, b, w)],
                  src=[(color, ptype, x, w)], snk=[(color, ptype, x, w)], disp=[(color, ptype, a, b)])
    disp = déplacement de chaque pièce qui bouge (pour le champ de vitesse aux cases).
    """
    ev = dict(steps=[], kn=[], src=[], snk=[], disp=[])
    a, b = move.from_square, move.to_square
    pc = board.piece_at(a)
    col, pt = pc.color, pc.piece_type

    def walk(path, c, p, w=W):
        for x, y in zip(path, path[1:]):
            ev["steps"].append((c, p, x, y, w))

    if board.is_castling(move):
        rank = a // 8
        kingside = chess.square_file(b) > chess.square_file(a)
        kb = chess.square(6 if kingside else 2, rank)                # python-chess : to_square = tour (960) ou g/c
        ra_ = chess.square(7 if kingside else 0, rank)
        rb_ = chess.square(5 if kingside else 3, rank)
        walk(line_path(a, kb), col, chess.KING)
        walk(line_path(ra_, rb_), col, chess.ROOK)                   # la tour « passe au-dessus » du roi
        ev["disp"] += [(col, chess.KING, a, kb), (col, chess.ROOK, ra_, rb_)]
        return ev
    if board.is_en_passant(move):
        cap = chess.square(chess.square_file(b), chess.square_rank(a))
        ev["snk"].append((not col, chess.PAWN, cap, W))
    elif board.is_capture(move):
        q = board.piece_at(b)
        ev["snk"].append((q.color, q.piece_type, b, W))
    if pt == chess.KNIGHT:
        if knight == "L":
            for p in knight_paths(a, b):
                walk(p, col, pt, W // 2)
        else:
            ev["kn"].append((col, pt, a, b, W))
    else:
        walk(line_path(a, b), col, pt)
    ev["disp"].append((col, pt, a, b))
    if move.promotion:
        ev["snk"].append((col, chess.PAWN, b, W))
        ev["src"].append((col, move.promotion, b, W))
    return ev


class Flow:
    """Accumulateur d'ensemble. add_game(moves, weight) ; tous les tableaux sont des sommes (en unités W)."""

    def __init__(self, tmax=400, frame="abs", knight="L"):
        self.tmax, self.frame, self.knight = tmax, frame, knight
        ns = NS_ABS if frame == "abs" else NS_MINE
        self.ns = ns
        T = tmax + 1
        z = lambda *sh: np.zeros(sh, dtype=np.int64)
        self.N = z(T)                       # parties vivantes en t (position t existe)
        self.S = z(T, ns, 64)               # occupation
        self.F = z(T, ns, len(EDGES), 2)    # pas sur les liens locaux, transition t -> t+1
        self.FK = z(T, ns, len(KEDGES), 2)  # liens cavalier directs (variante)
        self.src, self.snk, self.exit = z(T, ns, 64), z(T, ns, 64), z(T, ns, 64)
        self.D = z(T, ns, 64, 2)            # somme des déplacements (df, dr) des pièces partant de x
        self.D2 = z(T, ns, 64)              # somme des déplacements au carré
        self.NP = z(T)                      # nombre de pièces (W) attendu, compté indépendamment (prises)
        self.games = 0
        self.truncated = 0

    def _sp(self, c, p):
        return species(c, p, self.frame)

    def _x(self, x, c):
        return _sq(x, c, self.frame)

    def add_game(self, moves, start_fen=chess.STARTING_FEN, weight=1):
        b = chess.Board(start_fen)
        moves = list(moves)
        if len(moves) > self.tmax:
            moves = moves[: self.tmax]
            self.truncated += weight
        n_pieces = len(b.piece_map()) * W
        occ_t, occ_s, occ_x = [], [], []
        st, ss, se, sd, sw = [], [], [], [], []
        kt, ks, ke, kd = [], [], [], []
        pt_, ps, px, pw = [], [], [], []     # sources
        qt, qs, qx, qw = [], [], [], []      # puits
        dt, ds, dx, dv = [], [], [], []      # déplacements
        np_t = []

        def occupy(t):
            for x, pc in b.piece_map().items():
                occ_t.append(t); occ_s.append(self._sp(pc.color, pc.piece_type)); occ_x.append(self._x(x, pc.color))

        for t, mv in enumerate(moves):
            occupy(t)
            np_t.append(n_pieces)
            ev = move_events(b, mv, self.knight)
            for c, p, x, y, w in ev["steps"]:
                x, y = self._x(x, c), self._x(y, c)
                st.append(t); ss.append(self._sp(c, p)); sw.append(w)
                se.append(EIDX[(min(x, y), max(x, y))]); sd.append(0 if x < y else 1)
            for c, p, x, y, w in ev["kn"]:
                x, y = self._x(x, c), self._x(y, c)
                kt.append(t); ks.append(self._sp(c, p))
                ke.append(KIDX[(min(x, y), max(x, y))]); kd.append(0 if x < y else 1)
            for c, p, x, w in ev["src"]:
                pt_.append(t); ps.append(self._sp(c, p)); px.append(self._x(x, c)); pw.append(w)
            for c, p, x, w in ev["snk"]:
                qt.append(t); qs.append(self._sp(c, p)); qx.append(self._x(x, c)); qw.append(w)
            for c, p, a_, b_ in ev["disp"]:
                a2, b2 = self._x(a_, c), self._x(b_, c)
                dt.append(t); ds.append(self._sp(c, p)); dx.append(a2)
                dv.append((b2 % 8 - a2 % 8, b2 // 8 - a2 // 8))
            if b.is_capture(mv):
                n_pieces -= W
            b.push(mv)
        T = len(moves)
        occupy(T)
        np_t.append(n_pieces)
        # --- agrégation (une seule passe numpy par partie) ---
        wgt = weight
        occ = (np.array(occ_t), np.array(occ_s), np.array(occ_x))
        np.add.at(self.S, occ, W * wgt)
        fin = occ[0] == T
        np.add.at(self.exit, (occ[0][fin], occ[1][fin], occ[2][fin]), W * wgt)
        self.N[: T + 1] += wgt
        self.NP[: T + 1] += np.array(np_t) * wgt
        self.games += wgt
        if st:
            np.add.at(self.F, (np.array(st), np.array(ss), np.array(se), np.array(sd)), np.array(sw) * wgt)
        if kt:
            np.add.at(self.FK, (np.array(kt), np.array(ks), np.array(ke), np.array(kd)), W * wgt)
        if pt_:
            np.add.at(self.src, (np.array(pt_), np.array(ps), np.array(px)), np.array(pw) * wgt)
        if qt:
            np.add.at(self.snk, (np.array(qt), np.array(qs), np.array(qx)), np.array(qw) * wgt)
        if dt:
            dv = np.array(dv)
            idx = (np.array(dt), np.array(ds), np.array(dx))
            np.add.at(self.D, idx + (0,), dv[:, 0] * W * wgt)
            np.add.at(self.D, idx + (1,), dv[:, 1] * W * wgt)
            np.add.at(self.D2, idx, (dv ** 2).sum(1) * W * wgt)
        return T

    # ------------------------------------------------------------------ dérivées --
    def J(self):
        """Flux net sur les liens locaux, J[t, s, e] (unités W)."""
        return self.F[..., 0] - self.F[..., 1]

    def JK(self):
        return self.FK[..., 0] - self.FK[..., 1]

    def div(self):
        """Divergence exacte sur le graphe (flux sortant net), div[t, s, x] ; inclut les liens cavalier directs."""
        return self.J() @ B_LOC + self.JK() @ B_KN

    def residual(self):
        """Résidu de l'équation de continuité, pour t = 0 .. tmax-1 (doit être identiquement nul)."""
        S = self.S
        return S[1:] - S[:-1] + self.div()[:-1] - self.src[:-1] + self.snk[:-1] + self.exit[:-1]

    def rho(self):
        """Densité ρ[t, s, x] = S / (W N(t))  (NaN quand N(t) = 0)."""
        with np.errstate(invalid="ignore", divide="ignore"):
            return self.S / (W * self.N[:, None, None])


def random_game(rng, max_plies=200, start_fen=chess.STARTING_FEN):
    """Partie de coups légaux tirés uniformément (témoin 1 et tests)."""
    b = chess.Board(start_fen)
    out = []
    while len(out) < max_plies and not b.is_game_over():
        ms = list(b.legal_moves)
        mv = ms[rng.integers(len(ms))]
        out.append(mv)
        b.push(mv)
    return out


def san_moves(text, start_fen=chess.STARTING_FEN):
    b = chess.Board(start_fen)
    out = []
    for tok in text.split():
        tok = tok.split(".")[-1]
        if not tok:
            continue
        mv = b.parse_san(tok)
        out.append(mv)
        b.push(mv)
    return out
