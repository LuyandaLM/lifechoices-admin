from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from admin_portal.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            roles=validated_data['roles'],
            gender=validated_data['gender'],
            marital_status=validated_data['marital_status'],
            image=validated_data['image'],
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
            is_staff=validated_data['is_staff'],
            is_active=validated_data['is_active'],
            group=validated_data['group'],
            next_of_kin_name=validated_data['next_of_kin_name'],
            next_of_kin_relationship=validated_data['next_of_kin_relationship'],
            next_of_kin_contact_number=validated_data['next_of_kin_contact_number'],
            date_joined=validated_data['date_joined'],
            last_login=validated_data['last_login']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['user_name'] = user.user_name
        return token
