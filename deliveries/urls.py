from django.urls import path
from .views import DeliverySelectionView, DeliverySelectionListView

urlpatterns = [
    path(
        'menu/<uuid:id>/',
        DeliverySelectionView.as_view(),
        name='delivery-selection'
    ),
    path(
        'commensals/list/',
        DeliverySelectionListView.as_view(),
        name='commensal-list'
    ),
]
