from django.contrib.auth.forms import UserCreationForm
from django import forms

from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'cell_number',
                  'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'roles']


class GeneralUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'last_login', 'group', 'roles', 'groups', 'is_superuser', 'password',
                   'user_permissions', 'date_joined')
        fields = "__all__"

        def update(self, instance, validated_data):
            instance.save()
            return instance


class LifeChoicesForm(forms.ModelForm):
    class Meta:
        model = LifeChoicesMember
        exclude = ('user',)
        fields = "__all__"


class StudentUpdateForm(LifeChoicesForm):

    class Meta:
        model = LifeChoicesAcademy
        exclude = ('user',)
        fields = "__all__"


class StaffUpdateForm(LifeChoicesForm):

    class Meta:
        model = LifeChoicesStuff
        exclude = ('user',)
        fields = "__all__"
