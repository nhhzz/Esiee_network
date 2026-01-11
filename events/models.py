from django.conf import settings
from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_at", "title"]

    def __str__(self):
        return f"{self.title} ({self.start_at:%Y-%m-%d %H:%M})"

    @property
    def is_past(self):
        return self.start_at < timezone.now()
