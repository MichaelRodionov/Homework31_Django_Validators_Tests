from typing import Any

from rest_framework import serializers

from ads.models import Advertisement
from ads.serializers import AdListDetailSerializer
from selections.models import Selection


# ----------------------------------------------------------------
# Selection serializers
class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model: Selection = Selection
        fields: list[str] = ['id', 'name']


class SelectionDetailSerializer(serializers.ModelSerializer):
    advertisements: AdListDetailSerializer = AdListDetailSerializer(many=True, read_only=True)

    class Meta:
        model: Selection = Selection
        fields: str = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    advertisements: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement.objects.all(),
        slug_field='id'
    )

    def is_valid(self, raise_exception=False) -> bool:
        """
        Method to check initial data
        :param raise_exception: False
        :return: True or False
        """
        self.initial_data['owner'] = self.context['request'].user.id
        self._advertisements: Any = self.initial_data.pop('advertisements', [])

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data) -> Any:
        """
        Method to create instance
        :param validated_data: validated data taken from request.body
        :return: user instance
        """
        selection: Any = super().create(validated_data)
        if self._advertisements:
            for ad in self._advertisements:
                selection.advertisements.add(ad)
        selection.save()

        return selection

    class Meta:
        model: Selection = Selection
        fields: str = '__all__'


class SelectionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for UpdateView(update and partial update)
    """
    advertisements: serializers.SlugRelatedField = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Advertisement.objects.all(),
        slug_field='id'
    )

    def is_valid(self, raise_exception=False) -> bool:
        """
        Method to validate data
        :param raise_exception: False
        :return: bool
        """
        self.initial_data['owner'] = self.context['request'].user.id
        self._advertisements: Any = self.initial_data.pop('advertisements', [])
        return super().is_valid(raise_exception=raise_exception)

    def save(self) -> Any:
        """
        Method to save changes to selection's instance
        :return: selection instance
        """
        selection: Any = super().save()
        selection.advertisements.set(self._advertisements)
        selection.save()
        return selection

    class Meta:
        model: Selection = Selection
        fields: str = '__all__'


class SelectionDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer for DeleteView
    """
    model: Selection = Selection
    fields: list[str] = ['id']
