# Generated by Django 4.0.4 on 2022-07-03 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0003_alter_term_example_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]