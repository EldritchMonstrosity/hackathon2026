from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("posts/", views.post_list, name="post_list"),
    path("posts/<int:post_id>/", views.post_individual, name="post_individual"),

    path("analysis/<str:category>/", views.category_analysis, name="category_analysis"),

    path("posts/<int:post_id>/like/", views.like_post, name="like_post"),
    path("posts/<int:post_id>/dislike/", views.dislike_post, name="dislike_post"),
]