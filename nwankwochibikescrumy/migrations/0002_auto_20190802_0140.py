# Generated by Django 2.2.3 on 2019-08-02 00:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nwankwochibikescrumy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scrumygoals',
            options={'permissions': [('can_change_as_admin', 'can change the goals status if in the admin group')]},
        ),
    ]
