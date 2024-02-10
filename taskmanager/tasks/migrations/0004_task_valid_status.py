# Generated by Django 4.2.2 on 2024-02-10 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_sprint_epic_task_epic_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="task",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("status__in", ["UNASSIGNED", "IN PROGRESS", "DONE", "ARCHIVED"])
                ),
                name="valid_status",
            ),
        ),
    ]