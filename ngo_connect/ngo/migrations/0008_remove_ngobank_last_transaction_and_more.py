# Generated by Django 5.0.2 on 2024-04-01 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0007_reciever_under_ngo_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ngobank',
            name='last_transaction',
        ),
        migrations.RemoveField(
            model_name='ngobank',
            name='transaction_log',
        ),
    ]
