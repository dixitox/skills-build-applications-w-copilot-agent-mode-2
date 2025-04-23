import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "octofit_tracker.settings")

from pymongo import MongoClient
from django.conf import settings

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

def check_data_duplication():
    client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
    db = client[settings.DATABASES['default']['NAME']]

    collections = ['users', 'teams', 'activity', 'leaderboard', 'workouts']
    for collection in collections:
        pipeline = [
            {"$group": {"_id": "$name", "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}}
        ]
        duplicates = list(db[collection].aggregate(pipeline))
        if duplicates:
            print(f"Duplicates found in {collection}: {duplicates}")
        else:
            print(f"No duplicates found in {collection}.")

if __name__ == "__main__":
    test_connection()
    check_data_duplication()
