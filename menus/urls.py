from django.urls import path
from .views import MenuListView, MenuUpdateView, MenuCreateView, MenuDeleteView

urlpatterns = [
    path('list/', MenuListView.as_view(), name='menu-list'),
    path('<int:pk>/delete/', MenuDeleteView.as_view(), name='menu-delete'),
    path('<int:pk>/update/', MenuUpdateView.as_view(), name='menu-update'),
    path('create/', MenuCreateView.as_view(), name='menu-create'),
]
