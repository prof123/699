from django.db import models
from django import forms

#class MessageForm(forms.Form):
#    message = forms.CharField()

class Connections (models.Model) :
    """The connection Table"""
    uid1 = models.CharField(max_length=50)
    uid2 = models.CharField(max_length=50)
    #other misc connection info to go here..?
    
    def __str__(self):
        return '('+self.uid+','+ self.uid2+')'

class Users (models.Model) :
    uid = models.CharField(max_length=50,primary_key=True)
    status = models.CharField(max_length=10)
    partner = models.CharField(max_length=100)
    score1 = models.CharField(max_length=10)
    score2 = models.CharField(max_length=10)
    mq0 = models.CharField(max_length=1000)
    mq1 = models.CharField(max_length=1000)
    time = models.CharField(max_length=10)
    
    def __str__(self) :
        return repr((self.uid,self.status,self.partner,self.score1,self.score2,self.mq0,self.mq1,self.time))


class UserList(models.Model) :
    uid = models.CharField(max_length=50)

    def __str__(self):
        return self.uid

class FreeList(models.Model) :
    uid = models.CharField(max_length=50)
    
    def __str__(self):
        return self.uid
