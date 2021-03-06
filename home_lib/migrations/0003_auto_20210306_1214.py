# Generated by Django 3.1.7 on 2021-03-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_lib', '0002_auto_20210306_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='language',
            field=models.CharField(choices=[('FR', 'French'), ('EN', 'English'), ('NO', 'Norwegian'), ('PL', 'Polish'), ('RU', 'Russian'), ('UA', 'Ukrainian')], max_length=2),
        ),
    ]
