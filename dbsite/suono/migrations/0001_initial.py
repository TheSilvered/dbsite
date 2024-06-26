# Generated by Django 5.0.6 on 2024-06-05 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Suono',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_e_ora', models.DateTimeField()),
                ('laeq', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Intensita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequenza', models.FloatField()),
                ('intensita', models.FloatField()),
                ('suono', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suono.suono')),
            ],
        ),
    ]
