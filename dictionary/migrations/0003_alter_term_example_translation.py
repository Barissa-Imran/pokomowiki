# Generated by Django 4.0.4 on 2022-06-30 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0002_term_example_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='example_translation',
            field=models.TextField(default='Example not translated'),
        ),
    ]