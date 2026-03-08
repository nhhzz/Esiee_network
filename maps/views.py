from datetime import timedelta

from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from events.models import Event, Location


NO_END_EVENT_BUFFER_HOURS = 2


def index(request):
    now = timezone.now()
    no_end_cutoff = now - timedelta(hours=NO_END_EVENT_BUFFER_HOURS)

    events = (
        Event.objects.select_related("location", "created_by")
        .filter(Q(end_at__gte=now) | Q(end_at__isnull=True, start_at__gte=no_end_cutoff))
        .order_by("start_at", "title")
    )

    markers = []
    for event in events:
        x_percent = float(event.location.x_percent)
        y_percent = float(event.location.y_percent)

        if event.start_at <= now and (event.end_at is None or event.end_at >= now):
            state = "active"
        else:
            state = "upcoming"

        if x_percent < 20:
            popup_side = "side-right"
        elif x_percent > 80:
            popup_side = "side-left"
        else:
            popup_side = "side-center"

        popup_vertical = "below" if y_percent < 20 else "above"

        markers.append(
            {
                "event": event,
                "location": event.location,
                "state": state,
                "popup_side": popup_side,
                "popup_vertical": popup_vertical,
            }
        )

    context = {
        "event_markers": markers,
        "locations": Location.objects.order_by("name"),
    }
    return render(request, "maps/index.html", context)
