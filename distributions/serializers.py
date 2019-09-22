from rest_framework import serializers
from .models import Distribution


class DistributionSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for Distribution
    '''
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Distribution
        fields = ('id', 'name', 'link_id', 'is_active', 'owner')
