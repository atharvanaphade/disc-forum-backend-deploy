from os import read, stat
from rest_framework import serializers
from rest_framework.fields import empty
from .models import Profile, Thread, Post, Topic
from django.db import models
from django.contrib.auth.models import User

class AccountSerializer(serializers.ModelSerializer):
    class ProfileSerailizer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            # read_only_fields = ['userID']
            fields = ('__all__')

    profile = ProfileSerailizer(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'profile']

    @staticmethod
    def create(validated_data):
        user_instance = User.objects.create_user(**validated_data)
        if 'profile' in validated_data.keys():
            profile_data = validated_data.pop('profile')
            Profile.objects.create(userID=user_instance, **profile_data)
        else:
            Profile.objects.create(userID=user_instance)
        return user_instance

class ThreadSerializer(serializers.ModelSerializer):	
    class Meta:
        model = Thread
        fields = ('__all__')
        # exclude = ['upvotes', 'postedAt']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('__all__')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('__all__')
        

