# Rule-based Tic-tac-toe AI that can't lose

# Board representation (0-8 positions) 
# 0 | 1 | 2 
# --------- 
# 3 | 4 | 5 
# --------- 
# 6 | 7 | 8 

class TicTacToe:
    def __init__(self):
        # setup board
        # list of 9 positions (0-8)
        # empty pos = ' '
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'

        # list of all winning combos
        self.winning_combos = [
            [0,1,2], # top row
            [3,4,5], # mid row
            [6,7,8], # bottom row
            [0,3,6], # left col
            [1,4,7], # mid col
            [2,5,8], # right col
            [0,4,8], # diag TL to BR
            [2,4,6]  # diag TR to BL
        ]

    ### HELPERS ###
    # func display board
    # show each value in each position
    def display_board(self):
        """Display the current board state"""
        print("\n")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("-----------")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("-----------")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("\n")

    # display positions for ref
    def display_pos(self):
        """Show position IDs for reference when making a move"""
        print("\nPosition IDs:")
        print(" 0 | 1 | 2 ")
        print("-----------")
        print(" 3 | 4 | 5 ")
        print("-----------")
        print(" 6 | 7 | 8 ")
        print("\n")

    # func is valid move
    # check if pos is occupied
    def is_valid_move(self, position):
        """Check if a move is valid"""
        return 0 <= position <= 8 and self.board[position] == ' '
    
    # func make move
    # if valid, set board pos to player symbol
    def make_move(self, position, player):
        """Place a player's symbol on the board"""
        if self.is_valid_move(position):
            self.board[position] = player
            return True
        return False
    
    # func check winner
    # for each combo in winning combo
    # if symbols match in all board pos, then there is a winner
    # else no winner
    def check_winner(self):
        """Check the board for winning combo"""
        for combo in self.winning_combos:
            if(self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' '):
                return self.board[combo[0]]
        return None

    # func is board full
    def is_board_full(self):
        """Check if the board is completely filled"""
        return ' ' not in self.board
    
    def get_empty_positions(self):
        """Return list of empty positions"""
        return [i for i in range(9) if self.board[i] == ' ']
    
    # ========== AI Logic Start ========== #

    # func find_winning_move(self, player)
    def find_winning_move(self, player):
        """Find a position that wins the game or blocks opponent"""
        # FOR each winning combo
        for combo in self.winning_combos:
            positions = [self.board[i] for i in combo]

            # if 2 positions have the same symbol and one is empty
            if positions.count(player) == 2 and positions.count(' ') == 1:
                # find and return empty pos
                for i in combo:
                    if self.board[i] == ' ':
                        return i
        # RETURN None
        return None

    # func find_fork(board, symbol)
    def find_fork(self, player):
        """Find a position that creates a fork (two winning threats simultaneously)"""
        empty_pos = self.get_empty_positions()

        # FOR each empty position:
        for pos in empty_pos:
            # Place symbol temporarily
            self.board[pos] = player

            # Count how many winning patterns now have exactly 2 of our symbols 
            winning_threats = 0
            for combo in self.winning_combos:
                positions = [self.board[i] for i in combo]
                if positions.count(player) == 2 and positions.count(' ') == 1:
                    winning_threats += 1
        
            # Remove temporary symbol 
            self.board[pos] = ' '

            # IF winning_threats >= 2 THEN this is a fork
            if winning_threats >= 2:
                return pos
            
        return None

    # func block_opp_fork
    def block_opp_fork(self, ai_symbol, opp_symbol):
        """Block opponent's fork opprotunity while alos prioritizing two-in-a-row where possible"""
        empty_pos = self.get_empty_positions()
        fork_threats = []

        # find all pos where opp could fork
        # repeat of find_fork
        for pos in empty_pos:
            self.board[pos] = opp_symbol

            winning_threats = 0
            for combo in self.winning_combos:
                positions = [self.board[i] for i in combo]
                if positions.count(opp_symbol) == 2 and positions.count(' ') == 1:
                    winning_threats += 1
            
            self.board[pos] = ' '

            if winning_threats >= 2:
                fork_threats.append(pos)
        
        if not fork_threats:
            return None
        
        # try to find a blocking move that creates a two-in-a-row
        # force opp to defend instead of creating a fork
        for pos in empty_pos:
            if pos in fork_threats:
                continue

            # temp placement
            self.board[pos] = ai_symbol

            # check for two-in-a-row
            for combo in self.winning_combos:
                positions = [self.board[i] for i in combo]
                if positions.count(ai_symbol) == 2 and positions.count(' ') == 1:
                    self.board[pos] = ' '
                    return pos
                
            # remove temp placement
            self.board[pos] = ' '

        # no two-in-a-row possible
        # just block a fork
        return fork_threats[0]
    
    # def get_ai_move(self, ai_symbol):
    def get_ai_move(self, ai_symbol):
        """Main AI Function - evaluates rules in priority order"""
        opp_symbol = 'X' if ai_symbol == 'O' else 'O'

        # Priority 1: Check for winning move 
        move = self.find_winning_move(ai_symbol) 
        # IF move exists THEN RETURN move
        if move is not None:
            return move, "Winning move"

        # Priority 2: Block opponent's winning move 
        move = self.find_winning_move(opp_symbol) 
        # IF move exists THEN RETURN move 
        if move is not None:
            return move, "Blocking opponent's winning move"
        
        # Priority 3: Create a fork
        move = self.find_fork(ai_symbol) 
        # IF move exists THEN RETURN move 
        if move is not None:
            return move, "Creating fork"
        
        # Priority 4: Block opponent's fork 
        move = self.block_opp_fork(ai_symbol, opp_symbol) 
        # IF move exists THEN RETURN move 
        if move is not None:
            return move, "Blocking opponent's fork"
        
        # Priority 5: Take center 
        # IF board[4] is empty THEN RETURN 4
        if self.board[4] == ' ':
            return 4, "Taking center"
        
        # Priority 6: Take opposite corner
        corner_pairs = [(0,8), (8,0), (2,6), (6,2)]
        # FOR each corner, opposite IN corners: 
        for corner, oppo in corner_pairs:
            # IF board[corner] == opponent_symbol AND board[opposite] is empty 
            if self.board[corner] == opp_symbol and self.board[oppo] == ' ':
                # THEN RETURN opposite
                return oppo, "Taking opposite corner"
        
        # Priority 7: Take any empty corner
        corners = [0,2,6,8]
        # FOR corner IN [0, 2, 6, 8]:
        for corner in corners:
            # IF board[corner] is empty
            if self.board[corner] == ' ':
                # THEN RETURN corner
                return corner, "Taking corner" 
        
        # Priority 8: Take any empty side 
        sides = [1,3,5,7]
        # FOR side IN [1, 3, 5, 7]: 
        for side in sides:
            # IF board[side] is empty
            if self.board[side] == ' ':
                # THEN RETURN side
                return side, "Taking side"
            
        # Should never reach here if board has empty spaces
        return None, "No move available"
    
# Main gameplay loop
def play_game():
    """Main gameplay loop"""
    game = TicTacToe()

    # Welcome
    print("=" * 50)
    print("Welcome to rule-based Tic-Tac-Toe!")
    print("=" * 50)

    # Choose 1P
    print("\nWho should go first?")
    print("1. You (X)")
    print("2. AI (O)")

    while True:
        try:
            choice = input("\nEnter 1 or 2: ").strip()
            if choice in ['1','2']:
                ai_goes_first = (choice == '2')
                break
            else:
                print("Please enter 1 or 2")
        except:
            print("Invalid input. Please enter 1 or 2")

    # Prime gameplay loop
    game.display_pos()
    player_symbol = 'X'
    ai_symbol = 'O'
    current_turn = 'AI' if ai_goes_first else 'player'

    # Gameplay loop
    while True:
        game.display_board()

        if current_turn == 'player':
            # player turn
            print("Your turn (X)")
            while True:
                try:
                    pos = int(input("Enter position (0-8): "))
                    if game.make_move(pos, player_symbol):
                        break
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 8")
            
            current_turn = 'AI'
        else:
            # AI's turn
            print("AI's turn (O)")
            move, reason = game.get_ai_move(ai_symbol)
            if move is not None:
                game.make_move(move, ai_symbol)
                print(f"AI plays position {move} - Strategy: {reason}")

            current_turn = 'player'
        
        # Check for winner each turn
        winner = game.check_winner()
        if winner:
            game.display_board()
            if winner == player_symbol:
                print("Congratulations! You won!")
            else:
                print("AI wins! Beep Boop...")
            break

        # check for draw
        if game.is_board_full():
            game.display_board()
            print("It's a DRAW! Well played!")
            break

    # Play again?
    play_again = input("\nPlay again? (y/n): ").strip().lower()
    if play_again == 'y':
        play_game()
    else:
        print("\nThanks for playing! Goodbye!")

# init
if __name__ == "__main__":
    play_game()