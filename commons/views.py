from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, UpdateView, SingleObjectMixin
from django.views.generic.list import ListView


@method_decorator(login_required, name='dispatch')
class HomeTemplateView(TemplateView):
    template_name = "home.html"

    def get_context_data(self):
        kwargs = super(HomeTemplateView, self).get_context_data()
        return kwargs


class ThanksTemplateView(TemplateView):
    template_name = "deliveries/thanks.html"


class SadnessTemplateView(TemplateView):
    template_name = "deliveries/sadness.html"


class CommonMixinListView(ListView):
    template = 'crud/list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = self.create_url if hasattr(self, 'create_url') else ''
        context['update_url'] = self.update_url if hasattr(self, 'update_url') else ''
        context['delete_url'] = self.delete_url if hasattr(self, 'delete_url') else ''
        return context

    def get_template_names(self):
        return self.template

    def get_queryset(self):
        queryset = super(CommonMixinListView, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class CommonMixinCreateView(CreateView):
    template_name = 'crud/create.html'

    def get_success_url(self):
        return self.success_url

    def get_context_data(self, **kwargs):
        kwargs = super(CommonMixinCreateView, self).get_context_data(**kwargs)
        kwargs['titlename'] = self.titlename
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(CommonMixinCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())


class CommonMixinUpdateView(UpdateView):
    template_name = 'crud/create.html'

    def get_queryset(self):
        queryset = super(CommonMixinUpdateView, self).get_queryset()
        return queryset.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs)
        if not self.get_object().owner == self.request.user:
            raise Http404
        return context

    def get_context_data(self, **kwargs):
        kwargs = super(CommonMixinUpdateView, self).get_context_data(**kwargs)
        kwargs['titlename'] = self.titlename
        return kwargs

    def get_form_kwargs(self):
        kwargs = super(CommonMixinUpdateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())


class CommonMixinDeleteView(RedirectView, SingleObjectMixin):
    def get(self, request, *args, **kwargs):
        context = super().get(request, *args, **kwargs)
        if not self.get_object().owner == self.request.user:
            raise Http404
        self.get_object().delete()
        return context
