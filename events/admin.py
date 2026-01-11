from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_at", "end_at", "location", "created_by")
    list_filter = ("start_at", "created_by")
    search_fields = ("title", "location", "description")
