import random

class WordleGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.target_word = random.choice(self.word_list)
        self.guesses = []

    def guess_word(self, guess):
        if len(guess) != len(self.target_word):
            return "Guess must be {} letters long".format(len(self.target_word))

        self.guesses.append(guess)

        if guess == self.target_word:
            return "Congratulations! You've guessed the word."

        result = []
        for g, t in zip(guess, self.target_word):
            if g == t:
                result.append(('green', g))
            elif g in self.target_word:
                result.append(('yellow', g))
            else:
                result.append(('gray', g))

        return result

    def get_guesses(self):
        return self.guesses
    

def main():
    # List of words for the game
    word_list = ["apple", "banana", "cherry", "date", "elderberry"]

    # Create a new game
    game = WordleGame(word_list)

    # Game loop
    while True:
        # Get a guess from the user
        guess = input("Enter your guess: ")

        # Make a guess in the game
        result = game.guess_word(guess)

        # Print the result
        print(result)

        # Check if the game is over
        if result == "Congratulations! You've guessed the word.":
            break

if __name__ == "__main__":
    main()

