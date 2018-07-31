from django.shortcuts import render

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Resource, Classroom, Subject, Activity
from .forms import ActivityRequirementsForm
# Create your views here.


class ResourceCreate(CreateView):
    model = Resource
    fields = ('name', 'description')


class ResourceUpdate(UpdateView):
    model = Resource
    fields = ('name', 'description')


class ResourceList(ListView):
    model = Resource


class ClassroomList(ListView):
    model = Classroom


class ClasroomDetail(DetailView):
    model = Classroom


class SubjectList(ListView):
    """a test view for listing the subjects a user can alter"""
    model = Subject


class ActivityList(ListView):
    """The main view for listing the activities a user can alter"""
    model = Activity


class ActivityRequirements(UpdateView):
    model = Activity
    form_class = ActivityRequirementsForm
