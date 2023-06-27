from django.db import models
import os
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.




class Employee(models.Model):

    #put mat as the unique id 
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User , null=True , on_delete=models.CASCADE)
    name = models.CharField(max_length=200 , null=True , unique=True)
    matricule = models.CharField(max_length=200 , null=True , unique=True)
    email = models.CharField(max_length=50 , null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
    




class Files(models.Model):
    fiche = models.FileField(null="True")
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.fiche.name
    def get_file_name(self):
        return self.fiche.name


