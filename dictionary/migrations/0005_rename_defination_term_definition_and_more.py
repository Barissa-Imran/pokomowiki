# Generated by Django 4.0.3 on 2022-04-22 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_rename_approval_term_approved'),
    ]

    operations = [
        migrations.RenameField(
            model_name='term',
            old_name='defination',
            new_name='definition',
        ),
        migrations.RenameField(
            model_name='term',
            old_name='other_definations',
            new_name='other_definitions',
        ),
        migrations.AlterField(
            model_name='term',
            name='downvote',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='upvote',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]