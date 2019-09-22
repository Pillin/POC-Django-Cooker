from django.contrib.auth import logout

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class LoginFormView(LoginView):
    """
    Provides users the ability to login
    """
    form_class = AuthenticationForm
    template_name = "crud/create.html"
    success_url = reverse_lazy('home')
