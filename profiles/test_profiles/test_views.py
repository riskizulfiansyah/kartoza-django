from django.test import TestCase, Client
from django.urls import reverse
from profiles.forms import UserRegistrationForm
from django.contrib.auth.models import User


class TestRegisterView(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")  # Ensure 'register' is a valid URL name

    def test_register_get_request(self):
        """Test if GET request returns the registration form."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertIsInstance(response.context["form"], UserRegistrationForm)

    def test_register_post_valid_data(self):
        """Test if a user is successfully registered and logged in."""
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "email": "testuser@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        # Check user is created
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, "testuser")

        # Check if the user is logged in
        self.assertTrue("_auth_user_id" in self.client.session)

        # Check if redirected to profile page
        self.assertRedirects(response, reverse("profile"))

    def test_register_post_invalid_data(self):
        """Test if invalid data returns form errors."""
        response = self.client.post(
            self.register_url,
            {
                "username": "testuser",
                "email": "invalid-email",
                "password1": "pass",
                "password2": "mismatch",
            },
        )

        self.assertEqual(User.objects.count(), 0)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("email", response.context["form"].errors)
        self.assertIn("password2", response.context["form"].errors)
