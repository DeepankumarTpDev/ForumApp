# Generated by Django 5.1.1 on 2024-09-30 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_alter_post_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
