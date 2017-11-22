from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = 'username', 'email'
        # widget = {
        #     'email': forms.TextInput
        # }


class ProfileEditForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'country', 'website', 'photo'