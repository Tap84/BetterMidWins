from django.test import TestCase, RequestFactory
from .views import single_game

# Create your tests here.
class SingleCases(TestCase):
    def test_valid_game_page_exists(self):
        self.factory = RequestFactory()
        request = self.factory.get("/single/?summ_name=TyÌer&match_id=3214404628")
        single_game(request)
    