from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from commons.views import CommonMixinListView
from .models import Delivery, DeliverySelection
from .forms import DeliverySelectionForm


class DeliverySelectionView(FormView):
    form_class = DeliverySelectionForm
    template_name = 'deliveries/selection.html'
    success_url = reverse_lazy('thanks')

    def get(self, request, *args, **kwargs):
        delivery_id = str(self.kwargs.get('id'))
        try:
            delivery = Delivery.objects.get(menu_delivery_id=delivery_id)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse_lazy('sadness'))

        if (delivery.is_finished_booking()):
            return HttpResponseRedirect(reverse_lazy('sadness'))
        return super(DeliverySelectionView, self).get(request, args, kwargs)

    def get_success_url(self):
        return self.success_url

    def get_form_kwargs(self):
        kwargs = super(DeliverySelectionView, self).get_form_kwargs()
        kwargs['id'] = str(self.kwargs.get('id'))
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        delivery_id = str(self.kwargs.get('id'))
        delivery = Delivery.objects.get(menu_delivery_id=delivery_id)
        delivery_selection = DeliverySelection.objects.create(
            name=cleaned_data['name'],
            description=cleaned_data['description'],
            delivery_id=delivery_id,
            owner=delivery.owner
        )
        delivery_selection.plates.set(cleaned_data['plates'])
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class DeliverySelectionListView(CommonMixinListView):
    model = DeliverySelection
