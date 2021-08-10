from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(max_length=200)


class PictureForm(forms.Form):
    picture = forms.ImageField()


class ChatGroupForm(forms.Form):
    name = forms.CharField(max_length=200)


class FindGroupForm(forms.Form):
    gr_name = forms.CharField(max_length=200, label='Group name')
