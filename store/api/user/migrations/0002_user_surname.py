# Generated by Django 4.2.5 on 2023-10-01 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
