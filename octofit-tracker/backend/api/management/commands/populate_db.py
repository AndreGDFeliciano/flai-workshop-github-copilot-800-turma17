from django.core.management.base import BaseCommand
from api.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data...')
        
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Existing data cleared!'))
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Assembling Earth\'s Mightiest Heroes for fitness!',
            members=[],
            total_points=0
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='The Justice League of Fitness Champions!',
            members=[],
            total_points=0
        )
        
        self.stdout.write(self.style.SUCCESS('Teams created!'))
        
        # Create Users (Superheroes)
        self.stdout.write('Creating users...')
        
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com', 'team': 'Team Marvel'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com', 'team': 'Team Marvel'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com', 'team': 'Team DC'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com', 'team': 'Team DC'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com', 'team': 'Team DC'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com', 'team': 'Team DC'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com', 'team': 'Team DC'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com', 'team': 'Team DC'},
        ]
        
        all_heroes = marvel_heroes + dc_heroes
        users = []
        
        for hero_data in all_heroes:
            user = User.objects.create(
                name=hero_data['name'],
                email=hero_data['email'],
                password='superhero123',  # In production, this should be hashed
                team=hero_data['team'],
                total_points=random.randint(500, 2000)
            )
            users.append(user)
            
            # Update team members list
            if hero_data['team'] == 'Team Marvel':
                team_marvel.members.append(hero_data['email'])
            else:
                team_dc.members.append(hero_data['email'])
        
        team_marvel.save()
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} superhero users!'))
        
        # Create Activities
        self.stdout.write('Creating activities...')
        
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing']
        activities = []
        
        for user in users:
            # Create 5-10 random activities for each user
            num_activities = random.randint(5, 10)
            for i in range(num_activities):
                activity_type = random.choice(activity_types)
                duration = random.randint(15, 120)
                distance = random.uniform(1, 20) if activity_type in ['Running', 'Cycling', 'Swimming'] else 0
                calories = duration * random.randint(5, 10)
                points = calories // 10
                
                activity = Activity.objects.create(
                    user_email=user.email,
                    activity_type=activity_type,
                    duration=duration,
                    distance=round(distance, 2),
                    calories=calories,
                    points=points,
                    notes=f'{user.name} crushed this {activity_type} session!'
                )
                activities.append(activity)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities!'))
        
        # Update user and team points
        self.stdout.write('Updating points...')
        
        for user in users:
            user_activities = Activity.objects.filter(user_email=user.email)
            total_points = sum(activity.points for activity in user_activities)
            user.total_points = total_points
            user.save()
        
        # Update team points
        marvel_points = sum(u.total_points for u in users if u.team == 'Team Marvel')
        dc_points = sum(u.total_points for u in users if u.team == 'Team DC')
        
        team_marvel.total_points = marvel_points
        team_dc.total_points = dc_points
        team_marvel.save()
        team_dc.save()
        
        self.stdout.write(self.style.SUCCESS('Points updated!'))
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard...')
        
        sorted_users = sorted(users, key=lambda x: x.total_points, reverse=True)
        
        for rank, user in enumerate(sorted_users, start=1):
            Leaderboard.objects.create(
                user_email=user.email,
                user_name=user.name,
                team_name=user.team,
                total_points=user.total_points,
                rank=rank
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(sorted_users)} leaderboard entries!'))
        
        # Create Workouts
        self.stdout.write('Creating workouts...')
        
        workouts_data = [
            {
                'name': 'Super Soldier Training',
                'category': 'Strength',
                'difficulty': 'Advanced',
                'duration': 60,
                'description': 'Captain America\'s legendary training routine',
                'exercises': ['Push-ups', 'Pull-ups', 'Shield throws', 'Sprints'],
                'target_muscle_groups': ['Chest', 'Back', 'Arms', 'Legs']
            },
            {
                'name': 'Asgardian Warrior Workout',
                'category': 'Full Body',
                'difficulty': 'Expert',
                'duration': 90,
                'description': 'Thor\'s mighty hammer-swinging workout',
                'exercises': ['Hammer curls', 'Thunder squats', 'Lightning lunges', 'Godly planks'],
                'target_muscle_groups': ['Full Body', 'Core', 'Shoulders']
            },
            {
                'name': 'Bat Training Protocol',
                'category': 'Martial Arts',
                'difficulty': 'Advanced',
                'duration': 75,
                'description': 'Batman\'s legendary martial arts training',
                'exercises': ['Shadow boxing', 'Grappling', 'Bat kicks', 'Cave climbs'],
                'target_muscle_groups': ['Full Body', 'Core', 'Legs']
            },
            {
                'name': 'Amazonian Warrior Session',
                'category': 'Combat',
                'difficulty': 'Advanced',
                'duration': 70,
                'description': 'Wonder Woman\'s combat training routine',
                'exercises': ['Lasso swings', 'Shield blocks', 'Sword lunges', 'Warrior jumps'],
                'target_muscle_groups': ['Arms', 'Legs', 'Core', 'Back']
            },
            {
                'name': 'Speed Force Sprint',
                'category': 'Cardio',
                'difficulty': 'Intermediate',
                'duration': 45,
                'description': 'The Flash\'s speed-building workout',
                'exercises': ['Sprint intervals', 'Quick feet drills', 'Agility ladder', 'Speed bursts'],
                'target_muscle_groups': ['Legs', 'Cardiovascular']
            },
            {
                'name': 'Web-Slinger Circuit',
                'category': 'Agility',
                'difficulty': 'Intermediate',
                'duration': 50,
                'description': 'Spider-Man\'s agility and flexibility routine',
                'exercises': ['Wall climbs', 'Web swings', 'Spider push-ups', 'Acrobatic flips'],
                'target_muscle_groups': ['Full Body', 'Core', 'Arms']
            },
            {
                'name': 'Hulk Smash Strength',
                'category': 'Strength',
                'difficulty': 'Expert',
                'duration': 80,
                'description': 'Hulk\'s raw power training',
                'exercises': ['Heavy deadlifts', 'Smash ball slams', 'Gamma squats', 'Rage rows'],
                'target_muscle_groups': ['Back', 'Legs', 'Full Body']
            },
            {
                'name': 'Spy Conditioning',
                'category': 'Mixed',
                'difficulty': 'Advanced',
                'duration': 65,
                'description': 'Black Widow\'s elite spy conditioning',
                'exercises': ['Combat rolls', 'Stealth cardio', 'Flexibility training', 'Balance work'],
                'target_muscle_groups': ['Full Body', 'Core', 'Flexibility']
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts_data)} superhero workouts!'))
        
        # Summary
        self.stdout.write(self.style.SUCCESS('\n========================================'))
        self.stdout.write(self.style.SUCCESS('Database population completed!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(f'Teams: {Team.objects.count()}')
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Activities: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard Entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(f'Team Marvel Points: {team_marvel.total_points}')
        self.stdout.write(f'Team DC Points: {team_dc.total_points}')
        self.stdout.write(self.style.SUCCESS('========================================'))
