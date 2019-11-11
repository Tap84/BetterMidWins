from django.test import TestCase, RequestFactory
from .views import search
# Create your tests here.
class SearchCase(TestCase):
    def test(self):
        self.factory = RequestFactory()
        request = self.factory.get("/search")
        search(request)
