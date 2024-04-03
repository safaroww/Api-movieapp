# Generated by Django 4.2.5 on 2023-09-12 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.director'),
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(to='movie.genre'),
        ),
    ]
