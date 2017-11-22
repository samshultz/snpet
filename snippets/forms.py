from django import forms
from .models import Snippet, Language


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ('author', 'created', 'slug', 'upvotes', 'downvotes',
            'bookmarks')

        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control1",
                "placeholder": "Add a Title"}),
            'language': forms.Select(attrs={'class': 'form-control1'}),
            'category': forms.SelectMultiple(attrs={'class': 'form-control1'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control1 form-control',
                'cols': 5,
                'placeholder': "Enter a short Description of snippet"}),
            'code': forms.Textarea(attrs={
                'class': 'form-control1 form-control',
                'rows': 15, 'placeholder': "Enter Snippet"}),
            'sample_input': forms.Textarea(attrs={
                'class': 'form-control1 form-control',
                'cols': 5, 'placeholder': "Enter a sample input"}),
            'sample_output': forms.Textarea(attrs={
                'class': 'form-control1 form-control',
                'cols': 5, 'placeholder': "Enter a sample output"}),
        }
        help_texts = {
            'category': ("Hold down 'Control', or 'Command' on a Mac, to select more than one.")
        }

class LanguageForm(forms.Form):
    CHOICES = Language.objects.values_list('id', 'name')

    language = forms.MultipleChoiceField(choices=CHOICES, widget=forms.CheckboxSelectMultiple)
    