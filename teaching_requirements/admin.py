from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import\
    Classroom, Provides, Resource, \
    Teacher, Subject, Activity, ResourceComment


# Register your models here.
class ActivityInline(admin.StackedInline):
    model = Activity
    fk_name = 'subject'
    can_delete = True
    filter_horizontal = ('teachers', 'requirements')


class SubjectAdmin(ImportExportActionModelAdmin):
    inlines = (ActivityInline, )
    search_fields = ('name', 'short_name', 'code')


class ClassroomProvidesInline(admin.TabularInline):
    model = Provides
    fk_name = 'classroom'
    can_delete = True


class ClassroomAdmin(ImportExportActionModelAdmin):
    inlines = (ClassroomProvidesInline, )


class ResourceProvidedInline(admin.TabularInline):
    model = Provides
    fk_name = 'resource'
    can_delete = True


class ResourceAdmin(ImportExportActionModelAdmin):
    inlines = (ResourceProvidedInline, )


class TeacherAdmin(ImportExportActionModelAdmin):
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'code',
    ]
    model = Teacher


class ResourceCommentAdmin(ImportExportActionModelAdmin):
    search_fields = [
        'teacher__user__username',
        'teacher__user__first_name',
        'teacher__user__last_name',
        'resource__name',
    ]
    model = ResourceComment


admin.site.register(Classroom, ClassroomAdmin)
# admin.site.register(Provides)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(ResourceComment, ResourceCommentAdmin)
admin.site.register(Subject, SubjectAdmin)
# admin.site.register(Activity)
