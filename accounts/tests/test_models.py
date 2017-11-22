from django.test import TestCase
from django.contrib.auth.models import User
from django_webtest import WebTest
from accounts.models import Profile

class ProfileModelTest(TestCase):
    def test_string_representation(self):
        user = User.objects.create_user(username="samshultz", password="reductionism", email="samshultz2@hotmail.com")
        instance = Profile.objects.create(user=user)
        self.assertEqual(str(instance), "Profile for samshultz")
