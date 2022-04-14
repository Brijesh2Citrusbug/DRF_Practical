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
        fields = ('name', 'address', 'organiser_name', 'organiser_email')

    def create(self, validated_data):
        return EVENT.objects.create(**validated_data)

    def update(self, instance, validated_data):
        new_event = EVENT(**validated_data)
        new_event.id = instance.id
        new_event.save()
        return new_event
