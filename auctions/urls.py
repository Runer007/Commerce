from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("auction/new", views.new, name="new"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("list/<str:user_username>", views.list, name="list"),
    path("auction/<int:auction_id>/stavca", views.stavca, name="stavca"),
    path("auction/<int:auction_id>/coment", views.coment, name="coment"),
    path("categorien", views.categorien, name = "categorien"),
    path("category/<str:category>", views.category, name = "category"),
    path("auction/<int:auction_id>/close", views.close, name = "close"),
]