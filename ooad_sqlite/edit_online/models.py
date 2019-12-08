from django.db import models


class Users(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=10)
    user_phone = models.CharField(unique=True, max_length=11)
    user_email = models.CharField(unique=True, max_length=45, blank=True, null=True)
    user_password = models.CharField(max_length=500)

    class Meta:
        db_table = 'Users'



