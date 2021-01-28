from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin_portal.models import CovidQuestionnaire, LeaveApplication, User


class CovidQuestionnaireSerializer(serializers.ModelSerializer):

    class Meta:
        model = CovidQuestionnaire
        fields = '__all__'


class LeaveApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveApplication
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'user_name', 'first_name', 'last_name', 'gender', 'roles', 'marital_status', 'date_of_birth',
                  'nationality', 'address', 'telephone_number', 'cell_number', 'permanent_address', 'next_of_kin_name',
                  'permanent_telephone_number', 'next_of_kin_relationship', 'next_of_kin_contact_number', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        active = False
        if validated_data['roles'] == "VISITOR" or 'visitor':
            active = True

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
            is_active=active,
            next_of_kin_name=validated_data['next_of_kin_name'],
            next_of_kin_relationship=validated_data['next_of_kin_relationship'],
            next_of_kin_contact_number=validated_data['next_of_kin_contact_number'],
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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
