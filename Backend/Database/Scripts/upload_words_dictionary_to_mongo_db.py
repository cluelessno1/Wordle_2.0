import json
import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import dotenv_values

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the .env file
env_path = os.path.join(current_dir, '..', '..', '.env')

# Load the data from the .env file
config = dotenv_values(env_path)

# Construct the relative path to the words_dictionary.json file
json_file_path = os.path.join(current_dir, '..', 'words_dictionary.json')

JSON_FILE_PATH = json_file_path
DB_NAME = config['WORDLE_2_PROJECT_DB_NAME']
TABLE_NAME = config['ALL_ENGLISH_WORDS_TABLE_NAME']
MONGODB_CONNECTION_STRING = config['MONGODB_CONNECTION_STRING']

# Load data from the JSON file
with open(JSON_FILE_PATH, 'r') as file:
    data = json.load(file)

# Connect to MongoDB
client = MongoClient(MONGODB_CONNECTION_STRING)

# Create a new database
db = client[DB_NAME]

# Create a new collection (table)
collection = db[TABLE_NAME]

# Upload each key to the collection with an auto-incremented id
for word in data.keys():
    # The ObjectId() will generate a unique identifier for each entry
    word_entry = {'_id': ObjectId(), 'word': word}
    collection.insert_one(word_entry)

print("All keys have been uploaded to MongoDB.")
