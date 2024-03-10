from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_student = models.BooleanField('student',default=False)
    is_teacher = models.BooleanField('teacher',default=False)
    avatar = models.ImageField(upload_to='avatar/')


    