# Generated by Django 2.1.1 on 2018-11-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_auto_20181128_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='hits',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='number_of_songs',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='hits',
            field=models.IntegerField(default=0, null=True),
        ),
    ]