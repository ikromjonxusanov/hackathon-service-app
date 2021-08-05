# Generated by Django 3.2.5 on 2021-08-03 08:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serviceApp', '0004_alter_botusermodel_telegram_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='servicemodel',
            name='image',
            field=models.ImageField(default='default-service.png', upload_to='service'),
        ),
        migrations.RemoveField(
            model_name='ordermodel',
            name='service',
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='service',
            field=models.ManyToManyField(to='serviceApp.ServiceModel'),
        ),
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='serviceApp.botusermodel')),
            ],
        ),
        migrations.AddField(
            model_name='servicemodel',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='serviceApp.categorymodel'),
        ),
    ]
