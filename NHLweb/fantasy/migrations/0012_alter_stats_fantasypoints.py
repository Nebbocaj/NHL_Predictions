# Generated by Django 4.2 on 2023-07-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0011_stats_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stats",
            name="fantasyPoints",
            field=models.FloatField(default=0),
        ),
    ]
