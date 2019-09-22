from django.urls import path
from .views import PlateListView, PlateUpdateView, PlateCreateView, PlateDeleteView

urlpatterns = [
    path('list/', PlateListView.as_view(), name='plate-list'),
    path('<int:pk>/delete/', PlateDeleteView.as_view(), name='plate-delete'),
    path('<int:pk>/update/', PlateUpdateView.as_view(), name='plate-update'),
    path('create/', PlateCreateView.as_view(), name='plate-create'),
]
