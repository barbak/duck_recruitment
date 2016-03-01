from django.test import TestCase

# Create your tests here.

class Truc(TestCase):

    def test_truc(self):
        a = 2-3
        self.assertEqual(a, -1)