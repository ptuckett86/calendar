from django.db import transaction

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from ..core.models import AuthUser
from .models import CalendarEvent, Attendees
from .fields import CAL_CHOICES


class AttendeeReadSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Attendees
        fields = ["attendee", "status"]

    expandable_fields = {
        "attendee": ("calendar_events.core.AuthUserSerializer", {"source": "attendee"})
    }


class CalendarEventChangeSerializer(FlexFieldsModelSerializer):
    new_status = serializers.ChoiceField(choices=CAL_CHOICES, write_only=True)
    attendees = serializers.SerializerMethodField()

    def get_attendees(self, instance):
        if instance.attendee_event:
            return AttendeeReadSerializer(
                instance.attendee_event.all(), many=True, context=self.context
            ).data

    class Meta:
        model = CalendarEvent
        fields = [
            "url",
            "uuid",
            "attendees",
            "name",
            "event_type",
            "dt_start",
            "dt_end",
            "description",
            "location",
            "summary",
            "new_status",
        ]
        read_only_fields = [
            "url",
            "uuid",
            "attendees",
            "name",
            "event_type",
            "dt_start",
            "dt_end",
            "description",
            "location",
            "summary",
        ]


class CalendarEventSerializer(FlexFieldsModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(
        queryset=AuthUser.objects.all(), many=True
    )

    class Meta:
        model = CalendarEvent
        fields = [
            "url",
            "uuid",
            "owner",
            "attendees",
            "name",
            "event_type",
            "dt_start",
            "dt_end",
            "description",
            "location",
            "summary",
            "transparent",
        ]
        read_only_fields = ["owner"]

    expandable_fields = {
        "owner": ("calendar_events.core.AuthUserSerializer", {"source": "owner"}),
        "attendees": (
            "calendar_events.core.AuthUserSerializer",
            {"source": "attendees", "many": True},
        ),
    }

    def validate(self, data):
        if {"dt_start", "dt_end"} <= set(data):
            if data["dt_start"] > data["dt_end"]:
                raise serializers.ValidationError(
                    {"dt_end": "End date cannot be greater than start date"}
                )
        return super().validate(data)

    @transaction.atomic()
    def create(self, validated_data):
        owner = self.context["request"].user
        validated_data["owner"] = owner
        attendees = validated_data.pop("attendees")
        instance = super().create(validated_data)
        if attendees:
            # sets the many to many fields, because we use safe delete
            instance.attendees.set(attendees)
        return instance

    def update(self, instance, validated_data):
        try:
            attendees = validated_data.pop("attendees")
        except:
            attendees = None
        if attendees:
            # sets the many to many fields, because we use safe delete
            instance.attendees.set(attendees)
        return super().update(instance, validated_data)
