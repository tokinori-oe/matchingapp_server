from django.db import models
from django.contrib.auth.models import  User

# Create your models here.

class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length =20, unique= False, default = '')
    school_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hobbies = models.TextField(blank = True)
    profile = models.TextField(blank = True)
    age = models.IntegerField(blank=True, null=True)
    grade = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=1, null=False)
    
    class Meta:
        app_label = 'profiling'
    
    def __str__(self):
        return self.user.username #ユーザー名を返すことでプロフィールを識別
    