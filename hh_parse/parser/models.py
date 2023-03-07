from django.db import models

# Create your models here.


class Vacancy(models.Model):
    name = models.CharField(max_length=150, null=False)
    salary_min = models.PositiveIntegerField(null=True)
    salary_max = models.PositiveIntegerField(null=True)
    company_name = models.CharField(max_length=100, null=False)
    #tags = models.