from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from commons.views import CommonMixinListView, CommonMixinCreateView,\
    CommonMixinUpdateView, CommonMixinDeleteView
from tags.models import Tag
from .serializers import MealSerializer
from .forms import MealModelForm
from .models import Meal


class MealViewSet(viewsets.ModelViewSet):
    '''
    View for Meal
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_tags(self, data):
        tags = []
        if 'tags' in data:
            tags = Tag.objects.filter(id__in=data.getlist('tags', []))
        return tags

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            tags=self.get_tags(self.request.data)
        )

    def perform_update(self, serializer):
        serializer.save(
            owner=self.request.user,
            tags=self.get_tags(self.request.data)
        )

    def get_queryset(self):
        return Meal.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class MealListView(CommonMixinListView):
    model = Meal
    create_url = 'meal-create'
    update_url = 'meal-update'
    delete_url = 'meal-delete'


@method_decorator(login_required, name='dispatch')
class MealCreateView(CommonMixinCreateView):
    form_class = MealModelForm
    model = Meal
    template_name = 'crud/create.html'
    success_url = reverse_lazy('meal-list')
    titlename = 'Agregar Comida'

    def form_valid(self, form):
        meal = form.save(commit=False)
        meal.owner = self.request.user
        meal.save()
        meal.tags.set(form.cleaned_data['tags'])
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MealUpdateView(CommonMixinUpdateView):
    form_class = MealModelForm
    model = Meal
    template_name = 'crud/create.html'
    success_url = reverse_lazy('meal-list')
    titlename = 'Editar comida'

    def get_initial(self):
        initial = super(MealUpdateView, self).get_initial()
        initial['tags'] = self.get_object().tags.all()
        return initial

    def form_valid(self, form):
        meal = form.save()
        meal.tags.set(form.cleaned_data['tags'])
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class MealDeleteView(CommonMixinDeleteView):
    model = Meal
    url = reverse_lazy('meal-list')
