import django_filters
from .models import CalendarEvent
from .fields import CAL_EVENT_CHOICES


class EventFilter(django_filters.FilterSet):
    """Filtering for Calendar Events"""

    event_type = django_filters.ChoiceFilter(choices=CAL_EVENT_CHOICES)
    transparent = django_filters.BooleanFilter(
        widget=django_filters.widgets.BooleanWidget()
    )

    class Meta:
        model = CalendarEvent
        fields = {
            "name": ["icontains"],
            "attendees": ["exact"],
            "attendee_event__status": ["exact"],
            "owner": ["exact"],
            "dt_start": ["gte"],
            "dt_end": ["lte"],
            "description": ["icontains"],
            "location": ["icontains"],
            "summary": ["icontains"],
        }
