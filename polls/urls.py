from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path("", login_required(views.IndexView.as_view(), login_url="/polls/login"), name="index"),
    path("login/", LoginView.as_view(template_name="polls/login.html", next_page="/polls")),
    path("logout/", LogoutView.as_view(next_page="/")),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/", login_required(views.DetailView.as_view(), login_url="/polls/login"), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:pk>/results/", login_required(views.ResultsView.as_view(), login_url="/polls/login"), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),

    path("guestbook/", views.guestbook_view, name="guestbook"),
    path("guestbook/add/", views.guestbook_add, name="guestbook"),
    path("guestbook/filter/", views.guestbook_filter, name="guestbook"),
]