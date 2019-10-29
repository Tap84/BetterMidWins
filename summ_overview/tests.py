from django.test import TestCase, RequestFactory
from summ_overview.views import analyze


# Create your tests here.
class SearchFormEmpty(TestCase):
    def setup(self):
        self.factory = RequestFactory()
    def test_empty(self):
        request = self.factory.get("/analyze/?summ_name=")
        response = analyze(request)
        
        self.assertEqual(response,"Summoner doesnt exist")
    