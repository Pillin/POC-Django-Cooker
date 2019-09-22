from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import viewsets

from commons.views import CommonMixinListView, CommonMixinCreateView,\
    CommonMixinUpdateView, CommonMixinDeleteView
from .models import Tag
from .forms import TagModelForm
from .serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    '''
    View for Tag
    '''
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated, IsAuthenticatedOrReadOnly)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)


@method_decorator(login_required, name='dispatch')
class TagListView(CommonMixinListView):
    model = Tag
    create_url = 'tag-create'
    update_url = 'tag-update'
    delete_url = 'tag-delete'


@method_decorator(login_required, name='dispatch')
class TagCreateView(CommonMixinCreateView):
    form_class = TagModelForm
    model = Tag
    template_name = 'crud/create.html'
    success_url = reverse_lazy('tag-list')
    titlename = 'Etiqueta'


@method_decorator(login_required, name='dispatch')
class TagUpdateView(CommonMixinUpdateView):
    form_class = TagModelForm
    model = Tag
    template_name = 'crud/create.html'
    success_url = reverse_lazy('tag-list')
    titlename = 'Etiqueta'


@method_decorator(login_required, name='dispatch')
class TagDeleteView(CommonMixinDeleteView):
    model = Tag
    url = reverse_lazy('tag-list')
