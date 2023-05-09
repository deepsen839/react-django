from rest_framework import serializers
from .models import EventsModel,EventsLiked
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EventsLikedSerializer(serializers.ModelSerializer):
     class Meta:
          model = EventsLiked
          fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    user_details = EventsLikedSerializer(many=True,read_only=True)
    class Meta:
          model = EventsModel
          fields = '__all__'
    # def create(self, validated_data):
    #     # event_liked = validated_data.pop('event_liked')
    #     event_instance = EventsModel.objects.create(**validated_data)
    #     for el in event_liked:
    #         EventsLiked.objects.create(user=event_instance,**event_liked)
    #     return event_instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user          



          