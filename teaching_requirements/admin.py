from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import\
    Classroom, Provides, Resource, \
    Teacher, Subject, Activity


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


admin.site.register(Classroom, ClassroomAdmin)
# admin.site.register(Provides)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Teacher)
admin.site.register(Subject, SubjectAdmin)
# admin.site.register(Activity)
