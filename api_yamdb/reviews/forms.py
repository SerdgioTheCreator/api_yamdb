from django import forms
from reviews.models import Title, Genre


class TitleListForm(forms.ModelForm):
    # here we only need to define the field we want to be editable
    genre = forms.ModelMultipleChoiceField(queryset=Genre.objects.all())
