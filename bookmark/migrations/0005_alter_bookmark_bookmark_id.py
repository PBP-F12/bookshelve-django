# Generated by Django 4.2.6 on 2023-12-21 12:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0004_alter_bookmark_bookmark_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='bookmark_id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True),
        ),
    ]