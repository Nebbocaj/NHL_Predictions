# Generated by Django 4.2 on 2023-06-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stats",
            name="assists",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="stats",
            name="goals",
            field=models.IntegerField(default=0),
        ),
    ]
