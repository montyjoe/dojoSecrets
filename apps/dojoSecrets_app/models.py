from __future__ import unicode_literals

from django.db import models
import re
# import bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def register(self, data):
        errors = []
        if data['fname'] == "" or data['lname'] == "":
            errors.append("names may not be blank")
        elif len(data['fname']) < 2 or len(data['lname']) < 2:
            errors.append("first and last names must be at least 2 characters")
        if not data['fname'].isalpha() or not data['lname'].isalpha():
            errors.append("first and last names can only contain letters")
        if len(data['password']) < 8:
            errors.append("password must be at least 8 characters")
        if data['password'] != data['pass_conf']:
            errors.append("passwords do now match")
        if not EMAIL_REGEX.match(data['email']):
            errors.append('Email Must be Correct Format')
        if len(errors) == 0:
            user = User.objects.create(first_name=data['fname'], last_name=data['lname'], email=data['email'], password=data['password'],)
            print ('yes')
            return {'user':user, 'errors':None}
        else:
            print ('no')
            return {'user':None, 'errors':errors}

    def login(self, data):
        errors = []
        try:
            User.objects.get(email=data['email'])
        except:
            errors.append("username does not match")
            return {'user': None, 'errors':errors }
        if User.objects.get(email=data['email']).password == data['password']:
            user = User.objects.get(email=data['email'])
            return {'user':user, 'errors':None}
        else:
            return {'user': None, 'errors':errors}


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()

class Secret(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='secrets_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='user_likes')
    secret = models.ForeignKey(Secret, related_name='secret_likes')


# class SecretManager(models.Manager):
#     def register(self, data):
#
#
