# Generated by Django 2.2.3 on 2019-09-20 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_by', models.CharField(max_length=200)),
                ('time_of_creation', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScrumUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ScrumyGoals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goal_name', models.CharField(max_length=200)),
                ('goal_id', models.IntegerField()),
                ('created_by', models.CharField(max_length=200)),
                ('moved_by', models.CharField(max_length=200)),
                ('owner', models.CharField(max_length=200)),
                ('is_deleted', models.BooleanField(default=False)),
                ('goal_status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nwankwochibikescrumy.GoalStatus')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='nwankwochibikescrumy.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('can_change_as_admin', 'can change the goals status if in the admin group')],
            },
        ),
        migrations.CreateModel(
            name='ScrumyHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moved_by', models.CharField(max_length=200)),
                ('created_by', models.CharField(max_length=200)),
                ('moved_from', models.CharField(max_length=200)),
                ('moved_to', models.CharField(max_length=200)),
                ('time_of_action', models.DateTimeField(auto_now=True)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nwankwochibikescrumy.ScrumyGoals')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nwankwochibikescrumy.Project')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(through='nwankwochibikescrumy.ProjectRoles', to=settings.AUTH_USER_MODEL),
        ),
    ]
