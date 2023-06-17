from django.contrib import admin
from .models import Category, Item, Checklist, AssetCategory, AssetChecklist, AssetItem


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Checklist)
admin.site.register(AssetCategory)
admin.site.register(AssetChecklist)
admin.site.register(AssetItem)
