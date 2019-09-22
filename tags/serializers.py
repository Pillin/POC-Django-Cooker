from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for Menu
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'owner')
