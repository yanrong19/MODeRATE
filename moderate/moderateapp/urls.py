from django.urls import path
from . import views

urlpatterns = [
path("", views.home, name = "home"),
path("home/", views.home, name = "home"),
path("find/", views.find, name="find"),
path("find/comments", views.moderate, name="find"),
path("view/", views.view, name="view"),
path("view/rating/", views.rating, name="rating"),
path("view/searched/", views.searched, name="searched"),
path("problem/", views.problem, name="problem"),
path("problem/thankyou", views.thankyou, name="thankyou"),
path("find/error", views.find, name="error"),
]

##admin 
# Username: zhiqi
# Password: kriszhiqiNN