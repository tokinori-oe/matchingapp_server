# Generated by Django 4.2.5 on 2023-10-10 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiling", "0003_alter_userprofile_nickname"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="photo",
            field=models.ImageField(null=True, upload_to="profiling_photos/"),
        ),
    ]