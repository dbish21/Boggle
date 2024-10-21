import os
import random
import string


class Boggle():

    def __init__(self):
        # Get the directory of the current file (boggle.py)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the path to words.txt
        dict_path = os.path.join(current_dir, "words.txt")
        self.words = self.read_dict(dict_path)

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""
        try:
            with open(dict_path) as dict_file:
                return [w.strip().lower() for w in dict_file]
        except FileNotFoundError:
            print(f"Error: words.txt not found at {dict_path}")
            return []

    def make_board(self):
        """Make and return a random boggle board."""

        board = []

        for y in range(5):
            row = [random.choice(string.ascii_uppercase) for i in range(5)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""

        word_exists = word in self.words
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result

    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""

        if x > 4 or y > 4:
            return False

        if board[y][x] != word[0]:
            return False

        if (y, x) in seen:
            return False

        if len(word) == 1:
            return True

        seen = seen | {(y, x)}

        # Check all adjacent cells (including diagonals)
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                new_y, new_x = y + dy, x + dx
                if 0 <= new_y < 5 and 0 <= new_x < 5:
                    if self.find_from(board, word[1:], new_y, new_x, seen):
                        return True

        return False

    def find(self, board, word):
        """Can word be found in board?"""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, 5):
            for x in range(0, 5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.

        return False
