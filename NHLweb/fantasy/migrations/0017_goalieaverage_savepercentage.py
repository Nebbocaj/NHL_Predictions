# Generated by Django 4.2.3 on 2023-07-27 20:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0016_alter_centeraverage_assists_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="goalieaverage",
            name="savePercentage",
            field=models.FloatField(default=0),
        ),
    ]
