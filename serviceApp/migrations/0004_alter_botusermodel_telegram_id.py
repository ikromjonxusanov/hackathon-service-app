# Generated by Django 3.2.5 on 2021-08-03 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serviceApp', '0003_alter_botusermodel_telegram_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='botusermodel',
            name='telegram_id',
            field=models.IntegerField(unique=True),
        ),
    ]
