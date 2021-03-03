from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import Group

from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, BankingDetail


class RegisterUserForm(UserCreationForm):
    """
    Universal registration form for all users
    """

    class Meta:
        model = User
        fields = ['email', 'roles']

    def save(self, commit=True):
        """
        activate the account if the registering user is a visitor
        :param commit: standarded
        :return: the user's account activated or not activated
        """
        user = super(RegisterUserForm, self).save(commit=False)
        if self.cleaned_data["roles"] == "visitor":
            user.is_active = True
        else:
            user.is_active = False
        user.save()
        return user


class RegisterformTwo(forms.ModelForm):
    """
    Part two form ,user registration for all non visitors
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender',
                  'date_of_birth', 'nationality', 'identity_number', 'cell_number']


class GeneralUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('is_staff', 'is_active', 'last_login', 'group', 'roles', 'groups', 'is_superuser', 'password',
                   'user_permissions', 'date_joined')
        fields = "__all__"

        def update(self, instance, validated_data):
            instance.save()
            return instance


class LifeChoicesForm(GeneralUserUpdateForm, forms.ModelForm):
    class Meta:
        model = LifeChoicesMember
        exclude = ('user',)
        fields = "__all__"


class StudentUpdateForm(LifeChoicesForm, forms.ModelForm):

    class Meta:
        model = LifeChoicesAcademy
        exclude = ('user',)
        fields = "__all__"


# SEGMENTED FORMS


class BankingDetailsForm(forms.ModelForm):
    class Meta:
        model = BankingDetail
        exclude = ('user',)
        fields = "__all__"


class BasicInfoForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ('roles', 'is_staff', 'is_active', 'group', 'date_joined', 'last_login',
                   'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'password', 'groups')
        fields = ['image', 'user_name', 'first_name', 'last_name', 'gender',
                  'date_of_birth', 'marital_status', 'nationality', 'address', 'cell_number']


class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('roles', 'is_staff', 'is_active', 'group', 'date_joined', 'last_login',
                   'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'password', 'groups')
        fields = ['cell_number', 'telephone_number',  'permanent_telephone_number',
                  'address', 'permanent_address']


class NextOfKinForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('roles', 'is_staff', 'is_active', 'group', 'date_joined', 'last_login',
                   'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'password', 'groups')
        fields = ['next_of_kin_name', 'next_of_kin_relationship',
                  'next_of_kin_contact_number']
