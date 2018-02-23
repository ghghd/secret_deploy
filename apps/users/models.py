from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if not postData['email'] or not postData['first_name'] or not postData['last_name'] or not postData['password'] or not postData['conf']:
            errors['info'] = 'NO data'
            return errors
        if len(postData['first_name']) < 2 or len(postData['last_name'])<2:
            errors['name'] = 'Name fields should be more than 2 characters'
        if not postData['first_name'].isalpha() and postData['last_name'].isalpha():
            errors['char'] = 'Name fields can not contain numbers'
        if postData['password']< 8:
            errors['pass'] = 'Password must be more than two characters long'
        if postData['password']!= postData['conf']:
            errors['conf'] = 'Passwords do not match'
        users = User.objects.filter(email=postData['email'])
        if users:
            errors['email'] = "Email has already been used"
        if not EMAIL_REGEX.match(form['email']):
            errors['match'] = "Email format is invalid."
        return errors

    def register(self, postData):
        return self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))

    def login(self, postData):
        return self.get(email = postData['email'])

    def create_user(self, postData):
        user= User.objects.filter(email=postData['email'])
        password = postData['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email=postData['email'], password = hashed)
        return user


    def validate_login(self, postData):
        errors = {}
        user, created = User.objects.get_or_create(email=postData['email'])
        if not postData['email'] or not postData['password']:
            errors['name'] = 'Invalid'
            return errors
        if not User.objects.filter(email = postData['email']):
            errors['email'] = 'Email does not exist. Please register'
        if len(User.objects.filter(email = postData['email'])):
            b=User.objects.get(email= postData['email']).password
            password = b
            check = bcrypt.checkpw(postData['password'].encode(), password.encode())    
            if check != True:
                errors['password'] = 'Password does not exist'  
        return errors


    def add_secret(self, postData, userSecret_id):
        Secret.objects.create(secret = postData['secret'], users_id = userSecret_id)

    def add_like(self, postData, id, userSecret_id):
        this_secret = Secret.objects.get(id = id)
        this_user = User.objects.get(id = userSecret_id)
        this_secret.liked_by.add(this_user)
           

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    objects = UserManager()

class Secret(models.Model):
    secret = models.TextField(max_length = 1000)
    users = models.ForeignKey(User, related_name='secrets')
    liked_by = models.ManyToManyField(User, related_name="liked_secrets")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True) 
    