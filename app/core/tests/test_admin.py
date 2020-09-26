from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import (
    reverse,
)  # will allow us to generate URLs for our Django admin page.

from django.test import (
    Client,
)

# will allow us to make test requests to our application in our unit tests


class AdminSiteTests(TestCase):
    def setUp(self):
        # TODO
        # setup is gonna consist of creating
        # our test client we're going to add a new user that we can use to test
        # we're gonna make sure that user is logged into our client
        # a regular user to list in admin
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@indianadmin.com", password="test123"
        )
        # client's helper funciton force_login() that allows you to
        # login a user with the django authentication
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@indianadmin.com", password="test123", name="Test name"
        )

    # make changes to admin.py file so that it supports our custom user model

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse(
            "admin:core_user_changelist"
        )  # generate the URL for our list user page
        res = self.client.get(url)
        # this will perform our test client to perform a
        # HTTP GET on the URL that we have found here
        # run assertions
        self.assertContains(res, self.user.name)
        self.assertContains(
            res, self.user.email
        )  # check that HTTP response was HTTP 200

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        # /admin/core/user/id
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
