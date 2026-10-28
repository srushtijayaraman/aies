"""Playable Tic-Tac-Toe: human X, optimal computer O, Minimax + alpha-beta."""
HUMAN, AI, EMPTY = "X", "O", " "
WIN_LINES = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
MOVE_ORDER = (4, 0, 2, 6, 8, 1, 3, 5, 7)  # good moves first for alpha-beta pruning

def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None

def minimax(board, maximizing, depth, alpha, beta):
    result = winner(board)
    if result == AI:
        return 10 - depth
    if result == HUMAN:
        return depth - 10
    if EMPTY not in board:
        return 0
    if maximizing:  # AI O maximises the score
        best = -float("inf")
        for i in MOVE_ORDER:
            if board[i] == EMPTY:
                board[i] = AI
                best = max(best, minimax(board, False, depth+1, alpha, beta))
                board[i] = EMPTY
                alpha = max(alpha, best)
                if alpha >= beta:
                    break
        return best
    best = float("inf")
    for i in MOVE_ORDER:
        if board[i] == EMPTY:
            board[i] = HUMAN
            best = min(best, minimax(board, True, depth+1, alpha, beta))
            board[i] = EMPTY
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best

def best_ai_move(board):
    best_score, best_move = -float("inf"), None
    for i in MOVE_ORDER:
        if board[i] == EMPTY:
            board[i] = AI
            score = minimax(board, False, 1, -float("inf"), float("inf"))
            board[i] = EMPTY
            if score > best_score:
                best_score, best_move = score, i
    return best_move

def show(board):
    cells = [str(i+1) if x == EMPTY else x for i, x in enumerate(board)]
    print(f" {cells[0]} | {cells[1]} | {cells[2]}\n---+---+---\n {cells[3]} | {cells[4]} | {cells[5]}\n---+---+---\n {cells[6]} | {cells[7]} | {cells[8]}\n")

if __name__ == "__main__":
    board = [EMPTY] * 9
    print("You are X; the computer is O. Choose a cell from 1 to 9.")
    show(board)
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
            if not 0 <= move < 9 or board[move] != EMPTY:
                print("That cell is not available. Try again.")
                continue
        except EOFError:
            print("\nInput ended; game stopped.")
            break
        except ValueError:
            print("Please enter a number from 1 to 9.")
            continue
        board[move] = HUMAN
        show(board)
        if winner(board) == HUMAN:
            print("You win!"); break
        if EMPTY not in board:
            print("Draw!"); break
        ai_move = best_ai_move(board)
        board[ai_move] = AI
        print(f"Computer chooses cell {ai_move+1}.")
        show(board)
        if winner(board) == AI:
            print("Computer wins."); break
        if EMPTY not in board:
            print("Draw!"); break
