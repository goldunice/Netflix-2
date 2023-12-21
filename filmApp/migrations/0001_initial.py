# Generated by Django 5.0 on 2023-12-21 15:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aktyor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ism', models.CharField(max_length=255)),
                ('davlat', models.CharField(max_length=255)),
                ('jins', models.CharField(max_length=255)),
                ('tugilgan_yil', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('narx', models.PositiveIntegerField()),
                ('davomiylik', models.DurationField()),
            ],
        ),
        migrations.CreateModel(
            name='Kino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('janr', models.CharField(max_length=255)),
                ('yil', models.DateField(blank=True, null=True)),
                ('aktyor', models.ManyToManyField(to='filmApp.aktyor')),
            ],
        ),
        migrations.CreateModel(
            name='Izoh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matn', models.TextField()),
                ('sana', models.DateField(auto_now_add=True)),
                ('baho', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmApp.kino')),
            ],
        ),
    ]
