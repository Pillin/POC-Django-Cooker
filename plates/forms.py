from django.forms import ModelForm, ModelMultipleChoiceField
from commons.widgets import SelectMultiplePickerInput
from meals.models import Meal
from .models import Plate


class PlateModelForm(ModelForm):
    meals = ModelMultipleChoiceField(
        required=False,
        widget=SelectMultiplePickerInput(),
        queryset=Meal.objects.all()
    )

    class Meta:
        model = Plate
        fields = (
            'name', 'meals'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlateModelForm, self).__init__(*args, **kwargs)
        meals = Meal.objects\
            .filter(owner=user)
        self.fields['meals'].widget.queryset = meals
        if 'meals' in self.initial:
            self.fields['meals'].initial = self.initial['meals']
