# Generated by Django 2.2.5 on 2019-12-06 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=10)),
                ('user_phone', models.CharField(max_length=11, unique=True)),
                ('user_email', models.CharField(blank=True, max_length=45, null=True, unique=True)),
                ('user_password', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'Users',
            },
        ),
    ]
