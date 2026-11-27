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

## Résultats (Blitz, lichess 2026-10, 2 Go : 175 194 parties, 20 000 par tranche, 15 194 pour 2400-2600)
Validation : continuité exacte sur les données réelles ; Hodge à la précision machine ; test 6 parfait
(écart entre moitiés = bruit pur : médiane 0,67 / 95e 1,98 ; sd(N/2)/sd(N) = 1,41, sd(N/4)/sd(N) = 2,00).
- **Localité (test 5)** : Σ|div_fd − div_exacte| / Σ|div_exacte| ≈ 2 à tous les Elo. Les différences finies à 4 voisins
  ratent déjà un simple pas diagonal (écart 2) ; fou 3,3, tour jusqu'à 3,8. Les échecs ne sont PAS un fluide local à
  l'échelle 8×8 : toutes les conclusions reposent sur les quantités exactes sur les liens ; le continu = visuels seulement.
- **Fraction rotationnelle (Hodge)** : ouverture 0,65 (témoin 0,56), légèrement croissante avec l'Elo.
  Fin de partie : **0,45 (800) -> 0,34 (2400)**, pente −0,072 / 1000 Elo, IC95 [−0,085 ; −0,065] (ECO : [−0,102 ; −0,066]),
  témoin plat ≈ 0,55. Robuste : correction de biais par produit croisé des moitiés (0,445 -> 0,340), sous-fenêtres fixes
  60-80 (0,454 -> 0,365) et 80-100 (0,460 -> 0,348). Les forts joueurs ont un écoulement de fin de partie plus « dirigé ».
- **Entropie des prises** : prises très concentrées dans l'ouverture (3,2-4,0 bits contre 5,3 au hasard), d'autant plus
  que l'Elo est élevé : −0,53 bit / 1000 Elo (ECO : −0,39) ; l'effet diminue avec la phase (−0,07 au-delà de 60).
- **Convergence près du roi adverse** : les débutants convergent vers le roi adverse au milieu de partie (10-30 : 0,073
  à 800 contre 0,038 à 2400 ; témoin 0,045) ; les forts joueurs sont SOUS le hasard. Aucun effet après 60.
- **Cohérence** : effets minuscules (≤ 0,006) ; non retenu comme résultat.
- **Activité Σ|J|** : biaisée par le bruit (Σ|·| d'une moyenne bruitée). Fiable en ouverture (plancher de bruit 0,05 pour
  1,95), NON interprétable après 60 (plancher 0,19-0,27 pour 0,52, et dépendant de l'Elo par le nombre de survivants).

- **Référentiel « mon camp »** : même résultat, rotationnel fin de partie 0,47 -> 0,36.
- **Par type de pièce** (fin de partie, « mon camp ») : roi quasi potentiel (0,07-0,10), tours tourbillonnaires (0,70-0,74,
  sans effet Elo), pions 0,56 -> 0,49 et part d'énergie 40 % -> 30 % : la baisse globale vient surtout des pions.
- **Laminaire / turbulent** : intensité de turbulence √(1/coh² − 1) ≈ 7-10 à tous les Elo (hasard 10-13) ; spectre
  d'énergie sur les modes propres du graphe (`src/spectrum.py`, énergie sans biais par moitiés) : gradient en loi de
  puissance ≈ λ^-2 comme le témoin, rotationnel plat (pas de cascade), sans tendance Elo. Pas de transition
  laminaire/turbulent : le contraste pertinent est **écoulement potentiel vs tourbillonnaire**. Exploratoire (non
  pré-enregistré) : part des grands tourbillons au développement 0,17 -> 0,11 avec l'Elo.

## Prochaines étapes
2. Lecture en flux d'un fichier mensuel Lichess (database.lichess.org, accessible), Blitz, tranches de 200 Elo ;
   mesure du temps sur 1000 parties ; traitement de la fin de partie : puits « exit » vs survivants (T_g ≥ T).
3. Hodge (gradient + rotationnel + harmonique), test 4 ; localité (test 5) ; stabilité et bootstrap (test 6).
4. Témoin 1 (coups aléatoires, même distribution de longueurs) ; 5 indicateurs par tranche, IC, repondération ECO.
5. Visuels, vidéo, PDF.

## Limites et choix à garder en tête
- Le chemin d'un cavalier n'est pas unique : choix des deux L à 1/2 (sensibilité testée avec la variante directe).
- La tour du roque traverse la case du roi : décomposition le long de la rangée quand même (choix annoncé).
