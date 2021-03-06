# Generated by Django 4.0.4 on 2022-07-16 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary', '0004_alter_term_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='term',
            name='meta_description',
            field=models.CharField(default='pokomo,', help_text='Content for description meta tag', max_length=255, verbose_name='Meta Description'),
        ),
        migrations.AddField(
            model_name='term',
            name='meta_keywords',
            field=models.CharField(default='pokomo,', help_text='Comma-delimited set of SEO keywords for meta tag', max_length=255, verbose_name='Meta Keywords'),
        ),
        migrations.AlterField(
            model_name='term',
            name='dialect',
            field=models.CharField(choices=[('Ndera', 'Ndera'), ('Zubaki', 'Zubaki'), ('Kinakomba', 'Kinakomba'), ('Gwano', 'Gwano'), ('Malanchini', 'Malanchini'), ('All dialects', 'All dialects'), ('None', 'None')], max_length=50),
        ),
    ]
