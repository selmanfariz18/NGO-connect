# Generated by Django 5.0.2 on 2024-04-20 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reciever', '0005_recieverrequests'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recieverrequests',
            old_name='ting_quantity',
            new_name='thing_quantity',
        ),
    ]
