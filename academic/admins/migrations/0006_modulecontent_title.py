# Generated by Django 3.2.5 on 2022-01-21 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0005_auto_20220121_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='modulecontent',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
