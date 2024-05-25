from rest_framework import generics

from .models import Post
from .serializers import PostSerializer



class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


from django.http import HttpResponse
from .services import fetch_github_raw_text

def github_webhook(request):
    if request.method == 'POST':
        payload = request.body
        event = request.headers.get('X-GitHub-Event')
        if event == 'push':
            # Update all posts overview with the fetch_github service
            for post in Post.objects.all():
                raw_text = fetch_github_raw_text(post.github_url)
                if raw_text:
                    post.overview = raw_text[:200]  # Update the overview with the first 200 characters of the raw text
                    post.save()
        return HttpResponse('Webhook received')
    return HttpResponse('Invalid request')
