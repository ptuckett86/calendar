from django.db import transaction
from django.core.mail import send_mail
from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from ..core.models import AuthUser
from .models import CalendarEvent, Attendees
from .fields import CAL_CHOICES
from ..core.serializers import AuthUserCreateSerializer


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
            "notes",
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
            "notes",
        ]


class CalendarEventSerializer(FlexFieldsModelSerializer):
    attendees = serializers.PrimaryKeyRelatedField(
        queryset=AuthUser.objects.all(), many=True
    )
    add_user = AuthUserCreateSerializer(write_only=True, allow_null=True)

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
            "notes",
            "transparent",
            "add_user",
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
        add_user = validated_data.pop("add_user")
        check = AuthUser.objects.filter(email=add_user["email"])
        if not check:
            user = AuthUser.create_user(**add_user)
        else:
            user = AuthUser.objects.get(email=add_user["email"])
        validated_data["owner"] = user
        attendees = validated_data.pop("attendees")
        instance = super().create(validated_data)
        attendees.append(user)
        if attendees:
            for attendee in attendees:
                Attendees.objects.create(event=instance, attendee=attendee)
        send_mail(
            "New {} request".format(validated_data["event_type"]),
            "{} {} has added a new {} calendar event request".format(
                add_user["first_name"],
                add_user["last_name"],
                validated_data["event_type"],
            ),
            "utchwprogram@gmail.com",
            add_user["email"],
        )
        return instance

    def update(self, instance, validated_data):
        try:
            attendees = validated_data.pop("attendees")
        except:
            attendees = None
        if attendees:
            for attendee in attendees:
                Attendees.objects.create(event=instance, attendee=attendee)
        return super().update(instance, validated_data)
