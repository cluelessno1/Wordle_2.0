import json
from pymongo import MongoClient
from bson.objectid import ObjectId

JSON_FILE_PATH = '../words_dictionary.json'
DB_NAME = 'Wordle2DB'
TABLE_NAME = 'AllEnglishWordsTable'
MONGODB_CONNECTION_STRING = ''

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
