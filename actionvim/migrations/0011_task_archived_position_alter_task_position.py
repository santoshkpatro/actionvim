# Generated by Django 4.2.7 on 2023-12-03 19:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actionvim", "0010_alter_project_task_count_alter_task_public_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="archived_position",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="position",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
