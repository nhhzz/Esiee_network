from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from events.models import Event, Location


NO_END_EVENT_BUFFER_HOURS = 2


@login_required(login_url="users:login")
def index(request):
    now = timezone.now()
    no_end_cutoff = now - timedelta(hours=NO_END_EVENT_BUFFER_HOURS)

    events = (
        Event.objects.select_related("location", "created_by")
        .filter(Q(end_at__gte=now) | Q(end_at__isnull=True, start_at__gte=no_end_cutoff))
        .order_by("start_at", "title")
    )

    # Group by location to keep one clean marker per location.
    marker_map = {}
    for event in events:
        location = event.location
        location_id = location.id
        current_state = (
            "active"
            if event.start_at <= now and (event.end_at is None or event.end_at >= now)
            else "upcoming"
        )

        if location_id not in marker_map:
            x_percent = float(location.x_percent)
            y_percent = float(location.y_percent)

            if x_percent < 20:
                popup_side = "side-right"
            elif x_percent > 80:
                popup_side = "side-left"
            else:
                popup_side = "side-center"

            popup_vertical = "below" if y_percent < 20 else "above"

            marker_map[location_id] = {
                "location": location,
                "events": [],
                "state": current_state,
                "popup_side": popup_side,
                "popup_vertical": popup_vertical,
            }

        marker_map[location_id]["events"].append(event)
        # Active has priority for visual emphasis.
        if current_state == "active":
            marker_map[location_id]["state"] = "active"

    markers = list(marker_map.values())

    context = {
        "event_markers": markers,
        "locations": Location.objects.order_by("name"),
    }
    return render(request, "maps/index.html", context)
