from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import connection
from pymongo import MongoClient

from djongo import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    name = models.CharField(max_length=100)
    user_email = models.EmailField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear collections
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'ironman@marvel.com', 'username': 'Iron Man', 'team': 'Marvel'},
            {'email': 'captain@marvel.com', 'username': 'Captain America', 'team': 'Marvel'},
            {'email': 'spiderman@marvel.com', 'username': 'Spider-Man', 'team': 'Marvel'},
            {'email': 'batman@dc.com', 'username': 'Batman', 'team': 'DC'},
            {'email': 'superman@dc.com', 'username': 'Superman', 'team': 'DC'},
            {'email': 'wonderwoman@dc.com', 'username': 'Wonder Woman', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='test1234')

        # Create activities
        activities = [
            {'name': 'Running', 'user_email': 'ironman@marvel.com', 'team': 'Marvel'},
            {'name': 'Swimming', 'user_email': 'batman@dc.com', 'team': 'DC'},
            {'name': 'Cycling', 'user_email': 'spiderman@marvel.com', 'team': 'Marvel'},
            {'name': 'Yoga', 'user_email': 'wonderwoman@dc.com', 'team': 'DC'},
        ]
        for a in activities:
            Activity.objects.create(**a)

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=300)
        Leaderboard.objects.create(team='DC', points=250)

        # Create workouts
        workouts = [
            {'name': 'Push Ups', 'difficulty': 'Medium'},
            {'name': 'Pull Ups', 'difficulty': 'Hard'},
            {'name': 'Squats', 'difficulty': 'Easy'},
        ]
        for w in workouts:
            Workout.objects.create(**w)

        # Ensure unique index on email for users using PyMongo
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
