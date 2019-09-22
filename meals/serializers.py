from rest_framework import serializers
from .models import Meal


class MealSerializer(serializers.ModelSerializer):
    '''
    Serializer for Meal
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Meal
        fields = ('id', 'name', 'tags', 'owner')
