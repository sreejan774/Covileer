from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, OneToOneField



# Create your models here.
class UserProfile(models.Model):
    isVolunteer = models.BooleanField(default=False)
    isUser = models.BooleanField(default=False) 
    name = models.CharField(max_length=100,default='')

    contact = models.CharField(max_length=17,default='')
    address = models.CharField(max_length=100,default='')
    city = models.CharField(max_length=50,default='')
    state = models.CharField(max_length=50,default='')
    pincode = models.CharField(max_length=6,default='')

    user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class UserRequest(models.Model):
    requestList = models.TextField()
    requestStatus = models.BooleanField(default = False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} and {self.id}"


class Connection(models.Model):
    requestId = OneToOneField(UserRequest,on_delete=models.CASCADE)
    volunteerId = ForeignKey(User,on_delete=models.CASCADE)
    