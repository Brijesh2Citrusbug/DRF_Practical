from rest_framework import serializers
from api.models import *


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['password'])
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('email', 'password',)


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = EVENT
        fields = ('id', 'name', 'address', 'organiser_name', 'organiser_email', )


class EventDateSerializer(serializers.ModelSerializer):

    class Meta:
        model = EVENT_DATE
        fields = ('date', )


class AccessPointSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ACCESS_POINT
        fields = ('id', 'name',)


class EventSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = EVENT_SLOT
        fields = '__all__'


class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TIME
        fields = '__all__'


