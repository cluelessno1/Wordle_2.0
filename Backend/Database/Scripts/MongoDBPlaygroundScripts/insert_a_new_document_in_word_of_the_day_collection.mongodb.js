// MongoDB Playground
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.

// The current database to use.
use('Wordle2DB');

// Create a new document in the collection.
db.getCollection('WordOfTheDayTable').insertOne({
    "wordId": {
      "$oid": ""
    },
    "date": "2024-06-16" // ISO date format
  }
);
