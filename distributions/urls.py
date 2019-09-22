from django.urls import path
from .views import CreateDistributionView, UpdateDistributionView

urlpatterns = [
    path(
        'distribution/create/',
        CreateDistributionView.as_view(),
        name='distribution-create'
    ),
    path(
        'distribution/<int:pk>/update/',
        UpdateDistributionView.as_view(),
        name='distribution-update'
    ),
]
