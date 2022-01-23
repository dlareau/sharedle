# Generated by Django 3.2 on 2022-01-23 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesite', '0003_group_secret'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='groupmember',
            constraint=models.UniqueConstraint(fields=('user', 'group'), name='one_group'),
        ),
    ]