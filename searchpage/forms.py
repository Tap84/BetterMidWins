from django import forms

class SearchForm(forms.Form):
    summoner_name = forms.CharField(label = "Summoner Name", max_length=20, required=False, initial = 'test')