import logging
from datetime import datetime

from Backend.Database.DatabaseUtils import DatabaseUtils

class WordleGame:
    def __init__(self, mode='medium', max_tries=10, date='2024-06-14'):
        self.guesses = []
        self.mode = mode
        self.grayed_out_letters = set()
        self.dbUtils = DatabaseUtils()
        self.currentTries = 0
        self.max_tries = max_tries
        self.target_word = self.dbUtils.get_word_of_the_day(date)
        self.targetWordLen = len(self.target_word)

        logging.info(f'Game started in {self.mode} mode with target word: {self.target_word}')

    def guess_word(self, guess):
        self.currentTries += 1

        if self.currentTries > self.max_tries:
            return False, "You've reached the maximum number of tries."

        guessLengthValidationResult, guessLengthValidationMessage = self.guessLengthValidation(guess)
        if not guessLengthValidationResult:
            return False, guessLengthValidationMessage
        
        if not self.isAValidEnglishWord(guess):
            return False, "{0} is not a valid English word.".format(guess)
        
        if self.mode == 'hard' and any(letter in self.grayed_out_letters for letter in guess):
            return False, "You can't reuse the letters that have been grayed out in HARD mode."

        self.guesses.append(guess)

        if guess == self.target_word:
            return True, "Congratulations! You've guessed the word."

        result = []
        for g, t in zip(guess, self.target_word):
            if g == t:
                result.append(('green', g))
                for i, (colour, letter) in enumerate(result):
                    if letter == g and colour == 'yellow':
                        result[i] = (g, 'grey')
                        break
            elif g in self.target_word and all(g != r[1] for r in result):
                result.append(('yellow', g))
            else:
                result.append(('gray', g))
                if self.mode == 'hard':
                    self.grayed_out_letters.add(g)

        return False, result

    def get_guesses(self):
        return self.guesses
    
    def guessLengthValidation(self, guess):
        if self.mode == 'easy':
            return (True, '') if len(guess) <= len(self.target_word) else (False, "The length of the guess word can't be greater than {0}".format(len(self.target_word)))
        elif self.mode == 'medium' or self.mode == 'hard':
            return (True, '') if len(guess) == len(self.target_word) else (False, "The length of the guess word has to be equal to {0}".format(len(self.target_word)))

    def isAValidEnglishWord(self, guess):
        return self.dbUtils.is_word_present_in_AllEnglishWordsTable(guess)
    
    def triesLeft(self):
        return self.max_tries - self.currentTries
    
    def lengthOfTargetWord(self):
        return self.targetWordLen
         
def validate_mode(mode):
    if mode not in ['easy', 'medium', 'hard']:
        raise ValueError(f"Invalid game mode {mode} selected.")
    else:
        logging.info(f"{mode} game mode selected.")

def main():
    try:
        # Ask the user for the game mode
        mode = input("Enter game mode (easy, medium, hard): ")
        validate_mode(mode)
    except ValueError as e:
        logging.exception(str(e))
        raise e

    # Get the current date
    current_date = datetime.now()

    # Format the date as 'YYYY-MM-DD'
    formatted_date = current_date.strftime('%Y-%m-%d')

    print(formatted_date)

    # Create a new game
    game = WordleGame(mode=mode, date =formatted_date)

    print("Length of the Target Word is {0}".format(game.lengthOfTargetWord()))

    # Game loop
    while True:
        print("Tries left : {0}".format(game.triesLeft()))

        # Get a guess from the user
        guess = input("Enter your guess: ")

        # Make a guess in the game
        result = game.guess_word(guess)

        # Print the result
        print(result[1])
        # Log the guess and result
        logging.info(f'Guess: {guess}, Result: {result[1]}')

        # Check if the game is over
        if result[1] == "You've reached the maximum number of tries.":
            logging.info('Game over - maximum number of tries reached.')
            break

        # Check if the game is over
        if result[1] == "Congratulations! You've guessed the word.":
            logging.info('Game won - correct word guessed.')
            break

if __name__ == "__main__":
    main()