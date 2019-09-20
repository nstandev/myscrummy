# SignupForm and CreateGoalForm.
#  The signup form will contain fields from the User model
# such as first_name,last_name,email,username,password and the CreateGoalForm will contain
# the goal_name field and user field from the ScrumyGoals model.
# The user field will enable a user of you application select the particular user the
# goal is being created for.
from django.contrib.auth.models import User,Group
from django.forms import ModelForm, forms, PasswordInput
from django import forms

from nwankwochibikescrumy.models import ScrumyGoals, GoalStatus


class SignupForm (ModelForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    password = forms.CharField(widget=PasswordInput)
    confirm_password = forms.CharField(widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = True

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords must be the same")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "group", "password", "confirm_password"]


class CreateGoalForm(ModelForm):
    class Meta:
        model = ScrumyGoals
        fields = ['goal_name']
        # fields = ['goal_name', 'goal_status', 'user']
        # fields = ['goal_name', 'goal_status', 'user']


class MoveGoalForm(forms.Form):
    status_name = forms.ModelChoiceField(queryset=GoalStatus.objects.all())


class MoveGoalFormDeveloper(forms.Form):
    status_name = forms.ModelChoiceField(queryset=GoalStatus.objects.all())


class UpdateUserGroup(forms.Form):
    groups = forms.ModelChoiceField(queryset=Group.objects.all())
