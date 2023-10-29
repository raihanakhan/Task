from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=250, unique=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner')
    employee_count = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    email = models.EmailField(max_length=254, null=False, blank=False, unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __str__(self):
        return self.full_name


class EmploymentHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='employment_history')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employment_history')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{0} {1}".format(self.employee.full_name, self.company.name)
