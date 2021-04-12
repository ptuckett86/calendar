from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from .serializers import *
from .models import *
from ..core.pagination import FlexiblePagination
from .filters import EventFilter


class CalendarEventViewSet(viewsets.ModelViewSet):
    """
    Calendar events for a private user. Mostly used for managing events for interviews

    ###Expandable fields:
        * attendees

    """

    pagination_class = FlexiblePagination
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    filter_class = EventFilter
    ordering_fields = ("uuid", "dt_start", "dt_end", "location", "name", "event_type")
    search_fields = (
        "name",
        "description",
        "location",
        "summary",
        "owner__first_name",
        "owner__last_name",
    )

    def get_queryset(self):
        return CalendarEvent.objects.all()

    def get_serializer_class(self):
        if self.action == "change_status":
            return CalendarEventChangeSerializer
        return CalendarEventSerializer

    def get_permissions(self):
        return [AllowAny()]

    @action(methods=["get", "post"], detail=True)
    def change_status(self, request, pk=None):
        instance = self.get_object()
        user = request.user
        if request.method == "GET":
            serializer = CalendarEventChangeSerializer(
                instance, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            through = instance.attendee_event.all()
            if through:
                try:
                    event = through.get(attendee=user)
                except:
                    return Response(
                        "You can only change your own status",
                        status=status.HTTP_403_FORBIDDEN,
                    )
                event.status = serializer.validated_data["new_status"]
                event.save()
            return Response(
                CalendarEventChangeSerializer(
                    instance, context={"request": request}
                ).data,
                status=status.HTTP_200_OK,
            )
        return Response("serializer is not valid", status=status.HTTP_400_BAD_REQUEST)
