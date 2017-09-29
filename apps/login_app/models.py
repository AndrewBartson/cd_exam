from __future__ import unicode_literals
from django.db import models
import bcrypt
import re


class UserManager(models.Manager):
    def creator(self, postData):
        user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], b_day= postData['b_day'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
    
    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        if len(postData['name'].strip()) < 3:
            results['errors'].append('First name is too short.')
            results['status'] = False
        if len(postData['alias'].strip()) < 2:
            results['errors'].append('Last name is too short.')
            results['status'] = False            
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False
        if len(postData['b_day'].strip()) < 8:
            results['errors'].append('Please enter valid birthday.')
            results['status'] = False
        if not postData['password'] == postData['c_password']:
            results['errors'].append("Passwords don't match.")
            results['status'] = False
        if ' ' in postData['password']:
            results['errors'].append("Password cannot have spaces.")
            results['status'] = False            
        if len(postData['password']) < 8:
            results['errors'].append("Password must have 8 or more characters.")
            results['status'] = False
        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append("User already exists.")
            results['status'] = False               
        print results
        return results

    def loginVal(self, postData):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = postData['email'])
        if len(users) < 1:
            results['status']  = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0] # user is valid, proceed
            else:
                results['status']  = False
        return results

class User(models.Model):
    name = models.CharField(max_length = 200)
    alias = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    b_day = models.DateField(default="1776-07-04")
    friends_user = models.ManyToManyField('self', related_name="user_friends")
    objects = UserManager()
