from django.conf.urls import url
from .views import snippet_upvote, bookmark_snippets

app_name = "actions"

urlpatterns = [
    url(r'^upvote/$', snippet_upvote, name="upvote"),
    url(r'^bookmark/$', bookmark_snippets, name="bookmark")
]