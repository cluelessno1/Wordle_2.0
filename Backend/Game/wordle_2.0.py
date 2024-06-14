import random

class WordleGame:
    def __init__(self, word_list, mode='medium'):
        self.word_list = word_list
        self.target_word = random.choice(self.word_list)
        self.guesses = []
        self.mode = mode
        self.grayed_out_letters = set()

    def guess_word(self, guess):

        guessLengthValidationResult, guessLengthValidationMessage = self.guessLengthValidation(guess)
        if not guessLengthValidationResult:
            return False, guessLengthValidationMessage
        
        if self.mode == 'hard' and any(letter in self.grayed_out_letters for letter in guess):
            return False, "You can't reuse the letters that have been grayed out in HARD mode."

        self.guesses.append(guess)

        if guess == self.target_word:
            return True, "Congratulations! You've guessed the word."

        result = []
        for g, t in zip(guess, self.target_word):
            if g == t:
                result.append(('green', g))
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
    

def main():
    # List of words for the game
    word_list = ["apple", "banana", "cherry", "date", "elderberry"]

    # Ask the user for the game mode
    mode = input("Enter game mode (easy, medium, hard): ")

    # Create a new game
    game = WordleGame(word_list, mode)

    # Game loop
    while True:
        # Get a guess from the user
        guess = input("Enter your guess: ")

        # Make a guess in the game
        result = game.guess_word(guess)

        # Print the result
        print(result[1])

        # Check if the game is over
        if result == "Congratulations! You've guessed the word.":
            break

if __name__ == "__main__":
    main()
