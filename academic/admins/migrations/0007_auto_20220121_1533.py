# Generated by Django 3.2.5 on 2022-01-21 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admins', '0006_modulecontent_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='deadline',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='title',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
