from typing import Any

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from ads.models import Advertisement, Category


# ----------------------------------------------------------------
# Validators
class IsPublishedValidator:
    def __init__(self, status: bool):
        self.status = status

    def __call__(self, value):
        print(self.status)
        if value == self.status:
            raise serializers.ValidationError('"is_published" cannot be True')


# ----------------------------------------------------------------
# Category serializers
class CatListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for ListView and RetrieveView
    """
    class Meta:
        model: Category = Category
        fields: list[str] = ['name']


class CatCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CreateView
    """
    id: serializers.IntegerField = serializers.IntegerField(required=False)

    class Meta:
        model: Category = Category
        fields: str = '__all__'

    def create(self, validated_data) -> Any:
        return Category.objects.create(**validated_data)


class CatChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView(update and partial update), DeleteView
    """
    class Meta:
        model: Category = Category
        fields: str = '__all__'


# ----------------------------------------------------------------
# Advertisement serializers
class AdListDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for ListView and RetrieveView
    """
    author: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field='username')
    category: serializers.SlugRelatedField = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model: Advertisement = Advertisement
        fields: list[str] = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']


class AdCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for CreateView
    """
    id: serializers.IntegerField = serializers.IntegerField(required=False)
    image: serializers.ImageField = serializers.ImageField(required=False)
    locations: SerializerMethodField = SerializerMethodField()
    is_published: serializers.BooleanField = serializers.BooleanField(validators=[IsPublishedValidator(True)])

    def get_locations(self, ad) -> list:
        """
        Method to make list of locations
        :param ad: object of advertisement
        :return: list of locations
        """
        return [loc.name for loc in ad.author.locations.all()]

    def is_valid(self, raise_exception=False) -> bool:
        """
        Method to check initial data
        :param raise_exception: False
        :return: True or False
        """
        if not self.initial_data.get('author'):
            self.initial_data['author'] = self.context['request'].user.id
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data) -> Any:
        """
        Method to create instance of advertisement
        :param validated_data: validated data taken from request.body
        :return:
        """
        return Advertisement.objects.create(**validated_data)

    class Meta:
        model: Advertisement = Advertisement
        fields: str = '__all__'


class AdChangeSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView(update and partial update), DeleteView
    """
    class Meta:
        model: Advertisement = Advertisement
        exclude: list[str] = ['id', 'image']

