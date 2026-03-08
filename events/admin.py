from django.contrib import admin
from .models import Event, Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "x_percent", "y_percent")
    search_fields = ("name", "slug")
    ordering = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_at", "end_at", "location", "created_by")
    list_filter = ("start_at", "location", "created_by")
    search_fields = ("title", "description", "location__name")
