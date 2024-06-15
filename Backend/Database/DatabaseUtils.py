import os
import logging

from pymongo import MongoClient
from dotenv import dotenv_values
from bson.objectid import ObjectId

class DatabaseUtils:
    def __init__(self):
        try:
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
            
            # Log successful loading of configuration
            logging.info('Successfully loaded configuration from .env file')
        except Exception as e:
            logging.error(f"Failed to load configuration from .env file: {e}")
            raise e  # Re-raise exception after logging

        self.client = self.connect_to_MongoDB()

        # Log the initialization of the database utils
        logging.info('Initialized DatabaseUtils')

    def connect_to_MongoDB(self):
        try:
            # Log the attempt to connect to MongoDB
            logging.info('Connecting to MongoDB')

            # Create a connection to MongoDB
            client = MongoClient(self.MONGODB_CONNECTION_STRING)

            # Log successful connection to MongoDB
            logging.info('Connected to MongoDB')
            return client
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            return None

    def is_word_present_in_AllEnglishWordsTable(self, word):
        try:
            # Log the query attempt
            logging.info(f'Accessing {self.ALL_ENGLISH_WORDS_TABLE_NAME} to query for word: {word}')

            # Access the database
            db = self.client[self.DB_NAME]

            # Access the collection
            collection = db[self.ALL_ENGLISH_WORDS_TABLE_NAME]

            # Check if the lowercase word is in the collection
            word_entry = collection.find_one({'word': word.lower()})

            # Log the result of the query
            if word_entry:
                logging.info(f'Word found: {word}')
                return True
            else:
                logging.info(f'Word not found: {word}')
                return False
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False
    
    def get_word_from_id_from_AllEnglishWordsTable(self, wordId):
        try:
            # Log the attempt to access the database
            logging.info(f'Accessing {self.ALL_ENGLISH_WORDS_TABLE_NAME} with id: {wordId}')

            # Access the database
            db = self.client[self.DB_NAME]

            # Access the collection
            collection = db[self.ALL_ENGLISH_WORDS_TABLE_NAME]

            # Convert string id to ObjectId       
            object_id = ObjectId(wordId)

            # Find the document by its '_id'
            word_entry = collection.find_one({'_id': object_id})

            # Log the result of the query
            if word_entry:
                logging.info(f'Word entry found for id {wordId}: {word_entry["word"]}')
                return word_entry['word']
            else:
                logging.info(f'No word entry found for id {wordId}')
                return None
        except Exception as e:
            logging.error(f"An error occurred while getting word from id: {e}")
            return None
    
    def get_word_of_the_day(self, date):
        try:
            # Log the attempt to access the database
            logging.info(f'Accessing {self.WORD_OF_THE_DAY_TABLE_NAME} database for word of the day on {date}')

            # Access the database
            db = self.client[self.DB_NAME]

            # Access the collection
            collection = db[self.WORD_OF_THE_DAY_TABLE_NAME]

            # Find the document by its 'date'
            word_of_the_day_document = collection.find_one({'date': date})

            # Check if a document was found
            if word_of_the_day_document:
                # Extract ObjectId as a string
                word_id = str(word_of_the_day_document['wordId']['$oid'])
                # Log the found document
                logging.info(f'Document found for date {date}: {word_id}')
                return self.get_word_from_id_from_AllEnglishWordsTable(word_id)
            else:
                # Log no document found
                logging.info(f'No document found for date {date}')
                return None
        except Exception as e:
            logging.error(f"An error occurred while getting word of the day: {e}")
            return None