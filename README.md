# Le son des pièces d'échecs

Chaque pièce d'échecs devient un instrument : 64 billes (les cases) reliées par des élastiques
(un élastique entre deux cases si la pièce passe de l'une à l'autre en un coup, sur échiquier vide).
Modes propres du laplacien L = D − A → fréquences f = 500·√λ Hz → sons, puis mélodies d'ouvertures et de parties célèbres.

| Fichier | Rôle |
|---|---|
| `src/graphs.py` | graphes des 6 pièces (pion : graphe symétrisé poussées + prises), laplaciens, symétries D4 |
| `src/modes.py` | modes propres, base adaptée à D4 dans les espaces dégénérés, figures `figures/` |
| `src/synth.py` | son d'un coup (amplitude par niveau = ‖P_λ x‖, indépendante de la base), WAV dans `sounds/` |
| `tests/` | spectres vérifiés (tour 0/8/16, fou 2 composantes, cavalier biparti, formule du roi, dame 45 valeurs) |

```bash
pip install numpy scipy matplotlib pytest   # + python-chess pour les PGN
python3 -m pytest -q tests && python3 src/modes.py && python3 src/synth.py
```

## Étape 4 — mélodies (`src/melody.py`, `data/games.py`)
`python3 src/melody.py` (≈ 45 s) → `melodies/<nom>.mp3` + `<nom>.json` (frise : temps, coup, pièce, fréquence dominante, scores).
Règles : frappe à l'arrivée (tour : geste départ → arrivée) ; prise = accent ; roque = accord roi + tour ;
échec = demi-ton dissonant ; mat = accord majeur juste final ; Blancs à gauche, Noirs à droite.
PGN : coups vérifiés légaux par python-chess, mats finaux retrouvés.

Beauté musicale, deux scores entre notes successives, comparés à 300 parties jouées au hasard (z-score) :
- *simplicité* : rapport de fréquences dominantes proche d'une fraction simple p/q (hauteur de Tenney) ;
- *rugosité* : dissonance sensorielle de Sethares (1993) entre les spectres complets (plus bas = plus doux).

## Étape 5 — vidéo (`video/`, structure du dépôt ising)
Voix off anglaise Kokoro-82M `af_heart` (`video/common/narrative.py`, modèles dans `~/.cache/kokoro`, cf. ising).
Plan : `video/storyboard.md`. Sons des scènes : `python3 video/compute/sounds.py` → `media/sounds/`.
```bash
cd video && python3 render.py          # aperçu 480p  -> media/video/chess_sound_480p15.mp4 (≈ 3 min de rendu)
python3 render.py -q f                 # final 1080p30 -> media/video/chess_sound_1080p30.mp4
python3 render.py --only s09           # re-rendre une séquence puis réassembler
```
