from rest_framework import serializers
from .models import Plate


class PlateSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for Menu
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    meals = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Plate
        fields = ('id', 'name', 'meals', 'owner')
