from django.db import models

# Create your models here.


class Userinfo(models.Model):
    username = models.CharField(max_length=50, null=False,
                                unique=True)  # CharField()定义字符串类型的字段，max_length最大字符长度，null是否可以为空，unique是否唯一（是否是主键）。
    password = models.CharField(max_length=50, null=False, unique=False)
    email = models.CharField(max_length=50, null=True, unique=True)
    phone = models.CharField(max_length=50, null=False, unique=True)
    gender = models.CharField(max_length=50, null=True, unique=False)