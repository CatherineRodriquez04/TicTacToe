
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

class TicTacToe:
    def __init__(game):
        game.board = [' ']*9 #3x3 board
        game.win_combo = [ 
            (0, 1, 2),(3, 4, 5), (6, 7, 8),   # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        game.player1 = None
        game.player2 = None
        game.player1Name = None
        game.player2Name = None
        game.ai = 0
        
    #current state of board
    def print_board(game):
        print("-----------")
        print(" " + game.board[0] + " | " + game.board[1] + " | " + game.board[2])
        print("-----------")
        print(" " + game.board[3] + " | " + game.board[4] + " | " + game.board[5])
        print("-----------")
        print(" " + game.board[6] + " | " + game.board[7] + " | " + game.board[8])
        print("-----------")
        
    #checks if player won the game
    def winner(game, player):
        if player is None:
            return False
        for combo in game.win_combo:
            if all(game.board[i] == player for i in combo):
                return True
        return False
        
    #checks for space on the board
    def board_full(game):
        return ' ' not in game.board 
    
    #checks if the game is over by a player winning or the board is full
    def game_over(game):
        return game.winner(game.player1) or game.winner(game.player2) or game.board_full()
    
    def make_move(game, position, player):
        #placeholder for ai against ai
        if position in range(9) and game.board[position] == ' ':
            game.board[position] = player
            return True #successful move 
        else:
            return False #unsuccessful move -> position occupied
        
    def undo_move(self, position):
        self.board[position] = ' '
        
    #list of indices where board has empty spaces
    def available_moves(game): 
        return [i for i, v in enumerate(game.board) if v == ' ']
    
    #determine best move using alpha beta pruning
    def minimax_alpha_beta(game, depth, alpha, beta, maximizingPlayer):
        if game.game_over() or depth == 0:
            if game.winner(game.player2):
                return 10 - depth, None #ai wins
            elif game.winner(game.player1):
                return -10 + depth, None #player wins
            else:
                return 0, None #tied game

        #maximize ai
        if maximizingPlayer:
            max_eval = float('-inf')
            best_move = None
            #evaluates each move for best board state
            for move in game.available_moves():
                if (game.ai == 1):
                    game.make_move(move, game.player2)
                else:
                    game.make_move(move, game.player1)
                eval, _ = game.minimax_alpha_beta(depth - 1, alpha, beta, False)
                game.undo_move(move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break #beta cutoff
            return max_eval, best_move
        #minimize player
        else:
            min_eval = float('inf')
            best_move = None
            for move in game.available_moves():
                game.make_move(move, game.player1)
                eval, _ = game.minimax_alpha_beta(depth - 1, alpha, beta, True)
                game.undo_move(move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break #alpha cutoff
            return min_eval, best_move

    #ai makes move based on minimax algorithm
    def play_ai(game):
        _, best_move = game.minimax_alpha_beta(len(game.available_moves()), float('-inf'), float('inf'), True)
        print("AI plays at position:", best_move)
        if(game.ai == 1):
            game.make_move(best_move, game.player1)
        else:
            game.make_move(best_move, game.player2)
        
#creates a new instance of TicTacToe   
game = TicTacToe()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/choose_symbol', methods=['POST'])
def choose_symbol():
    data = request.get_json()
    symbol = data['symbol']
    
    if symbol == 'X':
        game.player1 = 'X'
        game.player2 = 'O'
    elif symbol == 'O':
        game.player1 = 'O'
        game.player2 = 'X'

    return jsonify(message=f'Symbol {symbol} chosen successfully')

if __name__ == '__main__':
    app.run(debug=True)