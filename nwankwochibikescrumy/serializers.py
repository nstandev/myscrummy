from rest_framework import serializers
from .models import ScrumyGoals, ScrumyHistory, GoalStatus, ScrumUser, Project, ProjectRoles
from django.contrib.auth.models import User, Group


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
        print("FilteredListGoal", data.all())
        data = data.filter(project_id=self.context['project_id'])
        return super(FilteredListGoal, self).to_representation(data)


class FilteredGoalSerializerForProject(serializers.ModelSerializer):
    class Meta:
        list_serializer_class = FilteredListGoal
        model = ScrumyGoals
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class ProjectRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRoles
        fields = '__all__'


class FilteredProjectRolesList(serializers.ListSerializer):
    def to_representation(self, data):
        print("FilteredProjectRolesList: ", data)
        data = data.filter(project_id=self.context['project_id'])
        return super(FilteredProjectRolesList, self).to_representation(data)


class FilteredProjectRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRoles
        list_serializer_class = FilteredProjectRolesList


class FilteredProjectList(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(project_id=self.context['project_id']).first()
        print("YESPSPS: ", data)
        return super(FilteredProjectList, self).to_representation(data)


class FilteredProjectForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        list_serializer_class = FilteredProjectList


class UserSerializer(serializers.ModelSerializer):
    goals = ScrumyGoalsSerializer(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'groups', 'goals']


class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class FilteredUserSerializerForProject(serializers.ModelSerializer):
    goals = FilteredGoalSerializerForProject(many=True, read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    # project_set = FilteredProjectForUserSerializer
    project_set = ProjectSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'groups', 'goals', 'project_set']



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




