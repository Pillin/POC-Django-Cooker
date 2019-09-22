from datetime import date

from django.conf import settings
from django.forms import ModelForm, ModelMultipleChoiceField, DateField

from commons.widgets import SelectMultiplePickerInput, DatePickerInput
from plates.models import Plate
from .models import Menu


class MenuModelForm(ModelForm):
    plates = ModelMultipleChoiceField(
        required=True,
        widget=SelectMultiplePickerInput(),
        queryset=Plate.objects.all()
    )

    date = DateField(
        input_formats=[settings.DATE_FORMAT],
        widget=DatePickerInput(
            attrs={
                'placeholder': 'Seleccione una fecha',
                'minDate': date.today()
            }
        ))

    class Meta:
        model = Menu
        fields = (
            'name', 'date', 'plates'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MenuModelForm, self).__init__(*args, **kwargs)
        if ('deliveries' in self.initial):
            self.fields['date'].initial = self.initial['deliveries'].first().date
        plates = Plate.objects\
            .filter(owner=user)
        self.fields['plates'].widget.queryset = plates
        if 'plates' in self.initial:
            self.fields['plates'].initial = self.initial['plates']
