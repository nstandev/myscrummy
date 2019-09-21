from django.contrib import admin
from .models import ScrumyGoals, ScrumyHistory, GoalStatus, Project, ProjectRoles

# Register your models here.

admin.site.register(ScrumyGoals)
admin.site.register(ScrumyHistory)
admin.site.register(GoalStatus)
admin.site.register(Project)
admin.site.register(ProjectRoles)
