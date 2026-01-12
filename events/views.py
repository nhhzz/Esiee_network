
"""""
from django.shortcuts import render

def index(request):
    return render(request,'events/index.html')
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import EventForm
from .models import Event, LOCATION_CHOICES

"""""
@login_required
def events_list(request):
    now = timezone.now()
    upcoming_events = Event.objects.filter(start_at__gte=now).order_by("start_at")
    past_events = Event.objects.filter(start_at__lt=now).order_by("-start_at")[:10]
    return render(
        request,
        "events/events_list.html",
        {"upcoming_events": upcoming_events, "past_events": past_events},
    )
"""
@login_required
def events_list(request):
    location_code = request.GET.get("location")

    events = Event.objects.all().order_by("start_at", "title")

    filtered_location_label = None
    if location_code:
        events = events.filter(location=location_code)
        # On récupère le label lisible à partir des choices
        choices_dict = dict(LOCATION_CHOICES)
        filtered_location_label = choices_dict.get(location_code)

    context = {
        "events": events,
        "filtered_location": filtered_location_label,
        "raw_location": location_code,
    }
    return render(request, "events/events_list.html", context)

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
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
    event = get_object_or_404(Event, pk=pk)

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
