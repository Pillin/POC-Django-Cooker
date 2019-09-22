from django.urls import path
from .views import TagListView, TagUpdateView, TagCreateView, TagDeleteView

urlpatterns = [
    path('list/', TagListView.as_view(), name='tag-list'),
    path('<int:pk>/delete/', TagDeleteView.as_view(), name='tag-delete'),
    path('<int:pk>/update/', TagUpdateView.as_view(), name='tag-update'),
    path('create/', TagCreateView.as_view(), name='tag-create'),
]
