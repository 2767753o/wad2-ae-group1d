# Generated by Django 2.1.5 on 2024-03-17 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blink_app', '0007_auto_20240317_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='likeID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]