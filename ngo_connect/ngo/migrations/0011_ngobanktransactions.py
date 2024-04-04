# Generated by Django 5.0.2 on 2024-04-04 17:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0010_remove_ngobank_is_balanced_defined'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NgoBankTransactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_balance', models.IntegerField(null=True)),
                ('transaction_id', models.CharField(max_length=10, null=True)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
