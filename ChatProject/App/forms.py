from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)


class PictureForm(forms.Form):
    picture = forms.ImageField()
