from django.forms import Form, CharField, ModelMultipleChoiceField
from plates.models import Plate
from commons.widgets import SelectMultiplePickerInput
from .models import Delivery


class DeliverySelectionForm(Form):
    plates = ModelMultipleChoiceField(
        required=True,
        widget=SelectMultiplePickerInput(),
        queryset=Plate.objects.all()
    )
    name = CharField(
        label='Tu nombre',
        required=True
    )
    description = CharField(
        label='Alguna sugerencia',
        required=False
    )

    def __init__(self, *args, **kwargs):
        delivery_id = kwargs.pop('id', None)
        super(DeliverySelectionForm, self).__init__(*args, **kwargs)
        delivery = Delivery.objects.filter(
            menu_delivery_id=delivery_id).select_related('menu').get()
        plates = delivery.menu.plates.all()
        self.fields['plates'].queryset = plates
