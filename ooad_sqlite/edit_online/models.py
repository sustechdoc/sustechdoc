from django.db import models


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=10)
    user_phone = models.CharField(unique=True, max_length=11)
    user_email = models.CharField(unique=True, max_length=45, blank=True, null=True)
    user_password = models.CharField(max_length=500)

    class Meta:
        db_table = 'Users'


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    project_name = models.CharField(max_length=40)
    creator_id = models.IntegerField()
    type = models.CharField(max_length=10)

    class Meta:
        db_table = 'Project'


class Authorize(models.Model):
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    can_write = models.IntegerField(default=0)
    class Meta:
        db_table = 'auth_pro'
        unique_together=("project_id","user_id")
