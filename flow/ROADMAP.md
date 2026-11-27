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

## Prochaines étapes
2. Lecture en flux d'un fichier mensuel Lichess (database.lichess.org, accessible), Blitz, tranches de 200 Elo ;
   mesure du temps sur 1000 parties ; traitement de la fin de partie : puits « exit » vs survivants (T_g ≥ T).
3. Hodge (gradient + rotationnel + harmonique), test 4 ; localité (test 5) ; stabilité et bootstrap (test 6).
4. Témoin 1 (coups aléatoires, même distribution de longueurs) ; 5 indicateurs par tranche, IC, repondération ECO.
5. Visuels, vidéo, PDF.

## Limites et choix à garder en tête
- Le chemin d'un cavalier n'est pas unique : choix des deux L à 1/2 (sensibilité testée avec la variante directe).
- La tour du roque traverse la case du roi : décomposition le long de la rangée quand même (choix annoncé).
