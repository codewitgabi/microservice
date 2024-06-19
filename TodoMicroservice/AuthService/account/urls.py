from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.RegisterUserView.as_view()),
    path("login/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("user/<int:user_id>", views.UserDetail.as_view()),
]
