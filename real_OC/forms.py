from django import forms

CHOICES = (('A', 'AM'), ('P', 'PM'))

class SearchForm(forms.Form):
	building = forms.CharField(max_length=40)
	number = forms.CharField(max_length=40)
	time = forms.CharField(max_length=40)
	day = forms.CharField(max_length=40)
	ap = forms.ChoiceField(widget=forms.Select, choices = CHOICES)