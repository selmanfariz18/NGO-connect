# Generated by Django 5.0.2 on 2024-04-23 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reciever', '0008_recieverrequestgoods'),
    ]

    operations = [
        migrations.AddField(
            model_name='recieverrequestgoods',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
