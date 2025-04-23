from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using Django ORM
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Database tables cleared successfully.'))

        # Drop existing collections using pymongo
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]
        collections = ['users', 'teams', 'activity', 'leaderboard', 'workouts']
        for collection in collections:
            db[collection].drop()

        self.stdout.write(self.style.SUCCESS('Database collections dropped successfully.'))

        # Insert data only if it does not already exist
        users = [
            User(_id=ObjectId(), username='thundergod', email='thundergod@mhigh.edu', password='thundergodpassword'),
            User(_id=ObjectId(), username='metalgeek', email='metalgeek@mhigh.edu', password='metalgeekpassword'),
            User(_id=ObjectId(), username='zerocool', email='zerocool@mhigh.edu', password='zerocoolpassword'),
            User(_id=ObjectId(), username='crashoverride', email='crashoverride@mhigh.edu', password='crashoverridepassword'),
            User(_id=ObjectId(), username='sleeptoken', email='sleeptoken@mhigh.edu', password='sleeptokenpassword'),
        ]
        User.objects.bulk_create(users, ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Users created successfully.'))

        # Create teams and assign users
        team1 = Team(_id=ObjectId(), name='Blue Team')
        team2 = Team(_id=ObjectId(), name='Gold Team')
        team1.save()
        team2.save()
        team1.members.add(*users)

        self.stdout.write(self.style.SUCCESS('Users assigned to Blue Team successfully.'))
        self.stdout.write(self.style.SUCCESS('Teams created successfully.'))

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], activity_type='Cycling', duration=timedelta(hours=1)),
            Activity(_id=ObjectId(), user=users[1], activity_type='Crossfit', duration=timedelta(hours=2)),
            Activity(_id=ObjectId(), user=users[2], activity_type='Running', duration=timedelta(hours=1, minutes=30)),
            Activity(_id=ObjectId(), user=users[3], activity_type='Strength', duration=timedelta(minutes=30)),
            Activity(_id=ObjectId(), user=users[4], activity_type='Swimming', duration=timedelta(hours=1, minutes=15)),
        ]
        Activity.objects.bulk_create(activities)

        self.stdout.write(self.style.SUCCESS('Activities created successfully.'))

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), user=users[0], score=100),
            Leaderboard(_id=ObjectId(), user=users[1], score=90),
            Leaderboard(_id=ObjectId(), user=users[2], score=95),
            Leaderboard(_id=ObjectId(), user=users[3], score=85),
            Leaderboard(_id=ObjectId(), user=users[4], score=80),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        self.stdout.write(self.style.SUCCESS('Leaderboard entries created successfully.'))

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Workouts created successfully.'))

        # Test direct insertion using Django ORM
        test_user = User(username='testuser', email='testuser@mhigh.edu', password='testpassword')
        test_user.save()
        retrieved_user = User.objects.filter(email='testuser@mhigh.edu').first()
        if retrieved_user:
            self.stdout.write(self.style.SUCCESS(f'Test user created and retrieved: {retrieved_user.username}'))
        else:
            self.stdout.write(self.style.ERROR('Failed to create or retrieve test user.'))

        # Test direct insertion using pymongo
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]
        db.test_collection.insert_one({"test": "pymongo insertion successful"})
        result = db.test_collection.find_one({"test": "pymongo insertion successful"})
        if result:
            self.stdout.write(self.style.SUCCESS(f'Test document inserted and retrieved using pymongo: {result}'))
        else:
            self.stdout.write(self.style.ERROR('Failed to insert or retrieve test document using pymongo.'))
        db.test_collection.drop()
