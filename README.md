Lab 1 is about symbolic vs probability-based AI, using a scholarship screening checker that keeps score >= 70 and complete documents, and adds deadline met and recommendation present as two new rules.
Run the code in lab1 (1).py with python "lab1 (1).py" and see the project summary in lab 1 summary.docx; all 4 tests pass, including a pass, a deadline failure, a recommendation failure, and the boundary score of 70.
Lab 2 is about intelligent agents and the PEAS framework, using a smart classroom agent that remembers its last mode and only sends a new command when the mode changes.
Run the code in lab2 (1).py with python "lab2 (1).py" and see the full summary and trace in lab 2 summary.docx; all 6 tests pass, including repeats, the 20 and 26 boundaries, a mode change, and an empty room.
Lab 3 implements uninformed search from scratch: BFS, DFS, DLS, IDDFS and UCS on a small building map.
The report (lab 3 summary.docx) holds the hand-traced BFS/DFS frontiers, DLS/IDDFS results at limits 1-4, and the weighted-graph UCS experiment.
Run the code with: python lab3.py
All 7 checks pass: visit orders, DLS/IDDFS limits, the UCS cost-3 path with independent cost check, the BFS-vs-UCS comparison, and the edge cases.
