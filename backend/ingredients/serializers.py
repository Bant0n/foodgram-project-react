from rest_framework import serializers

from .models import Ingredients, IngredientsAmount


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit",)


class AmountIngredients(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
    )

    class Meta:
        model = IngredientsAmount
        fields = ("id", "amount")

    def validate_amount(self, value):
        print(value)
        if value <= 0:
            raise serializers.ValidationError(
                "Количество должно быть больше нуля"
            )
        return value


class ReadIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
    )
    name = serializers.CharField(source="ingredient.name", required=False)
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit", required=False
    )

    class Meta:
        model = IngredientsAmount
        fields = ("id", "name", "measurement_unit", "amount")
