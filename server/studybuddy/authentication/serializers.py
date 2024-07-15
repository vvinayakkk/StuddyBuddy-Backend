from rest_framework import serializers
from .models import User
from connections.models import FriendRequest

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        
class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer()
    receiver = UserBasicSerializer()

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']
class UserSerializer(serializers.ModelSerializer):
    friends = serializers.SerializerMethodField()
    sent_friend_requests = FriendRequestSerializer(many=True, read_only=True)
    received_friend_requests = FriendRequestSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'department', 'year', 
            'availability', 'courses', 'preferred_study_methods', 
            'goals', 'password', 'friends', 'sent_friend_requests', 
            'received_friend_requests'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_friends(self, obj):
        friends = obj.friends.all()
        return UserBasicSerializer(friends, many=True).data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.department = validated_data.get('department', instance.department)
        instance.year = validated_data.get('year', instance.year)
        instance.availability = validated_data.get('availability', instance.availability)
        instance.courses = validated_data.get('courses', instance.courses)
        instance.preferred_study_methods = validated_data.get('preferred_study_methods', instance.preferred_study_methods)
        instance.goals = validated_data.get('goals', instance.goals)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance
