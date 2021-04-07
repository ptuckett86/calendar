from rest_framework.routers import DefaultRouter
from calendar_events.core.views import *
from calendar_events.events.views import *

router = DefaultRouter()

router.register("users", AuthUserViewSet, basename="authuser")
router.register("events", CalendarEventViewSet, basename="calendarevent")
