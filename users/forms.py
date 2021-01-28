from django.contrib.auth.forms import UserCreationForm

from admin_portal.models import User


class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'date_of_birth', 'cell_number',
                  'next_of_kin_name', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'roles']