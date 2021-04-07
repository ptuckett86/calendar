def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "uuid": user.pk,
    }


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret
