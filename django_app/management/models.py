from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # 添加自定义用户字段
    # 例如：profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return self.username
