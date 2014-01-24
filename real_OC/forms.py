from django import forms

CHOICES = (('A', 'AM'), ('P', 'PM'))

class SearchForm(forms.Form):
	building = forms.CharField(max_length=40, required=False)
	number = forms.CharField(max_length=40, required=False)
	time = forms.CharField(max_length=40, required=False)
	day = forms.CharField(max_length=40, required=False)
	ap = forms.ChoiceField(widget=forms.Select, choices = CHOICES)