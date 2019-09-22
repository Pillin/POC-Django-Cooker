from django.forms import ModelForm, ModelMultipleChoiceField
from commons.widgets import SelectMultiplePickerInput
from tags.models import Tag
from .models import Meal


class MealModelForm(ModelForm):
    tags = ModelMultipleChoiceField(
        required=False,
        widget=SelectMultiplePickerInput(),
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Meal
        fields = (
            'name', 'tags'
        )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MealModelForm, self).__init__(*args, **kwargs)
        tags = Tag.objects\
            .filter(owner=user)
        self.fields['tags'].queryset = tags

        if 'tags' in self.initial:
            self.fields['tags'].initial = self.initial['tags']
