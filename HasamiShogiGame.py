# Author: Adam Heidrick
# Date: 21 November 2021
# Description: Project-9 Portfolio Project: Hasami Shogi Game


class Player:
    """This class represents a Player object that is referenced by the HasamiShogiGame class to get and set player
     data. It is used to validate moves and captures; it also keeps track of how many pawns have been taken
     during gameplay."""

    def __init__(self, color, marker):
        """Initializes with two parameters: color and marker. Soldiers represents number of pieces lost during the game
        during a capture event in the HasamiShogiGame class"""
        self._color = color
        self._soldiers = 0
        self._marker = marker

    def get_color(self):
        """Returns the color of the player which will be BLACK or RED as determined by the HasamiShogiGame class"""
        return self._color

    def get_soldiers(self):
        """Returns the number of soldiers lost during the game when called"""
        return self._soldiers

    def get_marker(self):
        """Returns a marker for the game board: 'B' for Black and 'R' for RED as determined by the
        HasamiShogiGame class"""
        return self._marker

    def set_soldiers(self, amount):
        """Sets the amount of soldiers lost during a capture event in the HasamiShogiGame class"""
        self._soldiers += amount


def game_board():
    """This static function serves to initialize a game board for the HasamiShogiGame class"""
    board = {"a": [], "b": [], "c": [], "d": [], "e": [], "f": [], "g": [], "h": [], "i": []}
    for key in board.keys():
        for num in range(1, 10):
            if key == "a":  # First row filled with Player One's token: B
                board[key].append(" R ")
            elif key == "i":  # Last row filled with Player Two's token: R
                board[key].append(" B ")
            else:
                board[key].append(" . ")
    return board


class HasamiShogiGame:
    """THis object represents the attributes, methods, and mechanics required to play the Hasami Shogi Game variant 1"""

    def __init__(self):
        """Initializes with player1 and player2 objects, sets color and marker, sets game state, sets active player
        to player 1, and initializes a board using a game_board function."""
        self._player1 = Player("BLACK", ' B ')
        self._player2 = Player("RED", ' R ')
        self._game_state = 'UNFINISHED'
        self._active_player = self._player1
        self._board = game_board()
        # self._board = board_h

    def print_board(self):
        """This function print's the game board"""
        column = "   1   2   3   4   5   6   7   8   9"
        print(column)
        for key, value in self._board.items():
            print(key, ' '.join(value))  # Removes brackets and quotation marks for an more readable board.

    def get_game_state(self):
        """Returns the game state: UNFINISHED, RED_WON, or BLACK_WON"""
        return self._game_state

    def get_active_player(self):
        """Returns Active Player's color"""
        return self._active_player.get_color()

    def set_active_player(self, active_player):
        """Sets the active player, used at end of turn"""
        self._active_player = active_player

    def get_num_captured_pieces(self, color):
        """Returns number of soldiers from player's soldier list, requires the players color to return"""
        if color.upper() == 'BLACK':
            return self._player1.get_soldiers()
        else:
            return self._player2.get_soldiers()

    """ What Follows is the move checks to ensure the player move is valid and if the move results in a capture."""

    def horizontal_move(self, source_row, source_column, destination_column):
        """This function checks for valid horizontal movement of left and right of the move destination"""

        if destination_column < source_column:  # This is a move to the left
            for move in range(source_column - 2, destination_column - 2, -1):
                if self._board[source_row][move] != ' . ':
                    return True

        else:  # This is a move to the right
            for move in range(source_column, destination_column):
                if self._board[source_row][move] != ' . ':
                    return True

    def horizontal_capture(self, source_row, destination_row, source_column, destination_column):
        """This function checks the horizontal spaces to determine a horizontal capture, if a capture is determined
        Then capture helper functions are called"""
        custodian_capture = False

        """ A horizontal capture also needs to be checked upon a vertical move, so the next two blocks check that"""
        if destination_column == source_column:
            for index in range(destination_column, 9):  # iterates right to determine capture
                if self._board[destination_row][index] == ' . ':
                    custodian_capture = False
                    break
                elif self._board[destination_row][index] == self._active_player.get_marker():
                    self.horizontal_right_capture(destination_column, index, destination_row)  # Cap right call
                    custodian_capture = True
                    break

            for index in range(destination_column - 2, -1, -1):  # iterates left to determine capture
                if self._board[destination_row][index] == ' . ':
                    custodian_capture = False
                    break
                elif self._board[destination_row][index] == self._active_player.get_marker():
                    self.horizontal_left_capture(destination_column - 2, index + 1, destination_row)  # Cap Left Call
                    custodian_capture = True
                    break

        """The rest of the code blocks determine a capture for both left and right of the destination space"""
        if destination_column >= source_column:
            for index in range(destination_column, 9):  # iterates right
                if self._board[destination_row][index] == ' . ':
                    custodian_capture = False
                    break

                elif self._board[destination_row][index] == self._active_player.get_marker():
                    self.horizontal_right_capture(destination_column, index, source_row)
                    custodian_capture = True
                    break

        if destination_column <= source_column:
            for index in range(destination_column - 2, -1, -1):  # iterates left
                if self._board[destination_row][index] == ' . ':
                    custodian_capture = False
                    break

                elif self._board[destination_row][index] == self._active_player.get_marker():
                    self.horizontal_left_capture(destination_column - 2, index + 1, source_row)
                    custodian_capture = True
                    break

        return custodian_capture

    def horizontal_right_capture(self, destination_column, index, source_row):
        """This function calculates how many pieces are being captured in a horizontal right move, updates the game
        board, and updates player's soldier count"""
        grave_yard = 0

        for num in range(destination_column, index):
            grave_yard += 1
            self._board[source_row][num] = ' . '

        if self._active_player.get_color() == "BLACK":
            self._player2.set_soldiers(grave_yard)

        else:
            self._player1.set_soldiers(grave_yard)

    def horizontal_left_capture(self, destination_column, index, source_row):
        """This function calculates how many pieces are being captured in a horizontal left move, updates the game
        board, and updates player's soldier count"""
        grave_yard = 0
        for num in range(destination_column, index - 1, -1):
            grave_yard += 1
            self._board[source_row][num] = ' . '

        if self._active_player.get_color() == "BLACK":
            self._player2.set_soldiers(grave_yard)
        else:
            self._player1.set_soldiers(grave_yard)

    def vertical_move(self, source_row, destination_row, column):
        """This function checks for valid vertical movement of up and down of the move destination"""
        row_key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        move_key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
        row = row_key[source_row]
        row_dest = row_key[destination_row]

        if row > row_dest:  # Player is moving up
            for move in range(row - 1, row_dest - 1, -1):
                if self._board[move_key[move]][column - 1] != ' . ':
                    return True

        else:  # Player is moving down
            for move in range(row + 1, row_dest + 1):
                if self._board[move_key[move]][column - 1] != ' . ':
                    return True

    def vertical_capture(self, source_row, destination_row, destination_column):
        """This function determines if a capture will take place by checking vertical position up and down of the
        players movement destination"""
        row_key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8}
        move_key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
        source = row_key[source_row]
        row = row_key[destination_row]
        custodian_capture = False

        # This checks if the capture is possible
        if source >= row != 0:
            # This checks the tokens above the destination
            if self._board[move_key[row - 1]][destination_column - 1] == ' . ' or \
                    self._board[move_key[row - 1]][destination_column - 1] == self._active_player.get_marker():
                custodian_capture = False
            else:  # Iterates up until player token is met to pass that range into the capture function
                for index in range(row - 1, -1, -1):  # -1 to include 0 and -1 to go in reverse
                    if self._board[move_key[index]][destination_column - 1] == ' . ':
                        break
                    elif self._board[move_key[index]][destination_column - 1] == self._active_player.get_marker():
                        self.vertical_up_capture(row - 1, index + 1, destination_column - 1)
                        custodian_capture = True
                        break

        if source <= row != 8:
            # If row is 8, then a key error will occur which means a
            # This checks the token below the destination
            if self._board[move_key[row + 1]][destination_column - 1] == ' . ' or \
                    self._board[move_key[row + 1]][destination_column - 1] == self._active_player.get_marker():
                custodian_capture = False

            else:  # Iterates down until player token is met to pass that range into the capture function
                for index in range(row + 1, 9):
                    if self._board[move_key[index]][destination_column - 1] == ' . ':
                        break
                    elif self._board[move_key[index]][destination_column - 1] == self._active_player.get_marker():
                        self.vertical_down_capture(row + 1, index - 1, destination_column - 1)
                        custodian_capture = True
                        break

        return custodian_capture

    def vertical_up_capture(self, row, index, destination_column):
        """This function calculates how many pieces are being captured in a vertical up move, updates the game board,
        and updates players soldier count (how many solders that player has lost"""
        grave_yard = 0
        move_key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}
        for num in range(index, row + 1):
            grave_yard += 1
            self._board[move_key[num]][destination_column] = ' . '

        if self._active_player.get_color() == "BLACK":
            self._player2.set_soldiers(grave_yard)
        else:
            self._player1.set_soldiers(grave_yard)

    def vertical_down_capture(self, row, index, destination_column):
        """This function calculates how many pieces are being captured in a vertical down move, updates the game board,
        and updates player's soldier count"""
        grave_yard = 0
        move_key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i'}

        for num in range(row, index + 1):
            grave_yard += 1
            self._board[move_key[num]][destination_column] = ' . '

        if self._active_player.get_color() == "BLACK":
            self._player2.set_soldiers(grave_yard)
        else:
            self._player1.set_soldiers(grave_yard)

    def corner_capture(self, destination_row, destination_column):
        """This function iterates through the corners to validate and execute any corner captures"""
        position = destination_row + str(destination_column)
        move_check = ['b1', 'a2', 'a8', 'b9', 'h9', 'i8', 'i2', 'h1']  # All positions for corner capture
        corners = ['a1', 'a9', 'i9', 'i1']  # These are the corner coordinates
        corner_index = [0, 8, 8, 0]  # These are the corner indexes used for iteration loop below
        corner_capture = False  # Used for front end: if corner capture True return a message indicating a capture.

        # This determines who the opponent is for counting taken pawns and board position checks.
        if self.get_active_player() == 'BLACK':
            opponent = self._player2
        else:
            opponent = self._player1

        if position not in move_check:
            return corner_capture

        else:
            index = 0
            for num in range(0, 4):  # This iterates 4 times (4 corner checks).
                if position == move_check[index] or position == move_check[index + 1]:
                    if self.get_square_occupant(move_check[index]) == self.get_square_occupant(move_check[index + 1]):
                        if self.get_square_occupant(corners[num]) == opponent.get_color():
                            self._board[corners[num][0]][corner_index[num]] = ' . '
                            opponent.set_soldiers(1)
                            corner_capture = True
                            return corner_capture

                        else:
                            index += 2

                else:
                    index += 2

        return corner_capture

    def get_square_occupant(self, source_coord):
        """This function returns the occupant of a square"""
        source_row = (source_coord[0]).lower()
        source_column = int(source_coord[1])

        if self._board[source_row][source_column - 1] == ' B ':
            return 'BLACK'

        elif self._board[source_row][source_column - 1] == ' R ':
            return 'RED'

        else:
            return None

    def make_move(self, source_coord, destination_coord):
        """This function goes through several validation functions in order to make a move and to determine--and set--
        the state of the game. This is the primary function of this project everything above are helper functions for
        this particular method."""
        # This breaks down the string input of the function and translates it into key and value pairs for the board
        source_row = (source_coord[0]).lower()
        source_column = int(source_coord[1])
        destination_row = destination_coord[0].lower()
        destination_column = int(destination_coord[1])

        # Checks if the game is still going
        if self._game_state != 'UNFINISHED':
            return False

        # validate move is horizontal or vertical (player cannot move diagonally):
        if source_row != destination_row and source_column != destination_column:
            return False

        # validate square chosen is player color and not opponent color or empty space:
        if self.get_square_occupant(source_coord) != self.get_active_player():
            return False

        # Validates that the player actually moved and not entered duplicate coordinates
        if source_row == destination_row and source_column == destination_column:
            return False

        # Validates vertical move:
        if source_column == destination_column:
            if self.vertical_move(source_row, destination_row, source_column):
                return False

        # Validates horizontal move
        if source_row == destination_row:
            if self.horizontal_move(source_row, source_column, destination_column):
                return False

        """If all checks return True, then a move is made, captures are determined, game state is updated, and
        active player is updated to the next player"""

        # Replaces current player position with blank representation
        self._board[source_row][source_column - 1] = ' . '

        # Sets destination position with current player token
        self._board[destination_row][destination_column - 1] = self._active_player.get_marker()

        # Horizontal capture check
        self.horizontal_capture(source_row, destination_row, source_column, destination_column)

        # Vertical capture check
        self.vertical_capture(source_row, destination_row, destination_column)

        # Corner capture check
        self.corner_capture(destination_row, destination_column)

        # Update game state if necessary by checking opponents soldiers
        if self._active_player.get_color() == "BLACK" and self._player2.get_soldiers() >= 8:
            self._game_state = 'BLACK_WON'

        elif self._active_player.get_color() == "RED" and self._player1.get_soldiers() >= 8:
            self._game_state = 'RED_WON'

        else:
            self._game_state = 'UNFINISHED'

        # Update active player
        if self._active_player.get_color() == 'BLACK':
            self._active_player = self._player2

        else:
            self._active_player = self._player1

        return True


def main():
    game = HasamiShogiGame()
    game_on = True
    while game_on:
        if game.get_game_state() != 'UNFINISHED':
            print(game.get_game_state())
            game.print_board()
            game_on = False
        else:
            game.print_board()
            print('{}, it is your turn: '.format(game.get_active_player()))
            user_source = input('Choose the piece to move: ')
            user_destination = input('Choose your destination: ')
            print(game.make_move(user_source, user_destination))


main()
