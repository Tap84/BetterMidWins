from django.test import TestCase, RequestFactory
from .views import analyze
import cassiopeia as cass


# Create your tests here.
class AnalyzeCases(TestCase):
    def test_empty(self):
        self.factory = RequestFactory()
        request = self.factory.get("/analyze/?summ_name=")
        response = analyze(request)
        
        self.assertEqual(response.content.decode('UTF-8'),"Summoner doesnt exist")
    
    def test_invalid(self):
        self.factory = RequestFactory()
        request = self.factory.get("/analyze/?summ_name=invalidsumnametest")
        response = analyze(request)

        self.assertEqual(response.content.decode('UTF-8'),"Summoner doesnt exist")

    def test_no_games(self):
        self.factory = RequestFactory()
        request = self.factory.get("/analyze/?summ_name=tylercwru")
        response = analyze(request)

        self.assertEqual(response.content.decode('UTF-8'),"Summoner has no ranked solo 5v5 games")
    
    def test_has_games(self):
        self.factory = RequestFactory()
        request = self.factory.get("/analyze/?summ_name=tyìer")
        analyze(request)
        
