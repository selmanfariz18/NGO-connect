# Generated by Django 5.0.2 on 2024-03-30 14:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0005_remove_reciever_under_ngo_reciever_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reciever_under_ngo',
            name='id',
        ),
        migrations.AlterField(
            model_name='reciever_under_ngo',
            name='reciever',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='received_ngo', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
