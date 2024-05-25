from rest_framework import generics

from .models import Post
from .serializers import PostSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


import hmac
import hashlib
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .services import fetch_github_raw_text

@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        signature = request.headers.get('X-Hub-Signature-256')
        if signature is None:
            return JsonResponse({'error': 'Missing signature'}, status=400)
        
        sha_name, signature = signature.split('=')
        if sha_name != 'sha256':
            return JsonResponse({'error': 'Invalid signature format'}, status=400)

        mac = hmac.new(
            settings.GITHUB_WEBHOOK_SECRET.encode('utf-8'),
            msg=request.body,
            digestmod=hashlib.sha256
        )

        if not hmac.compare_digest(mac.hexdigest(), signature):
            return JsonResponse({'error': 'Invalid signature'}, status=400)
        
        payload = json.loads(request.body)
        if payload.get('ref') == 'refs/heads/main':  # Change this to your branch if different
            for post in Post.objects.all():
                if post.post_url:
                    post.overview = fetch_github_raw_text(post.post_url)
                    post.save()
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
