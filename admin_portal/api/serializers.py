from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin_portal.models import CovidQuestionnaire, LeaveApplication, User
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password


class CovidQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = CovidQuestionnaire
        fields = '__all__'


class LeaveApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveApplication
        fields = ["category", "personal_message", "leave_date_from", "leave_date_to", "pre_authorisation"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs
        super().__init__(*args, **kwargs)

    def validate(self, data):
        data['user'] = self.user['data']['user']
        return data


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'roles', 'marital_status', 'date_of_birth',
                  'nationality', 'address', 'telephone_number', 'cell_number', 'permanent_address', 'next_of_kin_name',
                  'permanent_telephone_number', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def activate_account(data):
        if data.lower() == 'visitor':
            return True
        return False

    def create(self, validated_data):
        user = User.objects.create(
            roles=validated_data['roles'],
            gender=validated_data['gender'],
            marital_status=validated_data['marital_status'],
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            nationality=validated_data['nationality'],
            address=validated_data['address'],
            telephone_number=validated_data['telephone_number'],
            cell_number=validated_data['cell_number'],
            permanent_address=validated_data['permanent_address'],
            permanent_telephone_number=validated_data['permanent_telephone_number'],
            is_active=self.activate_account(validated_data['roles']),
            next_of_kin_name=validated_data['next_of_kin_name'],
            next_of_kin_relationship=validated_data['next_of_kin_relationship'],
            next_of_kin_contact_number=validated_data['next_of_kin_contact_number'],
        )


        def validate_password(self, value: str) -> str:
            """
            Hash value passed by user.

            :param value: password of a user
            :return: a hashed version of the password
            """
            return make_password(value)

        group = Group.objects.get(name=validated_data['roles'])
        user.groups.add(group)
        user.password = validate_password(value=validated_data['password'])
        user.save()
        print(user.password)
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        print(user)
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        print(token)
        # Add custom claims
        token['user_name'] = user.user_name
        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
