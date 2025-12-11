import sys
from pathlib import Path
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / 'py-tic-tac-toe'))
import pytest
from unittest.mock import patch
from Main import TicTacToe
import random

@pytest.fixture
def game():
    """Provides a fresh TicTacToe instance for each test."""
    return TicTacToe()

def test_initialization(game):
    """Test that the board is an empty list upon initialization."""
    assert game.board == []

def test_create_board(game):
    """Test that create_board initializes a 3x3 board with '-'."""
    game.create_board()
    expected_board = [['-' for _ in range(3)] for _ in range(3)]
    assert game.board == expected_board
    assert len(game.board) == 3
    assert all(len(row) == 3 for row in game.board)

@patch('random.randint')
def test_get_random_first_player_is_zero(mock_randint, game):
    """Test get_random_first_player when randint returns 0."""
    mock_randint.return_value = 0
    assert game.get_random_first_player() == 0
    mock_randint.assert_called_once_with(0, 1)

@patch('random.randint')
def test_get_random_first_player_is_one(mock_randint, game):
    """Test get_random_first_player when randint returns 1."""
    mock_randint.return_value = 1
    assert game.get_random_first_player() == 1
    mock_randint.assert_called_once_with(0, 1)

def test_fix_spot(game):
    """Test placing a player's mark on the board."""
    game.create_board()
    game.fix_spot(1, 1, 'X')
    assert game.board[1][1] == 'X'
    game.fix_spot(0, 2, 'O')
    assert game.board[0][2] == 'O'

def test_swap_player_turn(game):
    """Test swapping between players 'X' and 'O'."""
    assert game.swap_player_turn('X') == 'O'
    assert game.swap_player_turn('O') == 'X'

def test_is_board_filled(game):
    """Test the logic for checking if the board is full."""
    game.create_board()
    assert not game.is_board_filled()

    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', '-']]
    assert not game.is_board_filled()

    game.board = [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']]
    assert game.is_board_filled()

@pytest.mark.parametrize("player, board_setup, expected", [
    # Row wins
    ('X', [['X', 'X', 'X'], ['-', '-', '-'], ['-', '-', '-']], True),
    ('O', [['-', '-', '-'], ['O', 'O', 'O'], ['-', '-', '-']], True),
    # Column wins
    ('X', [['X', '-', '-'], ['X', '-', '-'], ['X', '-', '-']], True),
    ('O', [['-', 'O', '-'], ['-', 'O', '-'], ['-', 'O', '-']], True),
    # Diagonal wins
    ('X', [['X', '-', '-'], ['-', 'X', '-'], ['-', '-', 'X']], True),
    ('O', [['-', '-', 'O'], ['-', 'O', '-'], ['O', '-', '-']], True),
    # No win
    ('X', [['X', 'O', 'X'], ['O', 'X', 'O'], ['O', 'X', 'O']], False),
    ('X', [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']], False),
    # Opponent win
    ('X', [['O', 'O', 'O'], ['-', '-', '-'], ['-', '-', '-']], False),
])
def test_has_player_won(game, player, board_setup, expected):
    """Test various win and non-win scenarios."""
    game.board = board_setup
    assert game.has_player_won(player) == expected

def test_show_board(game, capsys):
    """Test that the board is printed correctly to stdout."""
    game.create_board()
    game.board[0][0] = 'X'
    game.board[1][1] = 'O'
    game.board[2][2] = 'X'
    
    game.show_board()
    
    captured = capsys.readouterr()
    expected_output = (
        "X - -\n"
        "- O -\n"
        "- - X\n\n"
    )
    assert captured.out == expected_output