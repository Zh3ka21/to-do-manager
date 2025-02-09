# Generated by Django 5.1.5 on 2025-02-08 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0003_project_deleted_at"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="deleted_at",
        ),
        migrations.AddField(
            model_name="project",
            name="deleted",
            field=models.BooleanField(default=False),
        ),
    ]
