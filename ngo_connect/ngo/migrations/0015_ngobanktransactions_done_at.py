# Generated by Django 5.0.2 on 2024-04-11 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ngo', '0014_alter_ngobanktransactions_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ngobanktransactions',
            name='done_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
