# Generated by Django 4.2.4 on 2024-04-25 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reciever', '0009_recieverrequestgoods_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecieverResidents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=20)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], max_length=8, null=True)),
                ('reciever', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]