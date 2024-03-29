# Generated by Django 3.0.8 on 2020-11-21 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applications', '0005_auto_20201120_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='lottery_status',
            field=models.CharField(blank=True, choices=[('Lottery', 'Lottery'), ('Waitlist', 'Waitlist'), ('Admitted', 'Admitted'), ('Registered', 'Registered'), ('Declined', 'Declined')], default='Lottery', max_length=200, null=True),
        ),
    ]
