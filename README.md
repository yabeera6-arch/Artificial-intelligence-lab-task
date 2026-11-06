Artificial Intelligence Lab Tasks
CS4944, Labs 1 to 6. Each lab is in its own folder, with the code and a short summary.
Lab 1: Introduction to AI
I compared a rule based system with a probability based one. I used a scholarship checker for this. It keeps score 70 or more and complete documents. I added two new rules too, deadline met and recommendation present.
Run it with python "lab1 (1).py". The summary is in lab 1 summary.docx. All 4 tests pass, a pass, a deadline failure, a recommendation failure, and the boundary score of 70.
Lab 2: Intelligent Agents
This lab is about intelligent agents and the PEAS framework. I made a smart classroom agent. It remembers its last mode and only sends a new command when the mode changes.
Run it with python "lab2 (1).py". The summary is in lab 2 summary.docx. All 6 tests pass, repeats, the 20 and 26 boundaries, a mode change, and an empty room.
Lab 3: Uninformed Search
I built BFS, DFS, DLS, IDDFS and UCS from scratch, on a small building map.
The report in lab 3 summary.docx has the hand traced BFS and DFS frontiers, DLS and IDDFS results at limits 1 to 4, and the weighted graph UCS experiment.
Run it with python lab3.py. All 7 checks pass, visit orders, DLS and IDDFS limits, the UCS cost 3 path with an independent cost check, the BFS vs UCS comparison, and the edge cases.
Lab 4: Informed Search
A star search with a heuristic, on the campus graph S, A, B, C, G. I compared it with UCS, which uses a zero heuristic, and I also tried h(C) = 10, which is an overestimate.
Files are lab4.py and lab 4 summary.docx.
Run it with python lab4.py. A star finds S to A to C to G at cost 6 and expands 3 nodes. UCS finds the same path and cost but expands 4. The overestimate gives the cost 9 route, S to B to G. All checks pass.
Lab 5: Adversarial Search
Minimax and alpha-beta pruning on a small game tree. I did a hand trace, counted leaves for both methods, and tried reordering the branches.
Files are lab5.py and lab 5 summary.docx.
Run it with python lab5.py. The hand trace and every run give root value 5. Minimax checks all 8 leaves. Alpha-beta checks 5 or 7 leaves after reordering, so pruning saves work without changing the answer. All 7 checks pass.
Lab 6: NLP Fundamentals
Tokenization, embeddings and text chunking. I compared tokens on 6 inputs, made a FAQ chatbot, tried word window and sentence aware chunking, and ran TF-IDF retrieval on a help desk corpus.
Files are lab6.py and lab 6 summary.docx.
Run it with python lab6.py. I picked sentence aware packing, 22 chunks, 0 repeated words, 8 out of 8 evidence kept whole, best dev Hit at 3 is 1.0 and MRR at 3 is 0.833. All checks pass with exit 0. The embedding backend could not run here, so I wrote that down as a limitation.
