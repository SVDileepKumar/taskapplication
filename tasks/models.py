from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserManager(models.Manager):
    def get(self, user_id):
        customuser=UserModel.objects.get(user=user_id)
        if customuser.user_role == 'employee':
            user_tasklists=[]
            tasklists=TasklistUserModel.objects.filter(user_id=user_id)
            for tasklist in tasklists:
                user_tasklists += TaskList.objects.filter(id=tasklist.id)
            return user_tasklists
        else:
            return TaskList.objects.all()

class Project(models.Model):
    description = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_followed = models.BooleanField(default=False)

    def enddate_check(self):
        if self.end_date <= self.start_date:
            raise ValidationError(
                ('%(end_date) can not be less than %(start_date)'),
                params={'end_date': self.end_date, 'start_date': self.start_date},
            )
    def __str__(self):
        return str(self.id)


class MileStone(models.Model):
    description = models.CharField(max_length=300, null=True, blank=True)
    project_id = models.ForeignKey(Project, null=True, blank=True)
    status = models.BooleanField(default='open')

    def __str__(self):
        return str(self.id)


class TaskList(models.Model):
    name=models.CharField(max_length=30)
    description = models.CharField(max_length=300, null=True, blank=True)
    milestone_id = models.ForeignKey(MileStone, null=True, blank=True)
    notes = models.CharField(max_length=300, null=True, blank=True)
    status = models.CharField(max_length=10,default='open',choices=(('open','open'),('closed','closed')))
    objects=models.Manager()
    user_objects=UserManager()

    def __str__(self):
        return str(self.id)


class TasksModel(models.Model):
    name = models.CharField(max_length=20)
    completion_status = models.FloatField(default=0)
    description = models.TextField(max_length=300, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    tasklist_id = models.ForeignKey(TaskList, null=True, blank=True)
    root_id = models.IntegerField(null=True, blank=True)
    parent_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name.title()


class UserModel(models.Model):
    user=models.ForeignKey(User)
    user_rate = models.FloatField(default=0)
    user_role=models.CharField(max_length=15,choices=(('employee','employee'),('manager','manager'),('admin','admin')),default='employee')
    contact_number = models.CharField(max_length=10,default='')
    project_id = models.ForeignKey(Project, null=True,blank=True)

    def __str__(self):
        return self.user.username.title()


class CommentsModel(models.Model):
    task_id = models.ForeignKey(TasksModel)
    comment = models.CharField(max_length=300)

    def __str__(self):
        return self.comment.title()

class TasklistUserModel(models.Model):
    tasklist_id=models.ForeignKey(TaskList)
    user_id=models.ForeignKey(User)
