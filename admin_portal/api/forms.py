from django import forms
from admin_portal.models import User, CovidQuestionnaire
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = '__all__'


class CovidForm(forms.ModelForm):
    class Meta:
        model = CovidQuestionnaire
        fields = '__all__'

