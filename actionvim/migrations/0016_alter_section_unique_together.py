# Generated by Django 4.2.7 on 2023-12-05 18:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("actionvim", "0015_task_members"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="section",
            unique_together=set(),
        ),
    ]
