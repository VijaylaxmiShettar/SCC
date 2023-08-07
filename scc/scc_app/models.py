from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    unique_id = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)

    class Meta:
        db_table="user"

class Complaint_registration(models.Model):
    unique_id = models.CharField(max_length=1500)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    complaint_type = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    ward_no = models.CharField(max_length=100)
    desc = models.CharField(max_length=1500)
    file_upload = models.FileField(upload_to='uploads/')
    complaint_status = models.FileField(max_length=100)

    class Meta:
        db_table="complaint_registration"

class Contact(models.Model):
    username = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100)
    message = models.CharField(max_length=225)

    class Meta:
        db_table="contact"