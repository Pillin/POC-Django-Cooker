from django.forms import ModelForm
from .models import Tag


class TagModelForm(ModelForm):

    class Meta:
        model = Tag
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        kwargs.pop('user', None)
        super(TagModelForm, self).__init__(*args, **kwargs)
