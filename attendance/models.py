from django.db import models
from main.models import Employee, EmployeeWork


class EmployeePresence(models.Model):
    Employee = models.OneToOneField(Student, models.CASCADE)
    present = models.BooleanField(default=True)
    Employee_work = models.ForeignKey(EmployeeWork, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)  # when administrators empty the absents it changes to True and won't
    # appear in the least again
