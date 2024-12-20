from django.contrib import admin
from .models import CaptionData

@admin.register(CaptionData)
class CaptionDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'caption')
    search_fields = ('caption',)
    list_filter = ('uploaded_at',)
