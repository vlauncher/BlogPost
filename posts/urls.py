from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostList.as_view(), name="list"),
    path("<int:pk>/", views.PostDetail.as_view(), name="detail"),
    path('github-webhook/', views.GitHubWebhookView.as_view(), name='github-webhook'),
]