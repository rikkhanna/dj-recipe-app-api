from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = "test@indianadmin.com"
        password = "test123"
        user = get_user_model().objects.create_user(
            email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized """

        email = "test@INDIANADMIN.com"
        user = get_user_model().objects.create_user(email, "test123")
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        # make sure that email address is provided and
        # if not raise the ValueError
        with self.assertRaises(ValueError):
            # means anything that runs inside this and
            # should raise ValueError and if not that means test fail
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_superuser(self):
        """ test creating a new superuser """
        user = get_user_model().objects.create_superuser(
            "test@indianadmin.com", "test123"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
