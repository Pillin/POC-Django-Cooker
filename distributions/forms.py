from django.conf import settings
from django.forms import ModelForm, TimeField
from commons.widgets import TimePickerInput
from .models import Distribution


class DistributionModelForm(ModelForm):
    distribution_hour_link = TimeField(
        input_formats=(settings.TIME_FORMAT,),
        widget=TimePickerInput(
            attrs={'placeholder': 'Seleccione una hora'}
        ))
    end_available_distribution_link = TimeField(
        input_formats=(settings.TIME_FORMAT,),
        widget=TimePickerInput(
            attrs={'placeholder': 'Seleccione una hora'}
        ))

    class Meta:
        model = Distribution
        fields = (
            'name',
            'link_id',
            'distribution_hour_link',
            'end_available_distribution_link',
        )

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(DistributionModelForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        end_time = cleaned_data.get('end_available_distribution_link')
        initial_time = cleaned_data.get('distribution_hour_link')
        if end_time and initial_time and end_time < initial_time:
            self.add_error('end_available_distribution_link', "La hora tiene que ser mayor que la inicial")
