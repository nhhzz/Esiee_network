from django.conf import settings
from django.db import models
from django.utils import timezone


# Lieux possibles (points de la carte)
LOCATION_CHOICES = [
    ("DEJEUNERS", "Déjeuners"),
    ("RESTAURANT", "Restaurant"),
    ("CAFETERIA", "Cafétéria"),
    ("GYMNASE", "Gymnase"),
    ("AMPHI_DASSAULT", "Amphithéâtre M. Dassault"),
    ("EPI5", "Epi 5"),
    ("AMPHI", "Amphi"),
    ("ACCUEIL", "Accueil"),
    ("EPI2", "Epi 2"),
    ("BIBLIOTHEQUE", "Bibliothèque"),
    ("POSTE_NORD", "Poste Nord"),
    ("PORTE_NORD", "Porte Nord"),
    ("ROND_POINT", "Rond-Point"),
    ("PORTE_PRINCIPALE", "Porte principale"),
]


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # Champ lieu -> dropdown avec les choix ci-dessus
    location = models.CharField(
        "Lieu",
        max_length=50,
        choices=LOCATION_CHOICES,
    )

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
