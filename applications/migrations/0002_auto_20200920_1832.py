# Generated by Django 3.0.8 on 2020-09-20 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicant',
            name='has_sibling',
        ),
        migrations.RemoveField(
            model_name='application',
            name='other_hear_option',
        ),
    ]
