# Generated by Django 3.2.5 on 2022-01-22 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0008_submitassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='fees',
            name='batch',
            field=models.IntegerField(null=True),
        ),
    ]
