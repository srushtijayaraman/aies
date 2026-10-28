# AI & Expert Systems Lab — Independent Codes

Each script is a standalone program. You can run it independently; do not combine the files into one program.

## Quick start

1. Install Python 3.10+.
2. Extract this folder.
3. Open a terminal in the folder and run a script with `python path/to/script.py`.
4. The state-space, A*, local-search, CSP, Minimax, Prolog, and rule-based chatbot examples use the Python standard library (except the Prolog file).

## Assignment mapping

### Assignment 0 / State-space search
- `01_State_Space/01_tower_of_hanoi.py` — recursive Tower of Hanoi; minimal `2^n - 1` moves.
- `01_State_Space/02_missionaries_cannibals_bfs.py` — BFS shortest safe river-crossing solution.
- `01_State_Space/03_water_jug_bfs.py` — BFS shortest sequence for the 4L/3L jugs and target 2L.
- `01_State_Space/04_graph_bfs_dfs.py` — generic graph-search illustration of BFS and DFS.

### Assignment 1 — A* 8-puzzle
- `02_Astar/05_eight_puzzle_astar.py` — A* with Manhattan distance, solvability check, parent tracking, and optimal move count.
- Enter nine values 0..8; 0 is the blank. Press Enter to use the included 2-move demonstration.

### Assignment 2 — Hill climbing / local search
- `03_Local_Search/06_tsp_hill_climbing_2opt.py` — steepest-descent 2-opt Hill Climbing, with random restarts.
- `03_Local_Search/07_tsp_exact_held_karp.py` — optional exact TSP DP solver; unlike Hill Climbing, gives a global optimum for small instances. Time/memory grow exponentially.
- `03_Local_Search/08_n_queens_min_conflicts.py` — N-Queens local search with min-conflicts and randomized restarts.
- `03_Local_Search/09_tsp_genetic_algorithm.py` — optional TSP genetic algorithm with tournament selection, order crossover, mutation, and elitism.

### Assignment 3 — CSP / cryptarithmetic
- `04_CSP/09_send_more_money.py` — column-by-column backtracking for SEND + MORE = MONEY.
- `04_CSP/10_cross_roads_danger.py` — column-by-column backtracking for CROSS + ROADS = DANGER.

### Assignment 4 — Minimax
- `05_Minimax/11_tic_tac_toe_minimax_alphabeta.py` — playable Tic-Tac-Toe, human X vs AI O, Minimax with alpha-beta pruning and good move ordering.

### Assignment 5 — Expert system
- `06_Expert_System/12_expert_system_prolog.pl` — Prolog facts/rules. With SWI-Prolog, load using `?- consult('12_expert_system_prolog.pl').` from this folder (or use the file's full path), then query `?- recommendation(X).` Press `;` to see alternate answers.
- `06_Expert_System/13_expert_system_python.py` — interactive Python equivalent for demonstration. The assignment sheet asks for Prolog, so use the `.pl` program for the Prolog requirement.

### Assignment 6 — Chatbot / NLP
- `07_Chatbot/14_chatbot_rule_based.py` — short no-dependency chatbot using simple text rules.
- `07_Chatbot/15_chatbot_tfidf_sklearn.py` — optional learned-intent chatbot using TF-IDF + logistic regression. Install it with `python -m pip install scikit-learn`.

### Assignment 7 — Face detection / recognition
- `08_Face_Vision/16_face_detection_haar.py` — Haar cascade face detection (traditional ML, **not** a neural network).
- `08_Face_Vision/17_face_detection_yunet_dnn.py` — neural-network face detection with YuNet.
- `08_Face_Vision/18_face_match_yunet_sface.py` — compares two images using a neural-network detector and SFace face embeddings. Use only images you have permission to process; similarity is not proof of identity.

## Vision dependencies and model files

Install OpenCV:

```bash
python -m pip install opencv-python
```

Put an image named `face.jpg` next to the script, or pass a path to the Haar or YuNet detection scripts:

```bash
python 08_Face_Vision/16_face_detection_haar.py face.jpg
python 08_Face_Vision/17_face_detection_yunet_dnn.py face.jpg
```

The Haar cascade XML is included with the OpenCV Python package. The YuNet and SFace programs require ONNX files downloaded separately from the official OpenCV Zoo model folders:

- YuNet face detector (`face_detection_yunet_2023mar.onnx`): https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet
- SFace face recognizer (`face_recognition_sface_2021dec.onnx`): https://github.com/opencv/opencv_zoo/tree/main/models/face_recognition_sface

Place both ONNX files beside `18_face_match_yunet_sface.py`. Also put two images called `face1.jpg` and `face2.jpg` in the same folder before running the comparison script.

## Important correctness notes

- BFS returns shortest paths when every action has equal cost.
- A* with Manhattan distance is optimal for the standard 8-puzzle when implemented with correct costs and reopening improved states (done here).
- Hill Climbing is a local optimizer and **does not guarantee** the global TSP optimum; random restarts help. Use the Held-Karp file when the assignment specifically expects a provably optimal small TSP answer.
- CSP scripts enforce distinct digits, nonzero leading letters, and column carries; both solve the puzzle rather than hard-code the answer.
- Minimax with alpha-beta is optimal for Tic-Tac-Toe given perfect play and the implemented terminal scores.
- The Prolog and Python expert systems are rule-based demonstrations, not learning systems.
- The rule-based chatbot is the easiest to run; the scikit-learn chatbot is optional and needs its dependency.
- Face detection finds face locations; face matching compares two face images. These are different from naming/identifying a person with certainty.
