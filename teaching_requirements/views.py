from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.db.models.functions import Lower

from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.core.exceptions import PermissionDenied

from .models import Resource, Classroom, Subject, Activity
from .forms import ActivityRequirementsForm
# Create your views here.


class ResourceCreate(LoginRequiredMixin, CreateView):
    model = Resource
    fields = ('name', 'description')
    success_url = reverse_lazy("resource_list")


class ResourceUpdate(LoginRequiredMixin, UpdateView):
    model = Resource
    fields = ('name', 'description')
    success_url = reverse_lazy("resource_list")


class ResourceList(ListView):
    model = Resource


class ClassroomList(ListView):
    model = Classroom


class ClassroomDetail(DetailView):
    model = Classroom


class SubjectList(ListView):
    """a test view for listing the subjects a user can alter"""
    model = Subject


class ActivityList(LoginRequiredMixin, ListView):
    """The main view for listing the activities a user can alter"""
    model = Activity

    def get_queryset(self):
        try:
            result = self.request.user.teacher.activity_set.order_by(
                Lower('subject__name'), 'subject__code', '-lecture_type'
            )
        except Exception as e:
            result = Activity.objects.none()
        return result


class ActivityRequirements(LoginRequiredMixin, UpdateView):
    model = Activity
    form_class = ActivityRequirementsForm
    success_url = reverse_lazy("activity_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            activity = context['activity']
            teacher = self.request.user.teacher
            assert activity.teachers.filter(pk=teacher.pk).count() > 0
            # self.raise_exception = False
        except Exception as e:
            raise PermissionDenied
        return context
