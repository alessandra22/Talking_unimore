from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from blog.models import Thread


class ProfileMethodTests(TestCase):

    def setUp(self):
        thread = Thread(
            thread='PROVABC',
            periodo='Primo anno'
        )
        user = User(
            username='abc1234',
            email='abc.123@talking.unimore.it',
            password='cba321'
        )
        user.save()
        thread.save()
        profile = Profile(
            id=user.id
        )
        user.user_profile = profile

        profile.threads.set((thread,))

    def tearDown(self):
        user = User.objects.get(email='abc.123@talking.unimore.it')
        Profile.objects.get(user=user).delete()
        User.objects.get(email='abc.123@talking.unimore.it').delete()
        Thread.objects.get(thread='PROVABC').delete()

    def test_username_has_been_saved(self):
        user = User.objects.get(email='abc.123@talking.unimore.it')
        self.assertEqual(Profile.objects.get(user=user).user.username, 'abc1234')

    def test_thread_has_follower(self):
        user = User.objects.get(email='abc.123@talking.unimore.it')
        profile = Profile.objects.get(user=user)
        thread = Thread.objects.get(thread='PROVABC')
        threads = list()

        for thread in profile.threads.all():
            threads.append(thread)

        self.assertEqual(len(threads), 1)
        self.assertEqual(threads[0], thread)
