# Generated by Django 4.0.4 on 2022-06-29 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='example_translation',
            field=models.TextField(default='English'),
        ),
    ]