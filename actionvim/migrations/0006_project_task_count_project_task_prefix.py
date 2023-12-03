# Generated by Django 4.2.7 on 2023-12-02 12:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actionvim", "0005_project_users_alter_project_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="task_count",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="project",
            name="task_prefix",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
