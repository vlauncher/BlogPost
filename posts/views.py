from rest_framework import generics

from .models import Post
from .serializers import PostSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# views.py
import hmac
import hashlib
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from .services import fetch_github_raw_text

class GitHubWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        secret = settings.GITHUB_WEBHOOK_SECRET
        signature = request.headers.get('X-Hub-Signature-256')
        
        if not verify_github_signature(secret, signature, request.body):
            return Response({"detail": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        event = request.headers.get('X-GitHub-Event')
        if event == "push":
            update_all_post_overviews()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

def verify_github_signature(secret, signature, payload):
    hash_obj = hmac.new(secret.encode(), payload, hashlib.sha256)
    expected_signature = f"sha256={hash_obj.hexdigest()}"
    return hmac.compare_digest(expected_signature, signature)

def update_all_post_overviews():
    posts = Post.objects.all()
    for post in posts:
        if post.post_url:
            post.overview = fetch_github_raw_text(post.post_url)
            post.save()

