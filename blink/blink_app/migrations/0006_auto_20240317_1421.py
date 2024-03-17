# Generated by Django 2.1.5 on 2024-03-17 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blink_app', '0005_auto_20240314_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='likeID',
            field=models.AutoField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]