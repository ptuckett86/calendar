from django.db import models
from calendar_events.core.models import MetaModel

from .fields import TRANSPARENCY, CAL_EVENT_CHOICES, CAL_TENTATIVE, CAL_CHOICES


class CalendarEvent(MetaModel):
    """
    Keep track of Calendar Events
    """

    owner = models.ForeignKey("core.AuthUser", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(
        "core.AuthUser", related_name="events", through="events.Attendees"
    )
    name = models.CharField(max_length=60)
    event_type = models.CharField(max_length=30, choices=CAL_EVENT_CHOICES)
    dt_start = models.DateTimeField(
        help_text="Will store as UTC, set TZ on front end and process to UTC."
    )
    dt_end = models.DateTimeField()
    description = models.CharField(max_length=250, null=True)
    location = models.CharField(max_length=100, null=True)
    sequence = models.PositiveIntegerField(default=0)
    reminder = models.PositiveIntegerField(default=0)
    reminder_sent = models.BooleanField(default=False)
    notes = models.CharField(max_length=250, null=True)
    transparent = models.BooleanField(choices=TRANSPARENCY, default=False)

    class Meta:
        ordering = ["name"]


class Attendees(MetaModel):
    attendee = models.ForeignKey(
        "core.AuthUser", related_name="attendee_event", on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        CalendarEvent, related_name="attendee_event", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=60, choices=CAL_CHOICES, default=CAL_TENTATIVE, blank=True
    )
