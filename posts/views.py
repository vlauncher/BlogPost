from rest_framework import generics
from .models import Post
from .serializers import PostSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .services import fetch_github_raw_text

@csrf_exempt
def github_webhook(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            if payload.get('ref') == 'refs/heads/main':  # adjust if using a different branch
                update_all_posts_overview()
                return JsonResponse({'status': 'success'}, status=200)
            else:
                return JsonResponse({'status': 'ignored'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def update_all_posts_overview():
    posts = Post.objects.all()
    for post in posts:
        if post.post_url:
            post.overview = fetch_github_raw_text(post.post_url)
            post.save()
