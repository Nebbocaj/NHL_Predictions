# Generated by Django 4.2.3 on 2023-07-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0017_goalieaverage_savepercentage"),
    ]

    operations = [
        migrations.AddField(
            model_name="goalieaverage",
            name="ot",
            field=models.FloatField(default=0),
        ),
    ]
