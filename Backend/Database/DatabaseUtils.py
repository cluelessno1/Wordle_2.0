import os
import logging

from pymongo import MongoClient
from dotenv import dotenv_values
from bson.objectid import ObjectId

class DatabaseUtils:
    def __init__(self):
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the relative path to the .env file
        env_path = os.path.join(current_dir, '..', '.env')

        # Load the data from the .env file
        config = dotenv_values(env_path)

        self.DB_NAME = config['WORDLE_2_PROJECT_DB_NAME']
        self.ALL_ENGLISH_WORDS_TABLE_NAME = config['ALL_ENGLISH_WORDS_TABLE_NAME']
        self.WORD_OF_THE_DAY_TABLE_NAME = config['WORD_OF_THE_DAY_TABLE_NAME']
        self.MONGODB_CONNECTION_STRING = config['MONGODB_CONNECTION_STRING']
        # Log the initialization of the database utils
        logging.info('Initialized DatabaseUtils')

    def connect_to_MongoDB(self):
        # Log the attempt to connect to MongoDB
        logging.info('Connecting to MongoDB')

        # Create a connection to MongoDB
        client = MongoClient(self.MONGODB_CONNECTION_STRING)

        # Log successful connection to MongoDB
        logging.info('Connected to MongoDB')
        return client

    def is_word_present_in_AllEnglishWordsTable(self, word):
        # Log the query attempt
        logging.info(f'Querying for word: {word}')

        # Get client
        client = self.connect_to_MongoDB()

        # Access the database
        db = client[self.DB_NAME]

        # Access the collection
        collection = db[self.ALL_ENGLISH_WORDS_TABLE_NAME]

        # Check if the lowercase word is in the collection
        word_entry = collection.find_one({'word': word.lower()})

        # Log the result of the query
        if word_entry:
            logging.info(f'Word found: {word}')
        else:
            logging.info(f'Word not found: {word}')

        # Return True if the word is present, False otherwise
        return word_entry is not None
    
    def get_word_from_id_from_AllEnglishWordsTable(self, id):
        # Get client
        client = self.connect_to_MongoDB()

        # Access the database
        db = client[self.DB_NAME]

        # Access the collection
        collection = db[self.ALL_ENGLISH_WORDS_TABLE_NAME]

        # Convert string id to ObjectId       
        object_id = ObjectId(id)

        # Find the document by its '_id'
        word_entry = collection.find_one({'_id': object_id})

        # Return the word entry if present, None otherwise
        return word_entry['word'] if word_entry else None
    
    def get_word_of_the_day(self, date):
        # Get client
        client = self.connect_to_MongoDB()

        # Access the database
        db = client[self.DB_NAME]

        # Access the collection
        collection = db[self.WORD_OF_THE_DAY_TABLE_NAME]

        # Find the document by its 'date'
        word_of_the_day_document = collection.find_one({'date': date})

        # Check if a document was found
        if word_of_the_day_document:
            # Extract ObjectId as a string
            word_id = str(word_of_the_day_document['wordId']['$oid'])
            return self.get_word_from_id_from_AllEnglishWordsTable(word_id)
        else:
            return None