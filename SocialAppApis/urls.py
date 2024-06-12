from django.urls import path, include
from .views import UserLogin, UserLogout, UserRegister, UserViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register('users',UserViewSet)

urlpatterns = [
    path("register/", UserRegister.as_view()),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
    path('',include(router.urls))
]
