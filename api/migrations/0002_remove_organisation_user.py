# Generated by Django 5.0.6 on 2024-07-09 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='user',
        ),
    ]
