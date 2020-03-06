# Generated by Django 2.1.8 on 2019-12-16 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edit_online', '0002_project'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authorize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('can_write', models.IntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='project',
            old_name='creater_id',
            new_name='creator_id',
        ),
        migrations.RemoveField(
            model_name='project',
            name='user_id',
        ),
    ]
