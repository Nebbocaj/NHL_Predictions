# Generated by Django 4.2 on 2023-07-03 12:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0008_stats_fantasypoints"),
    ]

    operations = [
        migrations.AddField(
            model_name="season",
            name="current_season",
            field=models.BooleanField(default=True),
        ),
    ]