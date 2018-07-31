from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Activity


class ActivityRequirementsForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['requirements']
        widgets = {
            'requirements': FilteredSelectMultiple(
                verbose_name="requirements", is_stacked=False)
        }

