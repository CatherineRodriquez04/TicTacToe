#CSC 4444 Final Project
#Catherine Rodriquez and Shalvi Dalal

import time
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
                    game.make_move(move, game.player1)
                else:
                    game.make_move(move, game.player2)
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
        return 0, None

    #ai makes move based on minimax algorithm
    def play_ai(game):
        _, best_move = game.minimax_alpha_beta(len(game.available_moves()), float('-inf'), float('inf'), True)
        print("AI plays at position:", best_move)
        game.make_move(best_move, game.player2)
    
    #ai against ai
    def play_ai1_strategy(game):
        _, best_move = game.minimax_alpha_beta(len(game.available_moves()), float('-inf'), float('inf'), True)
        print(f"{game.player1Name} plays at position:", best_move)
        game.make_move(best_move, game.player1)

    def play_ai2_strategy(game):
        _, best_move = game.minimax_alpha_beta(len(game.available_moves()), float('-inf'), float('inf'), True)
        print(f"{game.player2Name} plays at position:", best_move)
        game.make_move(best_move, game.player2)
        
        
#creates a new instance of TicTacToe   
game = TicTacToe()
print("\n❌⭕ Welcome to TicTacToe! ❌⭕")
print("You can select between 3 game mode options\n\t1. Two Player\n\t2. Play Against Ai\n\t3. Ai Against Ai\n\t4. See Board Positions")
option = True
continue_game = True
while continue_game:
    option = True
    while option:
        game_option = int(input("Please select how you would like to play(1-4): "))
        #two player game
        if (game_option == 1):
            game.ai = 0 #placeholder
            game.player1Name = input("Enter Player1 Name: ")
            game.player2Name = input("Enter Player2 Name: ")
            player_choice = input(f"{game.player1Name} please choose X or O: ").upper()
            if player_choice == 'X':
                game.player1 = 'X'
                game.player2 = 'O'
            else:
                game.player1 = 'O'
                game.player2 = 'X'
            while not game.game_over():  
                game.print_board()
                correct_input = True
                available_moves = game.available_moves()
                while correct_input:
                    player_move = int(input(f"{game.player1Name} position (0-8): "))
                    if(player_move >= 9):
                        print(f"{player_move} position does not exist.")
                    elif(player_move not in available_moves):
                        print(f"{player_move} is already taken.")
                    else:
                        correct_input = False
                correct_input = True
                game.make_move(player_move, game.player1)
                if (game.game_over() == True):
                    break
                game.print_board()
                available_moves = game.available_moves()
                while correct_input:
                    player_move = int(input(f"{game.player2Name} position (0-8): "))
                    if(player_move >= 9):
                        print(f"{player_move} position does not exist.")
                    elif(player_move not in available_moves):
                        print(f"{player_move} is already taken.")
                    else:
                        correct_input = False
                game.make_move(player_move, game.player2)
                print()
            option = False
        #game against ai
        elif (game_option == 2):
            game.ai = 0 #placeholder
            game.player1Name = input("Enter Player Name: ")
            game.player2Name = "AI"
            # Prompt the player to choose X or O
            player_choice = input(f"{game.player1Name} please choose X or O: ").upper()
            if player_choice == 'X':
                game.player1 = 'X'
                game.player2 = 'O'
            else:
                game.player1 = 'O'
                game.player2 = 'X'
            # Main game loop for option 2
            while not game.game_over():  
                game.print_board()
                correct_input = True
                available_moves = game.available_moves()
                while correct_input:
                    player_move = int(input(f"{game.player1Name} position (0-8): "))
                    if(player_move >= 9):
                        print(f"{player_move} position does not exist.")
                    elif(player_move not in available_moves):
                        print(f"{player_move} is already taken.")
                    else:
                        correct_input = False
                game.make_move(player_move, game.player1)
                game.play_ai()  
                print()
            option = False
        #ai against ai
        elif (game_option == 3):
            game.player1Name = "AI-1"
            game.player1 = 'X'
            game.player2Name = "AI-2"
            game.player2 = 'O'
            correct_input = True
            while correct_input:
                    first_position = int(input("\nPlease enter starting position for AI-1 (0-8): "))
                    if(first_position >= 9):
                        print(f"{first_position} position does not exist.")
                    else:
                        correct_input = False
            correct_input = True
            while correct_input:
                    second_position = int(input("\nPlease enter starting position for AI-2 (0-8): "))
                    if(second_position >= 9):
                        print(f"{second_position} position does not exist.")
                    elif(second_position == first_position):
                        print(f"{second_position} is already taken.")
                    else:
                        correct_input = False
            print()
            game.make_move(first_position, game.player1)
            print(f"{game.player1Name} starts at position {first_position}")
            game.print_board()
            print()
            time.sleep(1)
            game.make_move(second_position, game.player2)
            print(f"{game.player2Name} starts at position {second_position}")
            game.print_board()
            print()
            
            time.sleep(1)
            while not game.game_over():  
                game.ai = 0 #placeholder
                game.play_ai1_strategy()
                game.print_board()
                time.sleep(1) #delay between moves
                if not game.game_over():
                    game.ai = 1 #placeholder
                    game.play_ai2_strategy()
                    game.print_board()
                    time.sleep(1) #delay between moves
                print()
            option = False
        #see board positions
        elif (game_option == 4):
            print("\nBoard Positions:")
            print("-----------")
            print(" " + "0" + " | " + "1" + " | " + "2")
            print("-----------")
            print(" " + "3" + " | " + "4" + " | " + "5")
            print("-----------")
            print(" " + "6" + " | " + "7" + " | " + "8")
            print("-----------\n")
            
        #invalid input for game options
        else:
            print("Invalid input. PLease enter a mode option 1-4")
            
    #print the final state of the board
    print("End Result:")
    game.print_board()

    #determine the winner and print the result
    if game.winner(game.player1):
        print(f"{game.player1Name} wins!👑\n")
        print(f"{game.player2Name} lost!😔")
    elif game.winner(game.player2):
        print(f"{game.player2Name} wins!👑\n")
        print(f"{game.player1Name} lost!😔")
    else:
        print("It's a draw!") 
        
    #ask if the player wants to play again
    play_again = input("\nWould you like to play again? (yes/no): ")
    if play_again.lower() != 'yes':
        continue_game = False

    #reset the game for a new round
    game.board = [' ']*9 
    
print("\nThank you for playing my TicTacToe Game!😊\n")