from pymongo import MongoClient

def test_connection():
    try:
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.test_collection.insert_one({"test": "connection successful"})
        result = db.test_collection.find_one({"test": "connection successful"})
        print("Test document:", result)
        db.test_collection.drop()
        print("Database connection and insertion test passed.")
    except Exception as e:
        print("Error:", e)

test_connection()
