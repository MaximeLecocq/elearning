from django.test import TestCase
from rest_framework.test import APIClient
from .models import Course


class CourseViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_course(self):
        response = self.client.post('/courses/', {'title': 'Test Course', 'description': 'This is a test course'}, format='json')
        self.assertEqual(response.status_code, 302)

    def test_retrieve_course_list(self):
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 302)


