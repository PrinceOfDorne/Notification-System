# Generated by Django 3.2.9 on 2021-12-08 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20211207_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='schedule_created',
            field=models.IntegerField(default=0),
        ),
    ]
