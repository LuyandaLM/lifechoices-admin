from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff


class RegisterUserForm(UserCreationForm):
    """
    registering all the users that would like to use our account
    """

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'cell_number',
                  'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'roles']

    def save(self, commit=True):
        """
        activate the account if the registering user is a visitor
        :param commit: standarded
        :return: the user's account activated or not activated
        """
        user = super().save(commit=False)
        if self.cleaned_data["roles"] == "visitor":
            user.is_active = True
        user.save()
        return user


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
        # exclude = ('user',)
        fields = "__all__"


class StudentUpdateForm(forms.ModelForm):

    class Meta:
        model = LifeChoicesAcademy
        # exclude = ('user',)
        fields = "__all__"


class StaffUpdateForm(forms.ModelForm):

    class Meta:
        model = LifeChoicesStuff
        # exclude = ('user',)
        fields = "__all__"
