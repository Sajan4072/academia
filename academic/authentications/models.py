from django.db import models
from django.contrib.auth.models import User
from admins.models import Courses


class Profile(models.Model):
    MARITAL_STATUS = (
        ('Single', 'Single'),
        ('Married', 'Married')
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True)
    middlename = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=200, choices=GENDER, null=True)
    dob = models.DateField(null=True)
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS, null=True)
    batch = models.IntegerField(null=True)
    course = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    guardian_name= models.CharField(max_length=200, null=True)
    guardian_phone = models.CharField(max_length=10, null=True)
    profile_pic = models.FileField(upload_to='static/uploads', default='static/default_user.png')
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username


class Others(models.Model):
    JOB_TYPE = (
        ('Full time', 'Full time'),
        ('Part time', 'Part time')
    )
    MARITAL_STATUS = (
        ('Single', 'Single'),
        ('Married', 'Married')
    )
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )
    JOB_ROLE = (
        ('Lecturer', 'Lecturer'),
        ('Administration', 'Administration'),
        ('Exam', 'Exam'),
        ('Account', 'Account'),
        ('Frontdesk', 'Frontdesk'),
        ('BOD', 'BOD'),
    )
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True)
    middlename = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True)
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255, null=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=200, choices=GENDER, null=True)
    marital_status = models.CharField(max_length=200, choices=MARITAL_STATUS, null=True)
    job_type = models.CharField(choices=JOB_TYPE, max_length=200, null=True)
    job_role = models.CharField(choices=JOB_ROLE, max_length=200, null=True)
    emergency_contact_name= models.CharField(max_length=200, null=True)
    emergency_contact_no = models.CharField(max_length=10, null=True)
    profile_pic = models.FileField(upload_to='static/uploads', default='static/default_user.png')
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username

