from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user    = models.OneToOneField(User,related_name='profile_user', on_delete=models.CASCADE)
    boi     = models.TextField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now=True, blank=True,null=True)
    photo   = models.ImageField(upload_to='profile_img/',blank=True, null=True)

    def __str__(self):
    	return "Profile of user {}".format(self.user.username)
	 

    