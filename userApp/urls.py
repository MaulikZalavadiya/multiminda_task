from django.urls import include, path

from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register("auth", UserAuthViewSet, basename="custom-auth")
router.register("user", UserViewSet, basename="user")

app_name = "userApp"

urlpatterns = [
    path("", include(router.urls)),
]
