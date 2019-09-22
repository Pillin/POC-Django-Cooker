from django.urls import path
from .views import MealListView, MealUpdateView, MealCreateView, MealDeleteView

urlpatterns = [
    path('list/', MealListView.as_view(), name='meal-list'),
    path('<int:pk>/delete/', MealDeleteView.as_view(), name='meal-delete'),
    path('<int:pk>/update/', MealUpdateView.as_view(), name='meal-update'),
    path('create/', MealCreateView.as_view(), name='meal-create'),
]
