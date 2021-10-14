"""Game tic-tac-toe

This module allows two players to play tic tac toe. The results of the game
 are recorded in the "list_victories.log" file.

This module imports the 'logging' and 'sys' package from the standard library.

This file can also be imported as a module and contains the following
functions:

    * main - the main function of the script

This file can also be imported as a module and contains the following
classes:

    * FileHandler
        Creates a file handler.

        Methods
        -------
        write_game_res(message : str)
            write 'message' to the file
        show_victories
            display the contents of the file
        clean_victories
            clear the contents of the file

    * PlayingField
        Creates and processes the playing field.

        Methods
        -------
        current_field
            Returns a string with the current state of the playing field
        get_field
            return field with free space (free space is ".")

    * Player
        Creates a player with a name and game marker (must be 'X' or 'O').
        Methods
        -------
        get_name
            return player name
        set_name(name) : staticmethod
            asks the player to enter their name for the game
    * Game
        The class is used to play tic-tac-toe.

        Methods
        -------
        get_players
            return a message with the names of the players and what markers they have.
        start(count_x=0, count_y=0, count_draw=0)
            start game
"""
import logging
import sys


def main():
    """Creates a file to record the results of winnings and start app.
    """
    file_victories = FileHandler("list_victories.log")
    menu(file_victories)


def menu(file_victories):
    """Allows through the interactive mode to start operations:
    Start the game, display the results of victories and
    delete records of victories, exit.
    Parameters
    ----------
    file_victories
        logger handler"""
    choice = input("Please make a choice:\n"
                   "1 - play\n"
                   "2 - list of victories\n"
                   "3 - clean the list of victories\n"
                   "4 - exit\n"
                   "your choice is ")
    if choice == "1":
        player_x = Player("X")
        player_o = Player("O")
        game = Game(file_victories, player_x, player_o)
        game.start()
    elif choice == "2":
        file_victories.show_victories()
        menu(file_victories)
    elif choice == "3":
        file_victories.clean_victories()
        menu(file_victories)
    elif choice == "4":
        sys.exit()
    else:
        print("Please make a choice")
        menu(file_victories)


class FileHandler:
    """
    Creates a file handler.
    Which can create a "win list" file on initialization.
    Allows you to write new victories to a file using
    logging (level = warning), display all victories
    and clear the list of all victories.

    Attributes
    ----------
    file : str
        filename to create and process to process
    logger : logging.getLogger()
        an instance of the Logger class
    game_handler : logging.FileHandler()
        an instance of the FileHandler class

    Methods
    -------
    write_game_res
        Passes a message to the handler to write the winners to the file.
    show_victories
        Outputs all recorded game results to the console.
    clean_victories(self)
        clear all records
    """
    def __init__(self, file_victories="list_victories.log"):
        """
        Parameters
        ----------
        file_victories : str
            The name of file to which the results of the game
            will be received (and all messages of the
            warning level and higher);) (default='list_victories.log')
        """
        self.file = file_victories
        self.logger = logging.getLogger(__name__)
        self.game_handler = self._create_handler(self.file)

    def _create_handler(self, file_name: str):
        """Creates a file handler (warning level) with the help of
        which writes to the file_name file are made.
        Parameters
        ----------
        file_name : str
            the file to which the results of the game
            will be received (and all messages of the warning level
            and higher);).
        """
        self.game_handler = logging.FileHandler(file_name)
        self.game_handler.setLevel(logging.WARNING)
        format_handler = logging.Formatter(
            fmt='%(asctime)s - %(message)s', datefmt="%d-%m-%y %H:%M")
        self.game_handler.setFormatter(format_handler)
        self.logger.addHandler(self.game_handler)
        return self.game_handler

    def write_game_res(self, message: str):
        """
        Passes a message to the handler to write the winners to the file.

        Parameters
        ----------
        message : str
            Message to write to the generated file
        """
        self.logger.warning("%s", message)   # (%message%s.format(message)) (f'{message}')

    def show_victories(self):
        """Outputs all recorded game results to the console."""
        with open(self.file, "r") as file_name:
            text = file_name.read()
            print(text)

    def clean_victories(self):
        """Clear all records."""
        with open(self.file, "w"):
            pass


class Player:
    """
    Creates a player with a name and game marker (must be 'X' or 'O').

    Attributes
    ----------
    marker : str
        the player's marker in the game must be 'X' or 'O'
    name : str
        player name

    Methods
    -------
    get_name
        return player name
    set_name(name) : staticmethod
        asks the player to enter their name for the game
    """
    def __init__(self, marker: str):
        """
        Parameters
        ----------
        marker : str
            player marker, must be 'X' or 'O'
        """
        self.marker = marker
        self.name = Player.set_name(marker)

    @staticmethod
    def set_name(marker):
        """Asks the player to enter their name for the game."""
        type_marker = "crosses"
        if marker == "X":
            type_marker = "crosses"
        if marker == "O":
            type_marker = "zeroes"
        name = input(
            f"The player who will play with {type_marker} please enter your name ")
        return name

    def get_name(self):
        """Return player name."""
        return self.name


class PlayingField:
    """
    Creates and processes the playing field.
    Methods
    -------
    current_field
        Returns a string with the current state of the playing field
    get_field
        return field with free space (free space is ".")
    """
    _start_field = {
        "1": "1", "2": "2", "3": "3", "4": "4", "5": "5",
        "6": "6", "7": "7", "8": "8", "9": "9"}

    def __init__(self):
        self._field = {
            "1": ".", "2": ".", "3": ".", "4": ".", "5": ".",
            "6": ".", "7": ".", "8": ".", "9": "."}

    def _check_space(self, i):
        """Checks whether the player has already made a move
        to the given number, if yes, then returns the marker
        of the player who made the move.
        """
        if self._field[i] == ".":
            return self._start_field[i]
        return self._field[i]

    def current_field(self):
        """Returns a string with the current state of the playing field.
        Used to display the current game result."""
        field_now = [self._check_space(i) for i in self._start_field]
        return f"{field_now[0]} {field_now[1]} {field_now[2]}\n"\
               f"{field_now[3]} {field_now[4]} {field_now[5]}\n"\
               f"{field_now[6]} {field_now[7]} {field_now[8]}"

    def get_field(self):
        """Returns the state of the field with unoccupied positions."""
        return self._field

    def _change_field(self, name, number_space: str, marker: str):
        if self._field[number_space] == ".":
            self._field[number_space] = marker
            return True
        print(f"This place is already taken, {name} please try again")
        print(self.current_field())
        return False

    @staticmethod
    def _check_input_number(name: str):
        number_space = input(f"{name}, please enter a number to make your move ")
        if number_space not in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            print("To make a move, you need to choose a number from 1 to 9."
                  " Please make your choice")
            return PlayingField._check_input_number(name)
        return number_space

    def player_turn(self, player_name, marker):
        """Place a player marker on the field replacing
         the starting number on the field."""
        number_space = PlayingField._check_input_number(player_name)
        if self._change_field(player_name, number_space, marker):
            return number_space
        return self.player_turn(player_name, marker)

    def clear_field(self):
        """Resets the field state to the start state."""
        for i in self._field:
            self._field[i] = "."


class Game:
    """
    The class is used to play tic-tac-toe.

    Attributes
    ----------
    player_x : Player()
        cross player
    player_o : Player()
        noughts player
    playing_field : PlayingField()
        playing field
    write_victory : FileHandler()
        file handler

    Methods
    -------
    get_players
        return a message with the names of the players and what markers they have.
    start(count_x=0, count_y=0, count_draw=0)
        start game
    """
    def __init__(self, handler_victories: FileHandler, player_x: Player, player_o: Player):
        """
        Parameters
        ----------
        handler_victories : FileHandler
            file handler
        player_x : Player
            cross player
        player_o : Player
            noughts player
        """
        self.player_x = player_x
        self.player_o = player_o
        self.playing_field = PlayingField()
        self.write_victory = handler_victories

    def get_players(self):
        """Return a message with the names of the players and what markers they have."""
        return f"{self.player_x.name} plays with X" \
               f" and {self.player_o.name} plays with {self.player_o.marker}"

    def _check_win_lines(self, player_marker):
        """Check if there is a winner in the lines."""
        field = self.playing_field.get_field()
        m_p = player_marker
        return (field["1"] == m_p and field["2"] == m_p and field["3"] == m_p or
                field["4"] == m_p and field["5"] == m_p and field["6"] == m_p or
                field["7"] == m_p and field["8"] == m_p and field["9"] == m_p)

    def _check_win_columns(self, player_marker):
        """Check if there is a winner in the columns."""
        field = self.playing_field.get_field()
        m_p = player_marker
        return (field["1"] == m_p and field["4"] == m_p and field["7"] == m_p or
                field["2"] == m_p and field["5"] == m_p and field["8"] == m_p or
                field["3"] == m_p and field["6"] == m_p and field["9"] == m_p)

    def _check_win_diagonals(self, player_marker):
        """Check if there is a winner in the diagonals."""
        field = self.playing_field.get_field()
        m_p = player_marker
        return (field["1"] == m_p and field["5"] == m_p and field["9"] == m_p or
                field["3"] == m_p and field["5"] == m_p and field["7"] == m_p)

    def _check_winner(self, player_marker: str):
        return (self._check_win_lines(player_marker) or
                self._check_win_columns(player_marker) or
                self._check_win_diagonals(player_marker))

    def _write_draw(self, count_x, count_y, count_draw):
        print(self.playing_field.current_field())
        print("Draw")
        if (count_x + count_y + count_draw) > 1:
            self.write_victory.write_game_res(
                f"{self.player_x.name} : {self.player_o.name}"
                f" - {count_x} : {count_y}, Draw {count_draw}")
        else:
            self.write_victory.write_game_res(
                f"{self.player_x.name} ({self.player_x.marker})"
                f" and {self.player_o.name}"
                f" ({self.player_o.marker}) played a draw")

    def _write_winner_few_game(self, count_x, count_y, count_draw):
        print()
        if (count_x + count_y + count_draw) > 1:
            self.write_victory.write_game_res(
                f"{self.player_x.name} : {self.player_o.name}"
                f" - {count_x} : {count_y}, Draw {count_draw}")

    def _write_winner_one_game(self, count_x, count_y, count_draw):
        if count_x == 1:
            self.write_victory.write_game_res(
                f"{self.player_x.name} won by playing with {self.player_x.marker}")
        if count_y == 1:
            self.write_victory.write_game_res(
                f"{self.player_o.name} won by playing with {self.player_o.marker}")
        if count_draw == 1:
            self._write_draw(count_x, count_y, count_draw)

    def start(self, count_x=0, count_o=0, count_draw=0):
        """Start game.
        Parameters
        __________
        count_x : int
            crosses win counter (default=0)
        count_o : int
            noughts win counter (default=0)
        count_draft : int
            draws counter (default=0)
        """
        i = 0
        while True:
            print(self.playing_field.current_field())
            print(f"Now it's {self.player_x.name}'s turn")
            self.playing_field.player_turn(self.player_x.name, self.player_x.marker)
            i += 1
            if self._check_winner(self.player_x.marker):
                print(self.playing_field.current_field())
                print(f"Player {self.player_x.name} won")
                count_x += 1
                break
            if i == 9:
                print(self.playing_field.current_field())
                print("Draw")
                count_draw += 1
                break
            print(self.playing_field.current_field())
            print(f"Now it's {self.player_o.name}'s turn")
            self.playing_field.player_turn(self.player_o.name, self.player_o.marker)
            i += 1
            if self._check_winner(self.player_o.marker):
                print(self.playing_field.current_field())
                print(f"Player {self.player_o.name} won")
                count_o += 1
                break

        self._repeat_game(count_x, count_o, count_draw)

    def _repeat_game(self, count_x, count_o, count_draw):
        repeat_game = input("Do you want to repeat the game, choice y/n ")
        if repeat_game not in ("y", "n", "Y", "N"):
            print("Please enter y - if you want continue or "
                  "n - if you want return to main menu  ")
            return self._repeat_game(count_x, count_o, count_draw)
        if repeat_game == "y":
            self._write_winner_few_game(count_x, count_o, count_draw)
            print()
            self.playing_field.clear_field()
            return self.start(count_x, count_o, count_draw)
        if repeat_game == "n":
            if (count_x + count_o + count_draw) == 1:
                self._write_winner_one_game(count_x, count_o, count_draw)
                self.playing_field.clear_field()
                print("Game over")
                return menu(self.write_victory)
            self._write_winner_few_game(count_x, count_o, count_draw)
            print("Game over")
            self.playing_field.clear_field()
            return menu(self.write_victory)
        return False


if __name__ == "__main__":
    main()
