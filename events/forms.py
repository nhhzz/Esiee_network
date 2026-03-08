from django import forms
from django.db.models import Case, IntegerField, Value, When

from .models import Event


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_order = [
            "epi-1",
            "epi-2",
            "epi-3",
            "epi-4",
            "epi-5",
            "epi-6",
            "amphi-1",
            "amphi-2",
            "amphi-3",
            "amphi-4",
            "accueil",
            "bibliotheque",
            "restaurant-crous",
            "cafeteria",
            "gymnase",
        ]
        ordering_case = Case(
            *[
                When(slug=slug, then=Value(index))
                for index, slug in enumerate(location_order)
            ],
            default=Value(999),
            output_field=IntegerField(),
        )
        self.fields["location"].queryset = (
            self.fields["location"].queryset.annotate(_sort_key=ordering_case).order_by("_sort_key", "name")
        )

    class Meta:
        model = Event
        fields = ["title", "description", "location", "start_at", "end_at"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "location": forms.Select(attrs={"class": "form-select"}),
            # Si tu utilises MDB/Bootstrap : datetime-local est pratique
            "start_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "end_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

    def clean(self):
        cleaned = super().clean()
        start_at = cleaned.get("start_at")
        end_at = cleaned.get("end_at")
        if start_at and end_at and end_at < start_at:
            self.add_error("end_at", "La date de fin doit être après la date de début.")
        return cleaned
