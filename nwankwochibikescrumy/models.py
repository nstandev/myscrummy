from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class GoalStatus(models.Model):
    status_name = models.CharField(max_length=200)

    def __str__(self):
        return self.status_name


class ScrumyGoals(models.Model):
    goal_name = models.CharField(max_length=200)
    goal_id = models.IntegerField()
    created_by = models.CharField(max_length=200)
    moved_by = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)
    goal_status = models.ForeignKey(GoalStatus, on_delete=models.PROTECT)
    is_deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='goals')

    def __str__(self):
        output = """Goal name: {}
                    Created by: {}
                """.format(self.goal_name, self.created_by)
        return output

    class Meta:
        permissions = [
            ('can_change_as_admin', 'can change the goals status if in the admin group')
        ]


class ScrumyHistory(models.Model):
    moved_by = models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    moved_from = models.CharField(max_length=200)
    moved_to = models.CharField(max_length=200)
    time_of_action = models.DateTimeField(auto_now=True)
    goal = models.ForeignKey(ScrumyGoals, on_delete=models.PROTECT)


class ScrumUser(models.Model):
    pass


class Project(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=200)
    users = models.ManyToManyField(User)
    time_of_creation = models.DateTimeField(auto_now=True)

