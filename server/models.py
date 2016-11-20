from django.db import models

class Project(models.Model):
    name        = models.CharField(max_length=300)
    description = models.CharField(max_length=8192)
    is_lab      = models.BooleanField(default=False)
    project_id  = models.IntegerField()

class Member(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    status      = models.CharField(max_length=100)
    comment     = models.CharField(max_length=300)
    member_id   = models.IntegerField()

class Crossings(models.Model):
    project_id  = models.ForeignKey(Project)
    member_id   = models.ForeignKey(Member)
    class Meta:
        unique_together = (('project_id', 'member_id'),)


class MemberInterest(models.Model):
    member_id   = models.ForeignKey(Member)
    interest1   = models.CharField(max_length=100)
    interest2   = models.CharField(max_length=100)
    interest3   = models.CharField(max_length=100)
    interest4   = models.CharField(max_length=100)
    interest5   = models.CharField(max_length=100)

class MemberSkills(models.Model):
    member_id   = models.ForeignKey(Member)
    skill1      = models.CharField(max_length=100)
    skill2      = models.CharField(max_length=100)
    skill3      = models.CharField(max_length=100)
    skill4      = models.CharField(max_length=100)
    skill5      = models.CharField(max_length=100)

class ProjectInterest(models.Model):
    project_id  = models.ForeignKey(Project)
    interest1   = models.CharField(max_length=100)
    interest2   = models.CharField(max_length=100)
    interest3   = models.CharField(max_length=100)
    interest4   = models.CharField(max_length=100)
    interest5   = models.CharField(max_length=100)

class ProjectSkills(models.Model):
    project_id  = models.ForeignKey(Project)
    skill1      = models.CharField(max_length=100)
    skill2      = models.CharField(max_length=100)
    skill3      = models.CharField(max_length=100)
    skill4      = models.CharField(max_length=100)
    skill5      = models.CharField(max_length=100)
