from pymongo import MongoClient
from dotenv import dotenv_values

class DatabaseUtils:
    def __init__(self):
        # Load the data from the .env file
        config = dotenv_values("C:\\Wordle_2.0\\Backend\\.env")

        self.DB_NAME = config['WORDLE_2_PROJECT_DB_NAME']
        self.ALL_ENGLISH_WORDS_TABLE_NAME = config['ALL_ENGLISH_WORDS_TABLE_NAME']
        self.MONGODB_CONNECTION_STRING = config['MONGODB_CONNECTION_STRING']

    def is_word_present_in_AllEnglishWordsTable(self, word):
        # Create a connection to MongoDB
        client = MongoClient(self.MONGODB_CONNECTION_STRING)

        # Access the database
        db = client[self.DB_NAME]

        # Access the collection
        collection = db[self.ALL_ENGLISH_WORDS_TABLE_NAME]

        # Check if the lowercase word is in the collection
        word_entry = collection.find_one({'word': word.lower()})

        # Return True if the word is present, False otherwise
        return word_entry is not None

# Create an instance of the class
db_utils = DatabaseUtils()

# Use the method
print(db_utils.is_word_present_in_AllEnglishWordsTable("Hello"))