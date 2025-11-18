
import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '{repo_basename}')))


# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', f'{safe_repo_name}')))
# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import sys
sys.path.insert(0, r'/home/vvdn/projects/sfit_unitest_19_9_2025/cloned_repos/py-tic-tac-toe')

import pytest
from unittest.mock import patch, MagicMock

from tic_tac_toe import TicTacToe

@pytest.fixture
def game():
    return TicTacToe()

def test_create_board(game):
    game.create_board()
    assert game.board == [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

def test_get_random_first_player(game):
    player_choice = game.get_random_first_player()
    assert player_choice in [0, 1]

def test_fix_spot(game):
    game.create_board()
    game.fix_spot(0, 0, 'X')
    assert game.board[0][0] == 'X'

def test_has_player_won_row(game):
    game.create_board()
    game.fix_spot(0, 0, 'X')
    game.fix_spot(0, 1, 'X')
    game.fix_spot(0, 2, 'X')
    assert game.has_player_won('X') is True

def test_has_player_won_col(game):
    game.create_board()
    game.fix_spot(0, 0, 'O')
    game.fix_spot(1, 0, 'O')
    game.fix_spot(2, 0, 'O')
    assert game.has_player_won('O') is True

def test_has_player_won_diag1(game):
    game.create_board()
    game.fix_spot(0, 0, 'X')
    game.fix_spot(1, 1, 'X')
    game.fix_spot(2, 2, 'X')
    assert game.has_player_won('X') is True

def test_has_player_won_diag2(game):
    game.create_board()
    game.fix_spot(0, 2, 'O')
    game.fix_spot(1, 1, 'O')
    game.fix_spot(2, 0, 'O')
    assert game.has_player_won('O') is True

def test_has_player_won_no_win(game):
    game.create_board()
    game.fix_spot(0, 0, 'X')
    game.fix_spot(0, 1, 'O')
    game.fix_spot(0, 2, '-')
    assert game.has_player_won('X') is False
    assert game.has_player_won('O') is False

def test_is_board_filled_true(game):
    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled() is True

def test_is_board_filled_false(game):
    game.create_board()
    assert game.is_board_filled() is False

def test_swap_player_turn_x_to_o(game):
    assert game.swap_player_turn('X') == 'O'

def test_swap_player_turn_o_to_x(game):
    assert game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['1 1', '1 2', '1 3', '2 1', '2 2', '2 3', '3 1', '3 2', '3 3'])
@patch('builtins.print')
def test_start_game_draw(mock_print, mock_input):
    game = TicTacToe()
    game.start()
    assert "Match Draw!" in "".join(str(call.args[0]) for call in mock_print.call_args_list)

@patch('builtins.input', side_effect=['1 1', '2 1', '1 2', '2 2', '1 3'])
@patch('builtins.print')
def test_start_game_win_x(mock_print, mock_input):
    game = TicTacToe()
    game.start()
    assert "Player X wins the game!" in "".join(str(call.args[0]) for call in mock_print.call_args_list)

@patch('builtins.input', side_effect=['1 1', '2 1', '1 2', '2 2', '3 3', '1 3', '2 3'])
@patch('builtins.print')
def test_start_game_win_o(mock_print, mock_input):
    game = TicTacToe()
    game.start()
    assert "Player O wins the game!" in "".join(str(call.args[0]) for call in mock_print.call_args_list)

@patch('builtins.input', side_effect=['1 1', '1 1', '1 2'])
@patch('builtins.print')
def test_start_game_invalid_move(mock_print, mock_input):
    game = TicTacToe()
    game.start()
    assert "Invalid spot. Try again!" in "".join(str(call.args[0]) for call in mock_print.call_args_list)

if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))