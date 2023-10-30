from django.db import models
from django.contrib.auth.models import User

class Education(models.Model):
    school_name = models.CharField(max_length=100)
    college_name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)


class WorkExperience(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    experience = models.IntegerField()

class Skill(models.Model):
    skill_name = models.CharField(max_length=100)

class Hobby(models.Model):
    hobby_name = models.CharField(max_length=100)


class Portfolio(models.Model):
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    email = models.EmailField(default=None, blank=False, null=True, unique=True)
    educations = models.ManyToManyField(Education, blank=True, related_name='portfolio_educations')
    work_experiences = models.ManyToManyField(WorkExperience, blank=True, related_name='portfolio_work_experiences')
    skills = models.ManyToManyField(Skill, blank=True, related_name='portfolio_skills')
    hobbies = models.ManyToManyField(Hobby, blank=True, related_name='portfolio_hobbies')
    additional_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.full_name