from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets
from commons.views import CommonMixinCreateView, CommonMixinUpdateView
from .models import Distribution
from .serializers import DistributionSerializer
from .forms import DistributionModelForm


class DistributionViewSet(viewsets.ModelViewSet):
    '''
    View for Distribution
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Distribution.objects.all()
    serializer_class = DistributionSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Distribution.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class CreateDistributionView(CommonMixinCreateView):
    form_class = DistributionModelForm
    model = Distribution
    template_name = 'crud/create.html'
    success_url = reverse_lazy('home')
    titlename = 'Crear distribución'
    template_name = 'crud/create.html'

    def form_valid(self, form):
        distribution = form.save(commit=False)
        distribution.owner = self.request.user
        distribution.is_active = True
        distribution.save()
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class UpdateDistributionView(CommonMixinUpdateView):
    form_class = DistributionModelForm
    model = Distribution
    template_name = 'crud/create.html'
    success_url = reverse_lazy('home')
    titlename = 'Editar Distribución'
