# chess-flow — l'échiquier comme un fluide (feuille de route)

## Faits établis
- **Étape 1 (fait)** — `src/flow.py` : comptage exact, en entiers (demi-unités W = 2), sur le graphe des 210 liens
  « roi » (8 voisins). Coups décomposés en pas unitaires ; roque = roi + tour (la tour traverse le roi) ;
  cavalier = moyenne des deux chemins en L (variante : lien direct non local, 168 liens) ; prise = puits de
  l'espèce prise (en passant : case du pion pris) ; promotion = puits pion + source nouvelle pièce ;
  fin de partie = puits « exit ». Référentiels : absolu (12 espèces) et « mon camp » (6 espèces, Noirs retournés).
- Tests au vert (`python3 -m pytest -q flow/tests`, 16 s) :
  1. 8 mini-parties calculées à la main (poussée, prise, en passant, petit et grand roque, promotion avec prise,
     cavalier en L et direct, référentiel « mon camp ») ;
  2. résidu de l'équation de continuité **identiquement nul**, partie par partie et agrégé, 2 référentiels × 2 variantes ;
  3. conservation : Σ_x S(x, t) = pièces restantes (comptées indépendamment par les prises) ; sortie = pièces finales.
- Coût du comptage : 2,6 ms par partie de 80 demi-coups (hors lecture PGN).

## Décisions
- Données : préfixe du fichier mensuel Blitz Lichess lu en flux, **plafond 2 Go** (on augmentera si les résultats sont bons) ;
  moins de 20 000 parties acceptées dans les tranches extrêmes.
- Témoin 2 (moteur / Maia / loi chess-physics) : reporté, plus tard.

## Indicateurs pré-enregistrés (définis avant de regarder les données, 27/11/2026)
Fenêtres de demi-coups : [0,10[, [10,30[, [30,60[, ≥ 60. Toutes espèces confondues, référentiel absolu, cavalier en L.
Normalisation par transition (t < T_g) : l'ensemble perd les parties terminées (puits « exit »).
1. **Activité** : Σ_e |J̄_e(t)|, J̄ = flux net moyen par partie vivante ; moyenne par fenêtre (t < 120).
2. **Fraction rotationnelle** : ‖Cᵀψ‖² / ‖J‖² du flux net cumulé sur la fenêtre (Hodge, complexe des triangles).
3. **Cohérence** : par case |Σ déplacements| / (n · √(Σ déplacement² / n)), moyennée sur les cases pondérées par n.
4. **Entropie des puits** : entropie (bits, max 6) de la carte des prises (hors promotions).
5. **Convergence près du roi adverse** : arrivées − départs des pièces du camp au trait dans le carré 5×5
   centré sur le roi adverse (Chebyshev ≤ 2), par transition.
IC : bootstrap de Poisson sur les parties (R = 200), avec et sans repondération ECO (groupes de 2 caractères,
cible = mélange moyen des tranches). Témoin 1 : 5000 parties de coups légaux au hasard par tranche, longueurs tirées
dans la distribution de la tranche.

## Prochaines étapes
2. Lecture en flux d'un fichier mensuel Lichess (database.lichess.org, accessible), Blitz, tranches de 200 Elo ;
   mesure du temps sur 1000 parties ; traitement de la fin de partie : puits « exit » vs survivants (T_g ≥ T).
3. Hodge (gradient + rotationnel + harmonique), test 4 ; localité (test 5) ; stabilité et bootstrap (test 6).
4. Témoin 1 (coups aléatoires, même distribution de longueurs) ; 5 indicateurs par tranche, IC, repondération ECO.
5. Visuels, vidéo, PDF.

## Limites et choix à garder en tête
- Le chemin d'un cavalier n'est pas unique : choix des deux L à 1/2 (sensibilité testée avec la variante directe).
- La tour du roque traverse la case du roi : décomposition le long de la rangée quand même (choix annoncé).
