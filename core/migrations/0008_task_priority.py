# Generated by Django 5.0.6 on 2024-06-15 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_task_created_at_task_updated_at_alter_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
