from django import forms

class SearchForm(forms.Form):
    search = forms.CharField(label = "Summoner Name", max_length=20, required=False)