from django.test import TestCase
from django.shortcuts import reverse


# Create your tests here.
class DashboardViewTests(TestCase):
    """
    Test whether the DashboardView is working perfectly and generating
    proper response.
    """

    def test_response(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
