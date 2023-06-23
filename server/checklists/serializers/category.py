from rest_framework import serializers
from checklists.models import Category, AssetCategory
from .item import ItemSerializer, AssetItemSerializer


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True, source="item_set")

    class Meta:
        model = Category
        fields = ["pk", "name", "summary", "category_id", "items"]


class AssetCategorySerializer(CategorySerializer):
    items = AssetItemSerializer(many=True, read_only=True, source="assetitem_set")

    class Meta:
        model = AssetCategory
        fields = CategorySerializer.Meta.fields
