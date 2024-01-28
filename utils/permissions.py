from django.conf import settings
from rest_framework.exceptions import ParseError
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsReadAction(BasePermission):
    def has_access(self, request, view, instance=None):
        return request.method in SAFE_METHODS


IsEditAction = ~IsReadAction


class IsAPIKEYAuthenticated(BasePermission):
    """
    This permission class is used for check api key and identify the requests.
    """

    def has_permission(self, request, view):
        # API_KEY should be in request headers to authenticate requests
        api_key_secret = request.META.get("HTTP_API_KEY")
        try:
            api_key_secret = bytes(api_key_secret, 'utf-8')
        except TypeError:
            raise ParseError("API-KEY is required.")
        if api_key_secret == settings.API_KEY_SECRET:
            return True
        else:
            raise ParseError("Invalid API-KEY.")
