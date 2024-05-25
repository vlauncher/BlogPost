from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("", views.PostList.as_view(), name="list"),
    path("<int:pk>/", views.PostDetail.as_view(), name="detail"),
    path('webhooks/github/', views.github_webhook, name='github-webhook'),
]