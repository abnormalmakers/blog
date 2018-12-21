from django.db import models

# Create your models here.
class Users(models.Model):
    phone=models.CharField(max_length=11)
    password=models.CharField(max_length=150)
    is_active=models.BooleanField()

    def __str__(self):
        return self.phone

    class Meta:
        db_table='users'
        verbose_name='用户'
        verbose_name_plural=verbose_name
