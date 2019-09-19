from rest_framework import serializers
from .models import ScrumyGoals, ScrumyHistory, GoalStatus, ScrumUser, Project
from django.contrib.auth.models import User


class ScrumyGoalsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = ScrumyGoals
        fields = ['id', 'goal_name', 'goal_id', 'created_by', 'moved_by', 'owner', 'goal_status', 'user', 'is_deleted']


# class FilteredListUserSerializer(serializers.ListSerializer):
#     def to_representation(self, data):
#         data = data.filter(project=self.)
#         return super(FilteredListUserSerializer, self).to_representation(data)

class FilteredListGoal(serializers.ListSerializer):
    def to_representation(self, data):
        # print(data)
        data = data.filter(project_id=self.context['project_id'])
        return super(FilteredListGoal, self).to_representation(data)


class FilteredGoalSerializerForProject(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListGoal
        model = ScrumyGoals
        fields = '__all__'


class FilteredUserSerializerForProject(serializers.ModelSerializer):
    goals = FilteredGoalSerializerForProject(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'groups', 'goals']


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


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']
