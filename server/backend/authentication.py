from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from backend.models import ProjectToken, AuthToken


class ProjectTokenAuthentication(TokenAuthentication):
    """this is a custom token authentication.
    The token is scoped to a specific project.

    Raises:
        exceptions.AuthenticationFailed: If token is invalid or expired.

    Returns:
        tuple: current user, used token 
    """
    model = ProjectToken
    keyword = "ProjectToken"

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.is_expired():
            token.delete()
            raise exceptions.AuthenticationFailed("Token expired")
        return user, token


class TokenExpiryAuthentication(TokenAuthentication):
    # deprecated! We switched to session auth which solves the problem of storing the token
    model = AuthToken

    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.is_expired():
            token.delete()
            raise exceptions.AuthenticationFailed("Token expired")
        return user, token
