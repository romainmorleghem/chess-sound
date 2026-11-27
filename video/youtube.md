# YouTube

## Title (recommended first)
1. Can You Hear the Shape of a Chess Piece?
2. What Does a Chess Piece Sound Like? (Real Physics)
3. The Melody of a Chess Game
4. I Turned Chess Pieces into Instruments

## Thumbnail
`video/thumbnail.png` (1280×720) — source: `video/scenes/thumb.py`

## Description
What does a knight sound like? Or a queen? Not a sound effect: the real sound, computed from the rules of chess and nothing else.

Put a bead on each of the 64 squares, and stretch a rubber band wherever a piece can move in one go. Each piece builds its own instrument. Its vibration modes (the eigenvectors of the graph Laplacian L = D − A) are its notes. The rook plays a tritone, the bishop is the same instrument twice, and the knight's highest mode is the chessboard itself. Then we play famous games as melodies: the Opera Game, the Immortal Game… and ask which one is the most musical.

In 1966, Mark Kac asked "Can one hear the shape of a drum?" Today: can you hear the shape of a chess piece?

⏱ Chapters
0:00 What does a knight sound like?
0:29 Beads and rubber bands
1:18 How things vibrate
2:03 The maths: L = D − A and eigenmodes
3:46 The knight's modes
4:37 Symmetry and ambiguity
5:44 Six instruments
7:17 Can you hear the shape of a piece? (quiz)
8:09 Striking the instrument
9:37 Games as melodies
11:02 The most melodious game?
11:58 Recap

📐 Our choices
• Frequencies: f = 500 Hz × √λ (λ = eigenvalue of L = D − A, empty board).
• Strike on the arrival square (rook: departure → arrival); mode amplitude ‖P_λ e_i‖ / ω; high notes fade faster.
• Pawn: rubber bands for every push and capture, of both colours (a band has no direction).
• "Beauty": interval simplicity (Tenney height) and roughness (Sethares 1993), compared with 300 random games.

💻 Code (Python: numpy, scipy, python-chess, Manim): https://github.com/romainmorleghem/chess-sound

📚 References
• M. Kac, "Can One Hear the Shape of a Drum?", Amer. Math. Monthly 73 (1966)
• C. Gordon, D. Webb, S. Wolpert, "One cannot hear the shape of a drum", Bull. AMS 27 (1992)
• W. Sethares, "Local consonance and the relationship between timbre and scale", JASA 94 (1993)

Voice: Kokoro-82M (af_heart), synthesised locally.

## Tags
chess, music, physics, eigenvalues, eigenvectors, graph laplacian, spectral graph theory, normal modes, chladni, can you hear the shape of a drum, sonification, knight, opera game, immortal game, manim, math, linear algebra
