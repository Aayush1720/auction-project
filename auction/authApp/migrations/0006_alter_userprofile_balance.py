# Generated by Django 4.1 on 2022-08-29 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0005_userprofile_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='balance',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
