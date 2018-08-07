from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path(r'', RedirectView.as_view(
        pattern_name='activity_list', permanent=False), name='index'),
    # path('subject', views.SubjectList.as_view(), name='subject_list'),
    # path('subject/<int:pk>/requirements',
    #      views.SubjectRequirements.as_view(),
    #      name='subject_requirements'),
    path('activity', views.ActivityList.as_view(), name='activity_list'),
    path('activity/nojs.html', views.ActivityList.as_view(
        template="activity_list_nojs.html"), name='activity_list_nojs'),
    path('activity/<int:pk>/requirements',
         views.ActivityRequirements.as_view(),
         name='activity_requirements'),
    path('classroom', views.ClassroomList.as_view(), name='classroom_list'),
    path('classroom/<int:pk>',
         views.ClassroomDetail.as_view(), name='classroom_detail'),
    path('resource', views.ResourceList.as_view(), name='resource_list'),
    path('resource/create', views.ResourceCreate.as_view(),
         name='resource_create'),
    # path('resource/<int:pk>/update', views.ResourceUpdate.as_view(),
    #      name='resource_update'),
]
