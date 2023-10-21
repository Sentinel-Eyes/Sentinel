# Generated by Django 4.2.6 on 2023-10-21 20:46

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_name', models.CharField(max_length=100)),
                ('author_name', models.CharField(max_length=100)),
                ('book_price', models.IntegerField()),
                ('book_image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Criminal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criminal_firstname', models.CharField(default='', max_length=100)),
                ('criminal_middlename', models.CharField(default='', max_length=5)),
                ('criminal_lastname', models.CharField(default='', max_length=100)),
                ('criminal_description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='CriminalImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criminal_image', models.ImageField(upload_to=app.models.criminal_image_upload_to)),
                ('criminal', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.criminal')),
            ],
        ),
    ]
