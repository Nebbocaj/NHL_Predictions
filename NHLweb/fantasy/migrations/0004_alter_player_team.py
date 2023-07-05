# Generated by Django 4.2 on 2023-06-29 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fantasy", "0003_team_player_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="team",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="fantasy.team"
            ),
        ),
    ]