from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='test@hero.com',
            password='testpass123',
            team='Test Team',
            total_points=100
        )
    
    def test_user_creation(self):
        """Test that user is created correctly"""
        self.assertEqual(self.user.name, 'Test Hero')
        self.assertEqual(self.user.email, 'test@hero.com')
        self.assertEqual(self.user.total_points, 100)
    
    def test_user_str(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'Test Hero')


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description',
            members=['test1@hero.com', 'test2@hero.com'],
            total_points=500
        )
    
    def test_team_creation(self):
        """Test that team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.total_points, 500)
    
    def test_team_str(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@hero.com',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            points=30
        )
    
    def test_activity_creation(self):
        """Test that activity is created correctly"""
        self.assertEqual(self.activity.user_email, 'test@hero.com')
        self.assertEqual(self.activity.activity_type, 'Running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.points, 30)


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            name='Test Hero',
            email='test@hero.com',
            password='testpass123',
            team='Test Team',
            total_points=100
        )
        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', args=[self.user.id])
    
    def test_get_user_list(self):
        """Test retrieving list of users"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_user_detail(self):
        """Test retrieving a single user"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Hero')
    
    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'name': 'New Hero',
            'email': 'new@hero.com',
            'password': 'newpass123',
            'team': 'New Team',
            'total_points': 0
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.team = Team.objects.create(
            name='Test Team',
            description='Test team description',
            members=['test1@hero.com'],
            total_points=500
        )
        self.list_url = reverse('team-list')
        self.detail_url = reverse('team-detail', args=[self.team.id])
    
    def test_get_team_list(self):
        """Test retrieving list of teams"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_team_detail(self):
        """Test retrieving a single team"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Team')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.activity = Activity.objects.create(
            user_email='test@hero.com',
            activity_type='Running',
            duration=30,
            distance=5.0,
            calories=300,
            points=30
        )
        self.list_url = reverse('activity-list')
        self.detail_url = reverse('activity-detail', args=[self.activity.id])
    
    def test_get_activity_list(self):
        """Test retrieving list of activities"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        data = {
            'user_email': 'test@hero.com',
            'activity_type': 'Cycling',
            'duration': 45,
            'distance': 10.0,
            'calories': 450,
            'points': 45,
            'notes': 'Great cycling session'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 2)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""
    
    def setUp(self):
        self.leaderboard = Leaderboard.objects.create(
            user_email='test@hero.com',
            user_name='Test Hero',
            team_name='Test Team',
            total_points=500,
            rank=1
        )
        self.list_url = reverse('leaderboard-list')
    
    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.workout = Workout.objects.create(
            name='Test Workout',
            category='Strength',
            difficulty='Intermediate',
            duration=45,
            description='A test workout',
            exercises=['Push-ups', 'Pull-ups'],
            target_muscle_groups=['Chest', 'Back']
        )
        self.list_url = reverse('workout-list')
        self.detail_url = reverse('workout-detail', args=[self.workout.id])
    
    def test_get_workout_list(self):
        """Test retrieving list of workouts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_workout_detail(self):
        """Test retrieving a single workout"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Workout')


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def test_api_root(self):
        """Test that API root returns all endpoint links"""
        url = reverse('api_root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

