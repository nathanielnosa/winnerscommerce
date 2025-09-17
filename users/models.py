from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICES=(
    ('Male','Male'),
    ('Female','Female'),
)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    profile_pix = models.ImageField(null=True,blank=True ,upload_to='profile',default="https://img.favpng.com/17/24/10/computer-icons-user-profile-male-avatar-png-favpng-jhVtWQQbMdbcNCahLZztCF5wk.jpg")
    def __str__(self):
        return self.fullname
