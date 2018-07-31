from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ACTIVITYTYPES = (
    ('P', 'Predavanja'),
    ('L', 'Laboratorijske vaje'),
    ('A', 'Avditorne vaje'),
)


class Classroom(models.Model):
    """A classroom"""
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=32)
    resources = models.ManyToManyField('Resource', through='Provides')

    def __str__(self):
        return "{}".format(self.short_name)


class Provides(models.Model):
    """What is provided by a classroom.
    e.g. if a classroom has 18 chairs, n should be set to 18.
    If the classroom has a window to the west, n may be set to NULL."""
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE)
    n = models.IntegerField(null=True, blank=True)
    classroom = models.ForeignKey('Classroom', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.classroom, self.resource)


class Resource(models.Model):
    """Anything that might be present in a classroom"""
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)

    def __str__(self):
        return "{}".format(self.name)


class Teacher(models.Model):
    """A model extending django.contrib.auth.models.User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.user)


class Subject(models.Model):
    """e. g. Math 101"""
    code = models.CharField(max_length=16, blank=True, unique=True)
    name = models.CharField(max_length=256)
    short_name = models.CharField(max_length=32, blank=True, default="")

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class Activity(models.Model):
    """An activity (e.g. lab exercises for Math 101)"""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lecture_type = models.CharField(max_length=16, choices=ACTIVITYTYPES)
    teachers = models.ManyToManyField(Teacher)
    requirements = models.ManyToManyField(Resource, blank=True)

    def __str__(self):
        return "{} ({})".format(self.subject.short_name, self.lecture_type)
