# Generated by Django 4.2 on 2023-09-05 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("school_name", models.CharField(max_length=100)),
                ("faculty", models.CharField(max_length=100)),
                ("department", models.CharField(max_length=100)),
                ("hobbies", models.TextField(blank=True)),
                ("profile", models.TextField(blank=True)),
                ("age", models.IntegerField(blank=True, null=True)),
                ("grade", models.CharField(max_length=10, null=True)),
                ("gender", models.CharField(max_length=1)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]