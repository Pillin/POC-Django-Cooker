from django.conf.urls import include
from django.urls import path
from django.views.generic.base import RedirectView
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from commons.views import HomeTemplateView, SadnessTemplateView, ThanksTemplateView
from users.views import LogoutView, LoginFormView
from .api_urls import Router


urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('api/', include(Router.urls), name='api'),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-auth/', include('rest_framework.urls')),
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('sadness/', SadnessTemplateView.as_view(), name='sadness'),
    path('thanks/', ThanksTemplateView.as_view(), name='thanks'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tags/', include('tags.urls')),
    path('meals/', include('meals.urls')),
    path('plates/', include('plates.urls')),
    path('menus/', include('menus.urls')),
    path('distributions/', include('distributions.urls')),
    path('', include('deliveries.urls')),
]
