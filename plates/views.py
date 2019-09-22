from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from commons.views import CommonMixinListView, CommonMixinCreateView,\
    CommonMixinUpdateView, CommonMixinDeleteView
from meals.models import Meal
from .models import Plate
from .forms import PlateModelForm
from .serializers import PlateSerializer


class PlateViewSet(viewsets.ModelViewSet):
    '''
    View for Plate
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Plate.objects.all()
    serializer_class = PlateSerializer

    def get_meals(self, data):
        meals = []
        if 'meals' in data:
            meals = Meal.objects.filter(id__in=data.get('meals', []))
        return meals

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            meals=self.get_meals(self.request.data)
        )

    def perform_update(self, serializer):
        serializer.save(
            owner=self.request.user,
            meals=self.get_meals(self.request.data)
        )

    def get_queryset(self):
        return Plate.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class PlateListView(CommonMixinListView):
    model = Plate
    create_url = 'plate-create'
    update_url = 'plate-update'
    delete_url = 'plate-delete'


@method_decorator(login_required, name='dispatch')
class PlateCreateView(CommonMixinCreateView):
    form_class = PlateModelForm
    model = Plate
    template_name = 'crud/create.html'
    success_url = reverse_lazy('plate-list')
    titlename = 'Agregar Plato'

    def form_valid(self, form):
        plate = form.save(commit=False)
        plate.owner = self.request.user
        plate.save()
        plate.meals.set(form.cleaned_data['meals'])
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PlateUpdateView(CommonMixinUpdateView):
    form_class = PlateModelForm
    model = Plate
    template_name = 'crud/create.html'
    success_url = reverse_lazy('plate-list')
    titlename = 'Editar Plato'

    def get_initial(self):
        initial = super(PlateUpdateView, self).get_initial()
        initial['meals'] = self.get_object().meals.all()
        return initial

    def form_valid(self, form):
        plate = form.save()
        plate.meals.set(form.cleaned_data['meals'])
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class PlateDeleteView(CommonMixinDeleteView):
    model = Plate
    url = reverse_lazy('plate-list')
