from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from commons.views import CommonMixinListView, CommonMixinCreateView,\
    CommonMixinUpdateView, CommonMixinDeleteView
from plates.models import Plate
from distributions.models import Distribution
from deliveries.models import Delivery

from .models import Menu
from .forms import MenuModelForm
from .serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    '''
    View for Menu
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_plates(self, data):
        plates = []
        if 'plates' in data:
            plates = Plate.objects.filter(id__in=data.getlist('plates', []))
        return plates

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            plates=self.get_plates(self.request.data)
        )

    def perform_update(self, serializer):
        serializer.save(
            owner=self.request.user,
            plates=self.get_plates(self.request.data)
        )

    def get_queryset(self):
        return Menu.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class MenuListView(CommonMixinListView):
    model = Menu
    create_url = 'menu-create'
    update_url = 'menu-update'


@method_decorator(login_required, name='dispatch')
class MenuCreateView(CommonMixinCreateView):
    form_class = MenuModelForm
    model = Menu
    template_name = 'crud/create.html'
    success_url = reverse_lazy('menu-list')
    titlename = 'Agregar Menu'

    def validate_distribution(self, request, *args, **kwargs):
        distribution = Distribution.objects\
            .filter(owner=self.request.user).first()
        return not distribution

    def get(self, request, *args, **kwargs):
        if self.validate_distribution(self, request, *args, **kwargs):
            return HttpResponseRedirect(reverse_lazy('distribution-create'))
        return super(MenuCreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if self.validate_distribution(self, request, *args, **kwargs):
            return HttpResponseRedirect(reverse_lazy('distribution-create'))
        return super(MenuCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        distribution = Distribution.objects\
            .filter(owner=self.request.user).first()
        menu = Menu(owner=self.request.user, name=form.cleaned_data['name'])
        menu.save()
        menu.plates.set(form.cleaned_data['plates'])
        delivery = Delivery(
            date=form.cleaned_data['date'],
            menu=menu,
            distribution=distribution,
            owner=self.request.user
        )
        delivery.save()
        menu.send_slack_link()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MenuUpdateView(CommonMixinUpdateView):
    form_class = MenuModelForm
    model = Menu
    template_name = 'crud/create.html'
    success_url = reverse_lazy('menu-list')
    titlename = 'Editar Menu'

    def get_initial(self):
        initial = super(MenuUpdateView, self).get_initial()
        delivery = self.get_object().deliveries.first()
        initial['plates'] = self.get_object().plates.all()
        initial['date'] = delivery.date if delivery else None
        return initial

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        instance.plates.set(form.cleaned_data['plates'])
        delivery = form.instance.deliveries.first()
        delivery.date = form.cleaned_data['date']
        delivery.save()
        instance.send_slack_link()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MenuDeleteView(CommonMixinDeleteView):
    model = Menu
    url = reverse_lazy('menu-list')
