# Generated by Django 5.0.4 on 2024-04-07 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='favorite',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
