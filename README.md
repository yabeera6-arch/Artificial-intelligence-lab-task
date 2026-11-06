Lab 1 is about symbolic vs probability-based AI, using a scholarship screening checker that keeps score >= 70 and complete documents, and adds deadline met and recommendation present as two new rules.
Run the code in lab1 (1).py with python "lab1 (1).py" and see the project summary in lab 1 summary.docx; all 4 tests pass, including a pass, a deadline failure, a recommendation failure, and the boundary score of 70.

Lab 2 is about intelligent agents and the PEAS framework, using a smart classroom agent that remembers its last mode and only sends a new command when the mode changes.
Run the code in lab2 (1).py with python "lab2 (1).py" and see the full summary and trace in lab 2 summary.docx; all 6 tests pass, including repeats, the 20 and 26 boundaries, a mode change, and an empty room.

Lab 3 implements uninformed search from scratch: BFS, DFS, DLS, IDDFS and UCS on a small building map.
The report (lab 3 summary.docx) holds the hand-traced BFS/DFS frontiers, DLS/IDDFS results at limits 1-4, and the weighted-graph UCS experiment.
Run the code with: python lab3.py
All 7 checks pass: visit orders, DLS/IDDFS limits, the UCS cost-3 path with independent cost check, the BFS-vs-UCS comparison, and the edge cases.

README.md
Lab 4: Informed Search — A* with a heuristic on the campus graph (S, A, B, C, G), compared with a zero-heuristic UCS run and an h(C) = 10 overestimate experiment.
Files: lab4.py (code) and lab 4 summary.docx (8-line Project Summary).
Run: python lab4.py
Result: A* finds S -> A -> C -> G at cost 6 and expands 3 nodes; UCS finds the same path and cost but expands 4; the overestimate returns the cost-9 route S -> B -> G; all checks pass.

Lab 5: Adversarial Search — Minimax and alpha-beta pruning on a small game tree: a hand trace, leaf counters on both algorithms, and a branch-reorder test.
Files: lab5.py (code) and lab 5 summary.docx (8-line Project Summary).
Run: python lab5.py
Result: the hand trace and every run give root value 5; minimax checks all 8 leaves, alpha-beta checks 5 or 7 leaves after reordering, so pruning saves work without changing the answer; all 7 checks pass.


Lab 6: NLP Fundamentals — Tokenization, Embeddings and Text Chunking: token comparison on 6 inputs, a FAQ chatbot, word-window and sentence-aware chunking, and TF-IDF retrieval evaluation on a help-desk corpus.
Files: lab6.py (code) and lab 6 summary.docx (8-line Project Summary).
Run: python lab6.py
Result: sentence-aware packing was chosen — 22 chunks, 0 repeated words, 8/8 evidence kept whole, best dev Hit@3 1.0 and MRR@3 0.833; all checks pass with exit 0, and the embedding backend is recorded as a limitation since it could not run here.










