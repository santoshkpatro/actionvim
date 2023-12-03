# Generated by Django 4.2.7 on 2023-12-03 19:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("actionvim", "0011_task_archived_position_alter_task_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="section",
            name="archived_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="section",
            name="archived_position",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="section",
            name="position",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
