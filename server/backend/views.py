from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from backend.serializers.user import UserMeSerializer
from .throttle import AuthFlowThrottle


# TODO: move to serializers
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginResponseSerializer(serializers.Serializer):
    user = UserMeSerializer(read_only=True)
    csrf_token = serializers.CharField()


class LogoutSerializer(serializers.Serializer):
    # pylint: disable=abstract-method
    """empty serializer. required to make spectacular happy
    """


class LoginView(APIView):
    """this view handles the login process
    similar to:
    https://github.com/django/django/blob/4.1/django/contrib/auth/views.py#L67
    """
    throttle_classes = [AuthFlowThrottle]
    authentication_classes = []

    @extend_schema(request=LoginSerializer, responses=LoginResponseSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        """handle the login process.
        use a method similar to the original django auth views but using JSON.

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password"),
            )
            if user:
                login(request, user)
                return Response(
                    LoginResponseSerializer(
                        {"user": user, "csrf_token": request.META["CSRF_COOKIE"]}
                    ).data
                )
            return Response(
                "Invalid username and/or password!", status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """just as the same implies: this view is used to destroy the session."""

    authentication_classes = [SessionAuthentication]

    @extend_schema(request=LogoutSerializer, responses=LogoutSerializer)
    @method_decorator(csrf_protect)
    def post(self, request, **kwargs):
        """Handle post request and perform logout.
        Use POST to prevent CSRF.

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class AuthCheckView(APIView):
    """Check if the user is logged in.
    This view provides a way for the frontend to get the CSRF_COOKIE.

    original code linked below. just add our user information here for the top bar.
    https://medium.com/swlh/django-rest-framework-and-spa-session-authentication-with-docker-and-nginx-aa64871f29cd
    """

    authentication_classes = [SessionAuthentication]

    @extend_schema(request={}, responses=LoginResponseSerializer)
    def get(self, request, **kwargs):
        if not request.user.is_authenticated:
            user = None
        else:
            user = request.user
        # no csrf_token set yet
        if not request.META.get('CSRF_COOKIE'):
            get_token(request)
        return Response(
            LoginResponseSerializer(
                {"user": user, "csrf_token": request.META.get("CSRF_COOKIE", None)}
            ).data
        )
