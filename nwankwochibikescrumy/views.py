from datetime import datetime, timedelta, timezone

import jwt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.forms import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from myscrumy import settings
from nwankwochibikescrumy.form import SignupForm, CreateGoalForm, MoveGoalForm, MoveGoalFormDeveloper, UpdateUserGroup
from nwankwochibikescrumy.serializers import UserSerializer, ScrumyGoalsSerializer, ScrumyHistorySerializer, \
    GoalStatusSerializer, ScrumUserSerializer, ProjectSerializer, FilteredUserSerializerForProject
from .models import ScrumyGoals, GoalStatus, ScrumyHistory, ScrumUser, Project, ProjectRoles
from django.contrib.auth.models import User, Group
from .miscellaneous import generate_unique_random_int as get_random_integer
from . import signals


def index(request):
    if request.user.is_authenticated:
        return redirect('nwankwochibikescrumy:home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            group_name = form.cleaned_data.get('group')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('confirm_password')

            print(group_name)
            if password == password2:
                if not User.objects.filter(email=email):
                    new_user = User(email=email,
                                    first_name=first_name,
                                    last_name=last_name,
                                    username=username
                                    )
                    new_user.set_password(password)
                    new_user.save()

                    try:
                        group = Group.objects.get(name=group_name)
                    except ObjectDoesNotExist:
                        context = {'message': "Group doesn't exist"}
                        return render(request, 'nwankwochibikescrumy/exception.html', context)
                    group.user_set.add(new_user)

                    return redirect('nwankwochibikescrumy:response')
                return HttpResponse('a user already exists with this email')

        print('********** post ********')
    else:
        form = SignupForm()
        print('********** get *********')

    return render(request, 'nwankwochibikescrumy/index.html', {'form': form})


@login_required()
def move_goal(request, goal_id):
    context = {}
    try:
        goal = ScrumyGoals.objects.get(goal_id=goal_id)
        user_group = request.user.groups.all().first()
        user_group_name = user_group.name
    except ObjectDoesNotExist:
        context.update({
            'message': 'A record with that goal id does not exist'
        })
        return render(request, 'nwankwochibikescrumy/exception.html', context)

    if request.method == 'POST':
        form = MoveGoalForm(request.POST)
        if form.is_valid():
            goal_status_name = form.cleaned_data.get("status_name")
            selected_goal_status = GoalStatus.objects.filter(status_name=goal_status_name).first()
            goal.goal_status = selected_goal_status

            moves_allowed = None

            if user_group_name == "Developer":
                moves_allowed = GoalStatus.objects.all().exclude(status_name='Verify Goal').exclude(
                    status_name='Done Goal')
            else:
                moves_allowed = GoalStatus.objects.all()

            if selected_goal_status not in moves_allowed:
                context.update({
                    'message': "You're not authorized to move this goal",
                    'redirect': "nwankwochibikescrumy:home"
                })
                return render(request, 'nwankwochibikescrumy/exception.html', context)

            goal.save()
            return redirect('nwankwochibikescrumy:home')
    else:
        try:
            group = Group.objects.get(name="Admin")
            is_admin = True if request.user.groups.all().filter(name="Admin").first() == group else False
            print(is_admin)
        except ObjectDoesNotExist:
            context.update({
                'message': 'A record with that group name does not exist'
            })
            return render(request, 'nwankwochibikescrumy/exception.html', context)
        if not is_admin:
            if goal.user != request.user:
                print(request.user.groups.all().filter(name="Admin").first())
                context.update({
                    'message': "You're not authorized to move this goal",
                    'redirect': "nwankwochibikescrumy:home"
                })
                return render(request, 'nwankwochibikescrumy/exception.html', context)
            else:
                print('here')
                form = MoveGoalForm()
        else:
            form = MoveGoalForm()

    context.update({
        'goal': goal,
        'form': form
    })
    return render(request, 'nwankwochibikescrumy/move_goal.html', context)


@login_required()
def add_goal(request):
    context = {}
    if request.method == 'POST':
        form = CreateGoalForm(request.POST)
        if form.is_valid():
            goal_name = form.cleaned_data.get('goal_name')
            username = form.cleaned_data.get('user')
            goal_status_name = form.cleaned_data.get('goal_status')
            selected_goal_status = GoalStatus.objects.get(status_name=goal_status_name)
            user = User.objects.get(username=username)

            goal_id = get_random_integer(1000, 9999)
            allowed_goal_status_dev = GoalStatus.objects.get(status_name='Weekly Goal')
            if user is not None and (allowed_goal_status_dev == selected_goal_status):
                goal = ScrumyGoals(goal_name=goal_name,
                                   goal_id=goal_id,
                                   created_by=username,
                                   owner=username,
                                   user=user,
                                   goal_status=allowed_goal_status_dev)
                goal.save()
                return redirect('nwankwochibikescrumy:home')
            else:
                context.update({
                    'message': "You're not authorized to add a goal with this status",
                    'redirect': "nwankwochibikescrumy:addgoal"
                })
                return render(request, 'nwankwochibikescrumy/exception.html', context)
    else:
        form = CreateGoalForm()
        # goal_status_weekly = GoalStatus.objects.filter(status_name="Weekly Goal").get()

    return render(request, 'nwankwochibikescrumy/add_goal.html', {'form': form, 'groups': request.user.groups.all()})


@login_required()
def home(request):
    users = User.objects.all()
    goals = ScrumyGoals.objects.all()

    # print(request.user.groups.all().filter(name="Developer").first())

    context = {
        'users': users,
        'goals': goals,
        'perm': request.user.has_perm('nwankwochibikescrumy.delete_scrumygoals'),
        'groups': request.user.groups.all()
    }

    return render(request, "nwankwochibikescrumy/home.html", context)


def success(request):
    context = {'result': 'successful', 'message': 'Your account has been created successfully!'}
    return render(request, 'nwankwochibikescrumy/response.html', context)


def update_group(request):
    if request.method == 'POST':
        form = UpdateUserGroup(request.POST)
        if form.is_valid():
            group_name = form.cleaned_data.get('groups')

            try:
                group = Group.objects.get(name=group_name)
                groups = request.user.groups.all()
            except ObjectDoesNotExist:
                context = {'message': "Group doesn't exist"}
                return render(request, 'nwankwochibikescrumy/exception.html', context)

            request.user.groups.clear()
            request.user.groups.add(group)
            print(request.user.groups)
            return redirect('nwankwochibikescrumy:home')
    else:
        form = UpdateUserGroup()

    return render(request, 'nwankwochibikescrumy/update_group.html',
                  {'form': form, 'groups': request.user.groups.all()})


# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def api_get(request, format=None):
#     if request.method == 'GET':
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)


# API views


class UserSerializerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = []
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("login")
        user = request.user
        if user is not None:
            user_serializer = UserSerializer(user)
            # token = self.generate_token(user)
            # token = self.get_tokens_for_user(user)
            user_dict = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'groups': user_serializer.data.get('groups')
            }
            token = Token.objects.get(user=user)
            user_group = request.user.groups.all().first()

            return Response({
                'user_token': token.key,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'role': str(user_group)
            }, status=200)
        return Response(status=401)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'first_name': user.first_name,
            'last_name': user.last_name,
        }

    def generate_token(self, user):
        dt = datetime.now() + timedelta(days=60)
        print(dt)
        token = jwt.encode({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'id': user.pk,
            'expiry': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        print(token)

        return token.decode('utf-8')

    # get the users linked to a particular project
    @action(methods=['get'], detail=True, url_path="projects-users", url_name="projects_users")
    def get_users_for_project(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        users = project.users.all()

        # serializer = UserSerializer(users, many=True)

        filtered_serializer = FilteredUserSerializerForProject(
            users, context={'project_id': pk}, many=True)

        print(filtered_serializer.data)

        # filtered_serializer.data.insert(0, project.created_by)

        print("get_users_for_project: ", project.users.all())
        return Response({
            "users": filtered_serializer.data,
            "project_owner": project.created_by
        })

    # get the user linked to a particular project
    @action(methods=['get'], detail=True, url_path="user-goals", url_name="user_goals")
    def get_user_for_project(self, request, pk=None):
        project = Project.objects.get(pk=pk)
        user = project.users.filter(username=request.query_params.get('user_id')).first()
        print("USER", request.query_params.get('user_id'))
        # serializer = UserSerializer(users, many=True)

        filtered_serializer = FilteredUserSerializerForProject(
            user, context={'project_id': pk}, many=False)

        print(filtered_serializer.data)

        # filtered_serializer.data.insert(0, project.created_by)

        print("get_users_for_project: ", project.users.all())
        return Response({
            "user": filtered_serializer.data,
            "project_owner": project.created_by
        })


class ScrumyGoalsSerializerViewSet(viewsets.ModelViewSet):
    queryset = ScrumyGoals.objects.all().filter(is_deleted=False)
    serializer_class = ScrumyGoalsSerializer

    def create(self, request, *args, **kwargs):

        form_data = {
            "goal_name": request.data.get('goal_name'),
            # "goal_status": request.data.get('goal_status'),
            # "user": request.data.get('user')
        }

        form = CreateGoalForm(form_data)

        # print(form_data)
        # print(request.data)
        print(form.errors)
        if form.is_valid():
            goal_name = form.cleaned_data.get('goal_name')
            # username = form.cleaned_data.get('user')
            # goal_status_name = form.cleaned_data.get('goal_status')
            # username = request.user
            selected_goal_status = GoalStatus.objects.get(status_name="Weekly Goal")
            user = request.user
            # user = User.objects.get(username=username)

            # if user.groups.all().first() == "Owner":
            #     return Response(status=401)

            goal_id = get_random_integer(1000, 9999)
            allowed_goal_status_dev = GoalStatus.objects.get(status_name='Weekly Goal')
            if user is not None and (allowed_goal_status_dev == selected_goal_status):
                goal = ScrumyGoals(goal_name=goal_name,
                                   goal_id=goal_id,
                                   created_by=user.username,
                                   owner=user.username,
                                   user=user,
                                   goal_status=allowed_goal_status_dev)

                serializer = ScrumyGoalsSerializer(goal)

                try:
                    project = Project.objects.get(name=request.data.get('project_name'))
                    goal.project = project
                    goal.save()
                except ObjectDoesNotExist:
                    return Response('errorMessage', status=401)

                return Response(serializer.data, status=200)
            else:
                return Response('errorMessage', status=401)

        return Response('failed', status=401)

    # def retrieve(self, request, *args, **kwargs):
    #     goals = ScrumyGoals.objects.all().filter(is_deleted=False)
    #     goals_serializer = ScrumyGoalsSerializer(goals, many=True)
    #     print("yes sir")
    #     print(goals_serializer.data)
    #     return Response(goals_serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            goal = ScrumyGoals.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=400)

        mode = request.META.get("HTTP_CUSTOM_MODE")

        print(mode)
        if mode == "change_owner":
            try:
                new_owner = User.objects.get(pk=request.data.get('user_id'))
                goal.user = new_owner
                goal.owner = new_owner.username
                goal.goal_status_id = request.data.get('status_id')
            except ObjectDoesNotExist:
                return Response(status=400)

        elif mode == "edit_goal_name":
            goal.goal_name = request.data.get('goal_name')

        serializer = ScrumyGoalsSerializer(goal)
        data = serializer.data

        data['moved_by'] = request.user.username

        new_serializer = ScrumyGoalsSerializer(goal, data=data, partial=False)

        if new_serializer.is_valid():
            print("here")
            new_serializer.save()
            return Response("done", status=200)

        print(new_serializer.errors)
        return Response(status=400)

    def partial_update(self, request, pk=None):
        print("partial update with patch request")
        print(pk)
        print(request.META.get('HTTP_CUSTOM_MODE'))
        goal = ScrumyGoals.objects.get(pk=pk)
        serializer = ScrumyGoalsSerializer(goal, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)

        return Response(request.data)

    def destroy(self, request, *args, **kwargs):
        goal_id = kwargs.get('pk')
        try:
            goal = ScrumyGoals.objects.get(pk=goal_id)
        except ObjectDoesNotExist:
            return Response(status=400)

        goal.is_deleted = True

        goal.save()

        serializer = ScrumyGoalsSerializer(goal)

        return Response(serializer.data, status=200)


class ScrumyHistorySerializerViewSet(viewsets.ModelViewSet):
    queryset = ScrumyHistory.objects.all()
    serializer_class = ScrumyHistorySerializer


class GoalStatusSerializerViewSet(viewsets.ModelViewSet):
    queryset = GoalStatus.objects.all()
    serializer_class = GoalStatusSerializer


class ScrumUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = ScrumUser.objects.all()
    serializer_class = ScrumUserSerializer
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        print("wrong post")

        if not request.data.get('role'):
            return Response(status=401)

        print(request.data.get('role'))

        try:
            group = Group.objects.get(name=request.data.get('role'))
        except ObjectDoesNotExist:
            print("1. exception")
            return Response(status=401)

        form_data = {
            "first_name": request.data.get("firstname"),
            "last_name": request.data.get("lastname"),
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "group": group.id,
            "password": request.data.get("password"),
            "confirm_password": request.data.get("password")
        }

        form = SignupForm(form_data)

        if form.is_valid():
            print("valid form data")
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            group = form.cleaned_data.get('group')
            password = form.cleaned_data.get('password')
            password2 = form.cleaned_data.get('confirm_password')

            if not User.objects.filter(email=email):
                new_user = User(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                username=username
                                )
                new_user.set_password(password)

                try:
                    print("group name:", group.name)
                    group = Group.objects.get(name=group)
                    new_user.save()
                except ObjectDoesNotExist:
                    print("2. exception")
                    context = {'message': "Group doesn't exist"}
                    return Response(status=400,)

                group.user_set.add(new_user)
                serializer = UserSerializer(new_user)

                # handle creating a new project if user is owner
                if group.name == "Owner":
                    group = Group.objects.get(name="Owner")
                    print("lets make a  new project")
                    project_name = request.data.get('new_project')
                    print("project-name: ", request.data)
                    new_project = Project(name=project_name, created_by=new_user.username, time_of_creation=datetime.now())
                    new_project.save()

                    project_roles_entry = ProjectRoles(user=new_user, project=new_project, role=group)
                    project_roles_entry.save()

                return Response(serializer.data, status=200)
            print("3. exception")
            return Response(status=400)
        print(form.errors)
        print("4. exception")
        return Response(status=400)

    @action(methods=['get'], detail=True, url_path='user-projects', url_name='user_projects')
    def get_user_projects(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            projects = user.project_set.all()
        except ObjectDoesNotExist:
            return Response(status=400)

        serializer = ProjectSerializer(projects, many=True)

        # print(serializer.data)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, url_path='add-user-project', url_name='add_user_project')
    def add_user_project(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            project = Project.objects.filter(id=request.data.get('project_id')).first()
            if project:
                group = Group.objects.get(name="User")
                print("add_user_project: ", group.name)
                # project.users.add(user)
                # project.save()
                project_role_entry = ProjectRoles(user=user, project=project, role=group)
                project_role_entry.save()
        except ObjectDoesNotExist:
            return Response(status=400)

        serializer = ProjectSerializer(project, many=False)

        print(serializer.data)
        return Response(serializer.data)


class ProjectSerializerViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = ()
    permission_classes = []


class ProjectSerializerAuthViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, *args, **kwargs):

        try:
            group = Group.objects.get(name="Owner")
            owner = User.objects.get(pk=request.data.get('user_id'))
        except ObjectDoesNotExist:
            return Response(status=401)

        print("lets make a  new project")
        project_name = request.data.get('name')

        print("project-name: ", request.data)

        new_project = Project(name=project_name, created_by=owner.username, time_of_creation=datetime.now())
        new_project.save()

        project_roles_entry = ProjectRoles(user=owner, project=new_project, role=group)
        project_roles_entry.save()

        return Response("done")


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        user_group = user.groups.all().first()
        # projects = Project.objects.filter()
        print(user.project_set.all())
        print(user)

        user_projects = user.project_set.all()

        serializer = ProjectSerializer(user_projects, many=True)

        print(serializer.data)

        token_obj = Token.objects.get(user=user)

        # Add custom claims
        token['id'] = user.id
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['role'] = str(user_group)
        token['projects'] = serializer.data
        token['token'] = token_obj.key
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class CustomTokenAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data.get('user'),
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_group = user.groups.all().first()

        response = {
            'token': token.key,
            'id': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'role': str(user_group),
        }

        if request.data.get('project_id'):

            try:
                project = Project.objects.get(pk=request.data.get('project_id'))

                if not user.project_set.filter(pk=project.id).exists():
                    group = Group.objects.get(name="User")
                    print("add_user_project: ", group.name)
                    # project.users.add(user)
                    # project.save()
                    project_role_entry = ProjectRoles(user=user, project=project, role=group)
                    project_role_entry.save()

                    response['project'] = project.id
                    response['project_creator'] = project.created_by
            except ObjectDoesNotExist:
                print("no login")
                return Response(status=400)

        return Response(response)
