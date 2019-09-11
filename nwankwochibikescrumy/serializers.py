from rest_framework import serializers
from .models import ScrumyGoals, ScrumyHistory, GoalStatus, ScrumUser
from django.contrib.auth.models import User


class ScrumyGoalsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ScrumyGoals
        fields = ['id', 'goal_name', 'goal_id', 'created_by', 'moved_by', 'owner', 'goal_status', 'user', 'is_deleted']


class UserSerializer(serializers.ModelSerializer):
    goals = ScrumyGoalsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'groups', 'goals']


class ScrumyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumyHistory
        fields = ['moved_by', 'created_by', 'moved_from', 'moved_to', 'time_of_action', 'goal']


class GoalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalStatus
        fields = "__all__"


class ScrumUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrumUser
        fields = "__all__"
