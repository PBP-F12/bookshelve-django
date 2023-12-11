# Generated by Django 4.2.6 on 2023-12-11 07:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0003_alter_bookmark_bookmark_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='bookmark_id',
            field=models.UUIDField(default=uuid.UUID('54ee7f01-1b3d-48c3-af66-8c535ae7309f'), primary_key=True, serialize=False, unique=True),
        ),
    ]
