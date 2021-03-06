# Generated by Django 2.0.2 on 2018-11-29 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20181128_2330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='songs_url',
        ),
        migrations.AddField(
            model_name='artist',
            name='songs_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='hits',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='artist',
            name='number_of_songs',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='artist',
            name='url',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='song',
            name='hits',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='song',
            name='url',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
