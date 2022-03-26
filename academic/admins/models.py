from django.db import models
from django.contrib.auth.models import User

class Result(models.Model):
    studentid = models.CharField(max_length=100)
    fullname=models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    semester = models.CharField(max_length=10)
    coursework = models.DecimalField(decimal_places=2,max_digits=5,null=True, blank=True)
    exam = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    marks = models.DecimalField(decimal_places=2,max_digits=5)
    status = models.CharField(max_length=5)


class ResultFile(models.Model):
    file = models.FileField(upload_to='static/results', null=True)
    result_cycle = models.CharField(max_length=200, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Courses(models.Model):
    course_name = models.CharField(max_length=200, null=True)
    course_desc = models.TextField(null=True)
    course_pic = models.FileField(upload_to='static/uploads', default='static/default_user.png', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.course_name


class Modules(models.Model):
    SEMESTER = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )
    module_code = models.CharField(max_length=200, null=True)
    module_name = models.CharField(max_length=200, null=True)
    module_desc =models.TextField(null=True)
    course = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    semester = models.CharField(max_length=100, null=True, choices=SEMESTER)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.module_name


class ModuleContent(models.Model):
    WEEK = (
        ('WEEK1', 'WEEK1'),
        ('WEEK2', 'WEEK2'),
        ('WEEK3', 'WEEK3'),
        ('WEEK4', 'WEEK4'),
        ('WEEK5', 'WEEK5'),
        ('WEEK6', 'WEEK6'),
        ('WEEK7', 'WEEK7'),
        ('WEEK8', 'WEEK8'),
        ('WEEK9', 'WEEK9'),
        ('WEEK10', 'WEEK10'),
        ('WEEK11', 'WEEK11'),
    )
    course = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    week = models.CharField(max_length=100, null=True, choices=WEEK)
    content = models.FileField(upload_to='static/uploads/modulecontent', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Assignment(models.Model):
    WEEK = (
        ('WEEK1', 'WEEK1'),
        ('WEEK2', 'WEEK2'),
        ('WEEK3', 'WEEK3'),
        ('WEEK4', 'WEEK4'),
        ('WEEK5', 'WEEK5'),
        ('WEEK6', 'WEEK6'),
        ('WEEK7', 'WEEK7'),
        ('WEEK8', 'WEEK8'),
        ('WEEK9', 'WEEK9'),
        ('WEEK10', 'WEEK10'),
        ('WEEK11', 'WEEK11'),
    )
    course = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    week = models.CharField(max_length=100, null=True, choices=WEEK)
    assignment_file = models.FileField(upload_to='static/uploads/assignment', null=True)
    deadline = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class SubmitAssignment(models.Model):
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    submission_file = models.FileField(upload_to='static/uploads/submissions', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Fees(models.Model):
    SEMESTER = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )
    course = models.ForeignKey(Courses, null=True, on_delete=models.CASCADE)
    semester = models.CharField(max_length=100, null=True, choices=SEMESTER)
    batch = models.IntegerField(null=True)
    fee = models.CharField(max_length=10, null=True)
    clearance_date = models.DateField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Enquiries(models.Model):
    fullname = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=10, null=True)
    message = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class UserModule(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, null=True, on_delete=models.CASCADE)


