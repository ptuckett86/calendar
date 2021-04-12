from django.contrib.auth import authenticate

from django.forms import EmailField

from rest_framework import serializers
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import get_username_field, PasswordField
from rest_flex_fields import FlexFieldsModelSerializer

from calendar_events.core.models import AuthUser

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class AuthUserSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = AuthUser
        fields = [
            "url",
            "uuid",
            "created_at",
            "updated_at",
            "last_login",
            "full_name",
            "first_name",
            "last_name",
            "middle_name",
            "suffix",
            "alias",
            "email",
            "email_confirmed",
        ]
        read_only_fields = ["last_login", "email_confirmed"]


class AuthUserCreateSerializer(AuthUserSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, allow_null=True
    )

    class Meta:
        model = AuthUser
        fields = AuthUserSerializer.Meta.fields + ["password"]
        read_only_fields = AuthUserSerializer.Meta.read_only_fields

    def create(self, validated_data):
        user = AuthUser.create_user(**validated_data)
        return user


class LoginJSONWebTokenSerializer(serializers.Serializer):
    """
    Serializer class used to validate a username and password for user.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    email = serializers.EmailField(required=False, allow_null=True)
    password = serializers.CharField(
        style={"input_type": "password"}, required=False, allow_null=True
    )

    def validate(self, attrs):
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError("Must provide an email")
        password = attrs.get("password")
        if not password:
            raise serializers.ValidationError("Must provide an password")
        credentials = {"email": email, "password": password}
        if credentials:
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "Credentials could not be verified"
                    )

                payload = jwt_payload_handler(user)
                return {"token": jwt_encode_handler(payload), "user": user}
            else:
                raise serializers.ValidationError("Credentials could not be verified")
        else:
            raise serializers.ValidationError("Credentials could not be verified")
