

from rest_framework import serializers

from .models import Menu


class MenuSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Serializer for Menu
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    plates = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Menu
        fields = ('id', 'name', 'plates', 'owner')
