from django import forms
from reviews.models import Genre


class TitleListForm(forms.ModelForm):
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
