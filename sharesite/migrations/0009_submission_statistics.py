# Generated by Django 3.2 on 2022-01-26 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharesite', '0008_auto_20220124_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='statistics',
            field=models.JSONField(blank=True, null=True),
        ),
    ]