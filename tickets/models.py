from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    mobile = models.CharField(max_length=20, null=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name


class Tehnician(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50)
    specializari = models.CharField(max_length=100, null=False)
    mobile = models.CharField(max_length=20, null=False)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.first_name


class Request(models.Model):
    cat = (
        ('servomotor', 'servomotor'),
        ('convertizor', 'convertizor')
    )
    category = models.CharField(max_length=50, choices=cat)

    reper_no = models.PositiveIntegerField(null=False)
    reper_name = models.CharField(max_length=40, null=False)
    reper_model = models.CharField(max_length=40, null=False)
    reper_brand = models.CharField(max_length=40, null=False)

    problem_description = models.CharField(max_length=500, null=False)
    date = models.DateField(auto_now=True)
    cost = models.PositiveIntegerField(null=True)

    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, null=True)
    tehnician = models.ForeignKey('Tehnician', on_delete=models.CASCADE, null=True)

    stat = (('In asteptare', 'In asteptare'),
            ('Aprobat', 'Aprobat'),
            ('In reparatie', 'In reparatie'),
            ('Reparat', 'Reparat'),
            ('Trimis', 'Trimis'))
    status = models.CharField(max_length=50, choices=stat, default='In asteptare', null=True)

    def __str__(self):
        return self.problem_description


class Attendance(models.Model):
    tehnician = models.ForeignKey('Tehnician', on_delete=models.CASCADE, null=True)
    date = models.DateField()
    present_status = models.CharField(max_length=10)


class Feedback(models.Model):
    date = models.DateField(auto_now=True)
    by = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
