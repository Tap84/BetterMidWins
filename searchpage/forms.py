from django import forms

class SearchForm(forms.Form):
    summ_name = forms.CharField(label = "Summoner Name", max_length=20, required=True)