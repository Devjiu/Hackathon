from django.db import models

class Projects(models.Model):
    name        = models.CharField(max_length=300)
    description = models.CharField(max_length=8192)
    project_id  = models.IntegerField()

class Member(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    member_id   = models.IntegerField()

class Crossings(models.Model):
    project_id  = models.ForeignKey(Projects)
    member_id   = models.ForeignKey(Member)
    class Meta:
        unique_together = (('project_id', 'member_id'),)


class MemberInterest(models.Model):
    member_id   = models.ForeignKey(Member)

