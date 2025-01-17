from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.vote, name="vote"),
    path("candidatos", views.candidatos, name="candidatos"),
    path("vote_success", views.vote_success, name="vote_success"),
    path("already_voted", views.already_voted, name="already_voted"),
    path("election_over", views.election_over, name="election_over"),
    path("before_election", views.before_election, name="before_election"),
    
    # path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/login/", views.RunLoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
]
