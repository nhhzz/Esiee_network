from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventForm
from .models import Event, Location


NO_END_EVENT_BUFFER_HOURS = 2


def _visible_events_queryset(queryset):
    """
    Keep upcoming and ongoing events. Ended events are excluded.
    If end_at is missing, keep the event visible up to 2h after start.
    """
    now = timezone.now()
    no_end_cutoff = now - timedelta(hours=NO_END_EVENT_BUFFER_HOURS)
    return queryset.filter(
        Q(end_at__gte=now) | Q(end_at__isnull=True, start_at__gte=no_end_cutoff)
    )


@login_required
def events_list(request):
    filter_follow = request.GET.get("filter")
    location_slug = request.GET.get("location")

    events = Event.objects.select_related("location", "created_by")
    events = _visible_events_queryset(events)

    if filter_follow == "following":
        followed_users = request.user.following.values_list("followed_id", flat=True)
        events = events.filter(created_by__in=followed_users)

    filtered_location_label = None
    if location_slug:
        events = events.filter(location__slug=location_slug)
        filtered_location_label = (
            Location.objects.filter(slug=location_slug)
            .values_list("name", flat=True)
            .first()
        )

    events = events.order_by("start_at", "title")

    context = {
        "events": events,
        "filtered_location": filtered_location_label,
        "raw_location": location_slug,
        "filter_follow": filter_follow,
    }
    return render(request, "events/events_list.html", context)


@login_required
def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related("location", "created_by"),
        pk=pk,
    )
    return render(request, "events/event_detail.html", {"event": event})


@login_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect("events:detail", pk=event.pk)
    else:
        form = EventForm()

    return render(request, "events/event_form.html", {"form": form, "mode": "create"})


@login_required
def event_update(request, pk):
    event = get_object_or_404(Event.objects.select_related("location"), pk=pk)

    if event.created_by != request.user:
        return redirect("events:detail", pk=event.pk)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("events:detail", pk=event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_form.html", {"form": form, "mode": "update"})


@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.created_by != request.user:
        return redirect("events:detail", pk=event.pk)

    if request.method == "POST":
        event.delete()
        return redirect("events:list")

    return render(request, "events/event_confirm_delete.html", {"event": event})
