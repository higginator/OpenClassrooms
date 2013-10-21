from django import forms

class SearchForm(forms.Form):
	building = forms.CharField(max_length=40)
	number = forms.CharField(max_length=40)
	time = forms.CharField(max_length=40)
	day = forms.CharField(max_length=40)