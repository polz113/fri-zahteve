from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext as _

from .models import Activity


class ActivityRequirementsForm(ModelForm):
    class Meta:
        model = Activity
        fields = ['requirements']
        widgets = {
            'requirements': FilteredSelectMultiple(
                verbose_name=_("requirements"), is_stacked=False)
        }
