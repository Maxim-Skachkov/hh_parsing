from django.db import models

# Create your models here.


class KeySkill(models.Model):
    skill_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.skill_name


class Vacancy(models.Model):
    job_name = models.CharField(max_length=150, null=False)
    salary_min = models.PositiveIntegerField(null=True)
    salary_max = models.PositiveIntegerField(null=True)
    salary_tax = models.CharField(max_length=50)
    job_expirience = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100, null=False)
    job_description = models.TextField()
    key_skills = models.ManyToManyField(KeySkill)

    def __str__(self):
        return f"{self.company_name} *** {self.job_name}"