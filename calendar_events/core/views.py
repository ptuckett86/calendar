from django.shortcuts import render
from calendar_events.core.models import *
from calendar_events.core.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework_jwt.views import JSONWebTokenAPIView


class AuthUserViewSet(viewsets.ModelViewSet):
    serializer_class = AuthUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_admin:
                return AuthUser.objects.all()
            else:
                return AuthUser.objects.filter(pk=user.pk)
        else:
            return AuthUser.objects.none()

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthUserSerializer

        return AuthUserCreateSerializer


class LoginObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password for users.

    Returns a JSON Web Token that can be used for authenticated requests.
    """

    serializer_class = LoginJSONWebTokenSerializer

    # def post(self, request):
    #     response = super().post(request)
    #     return response

    def post(self, request, *args, **kwargs):
        from calendar_events.core.jwt_overrides import jwt_response_payload_handler

        serializer = LoginJSONWebTokenSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user") or request.user
            token = serializer.validated_data.get("token")
        response_data = jwt_response_payload_handler(token, user, request)
        response = Response(response_data)
        if settings.JWT_AUTH["JWT_AUTH_COOKIE"]:
            expiration = datetime.utcnow() + settings.JWT_AUTH["JWT_EXPIRATION_DELTA"]
            response.set_cookie(
                settings.JWT_AUTH["JWT_AUTH_COOKIE"],
                token,
                expires=expiration,
                httponly=True,
            )
        user.save()
        return response


login_obtain_jwt_token = LoginObtainJSONWebToken.as_view()

