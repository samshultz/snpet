from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from snippets.models import Snippet
from common.decorators import ajax_required


@ajax_required
@login_required
@require_POST
def snippet_upvote(request):
    snippet_id = request.POST.get("id")
    action = request.POST.get("action")

    if snippet_id and action:
        try:
            snippet = Snippet.objects.get(id=snippet_id)
            # checks if the current user has already upvoted the snippet
            # to prevent them from carrying out multiple upvote/downvote
            upvoted = request.user in snippet.upvotes.all()
            downvoted = request.user in snippet.downvotes.all()

            if action == "upvote":
                if not upvoted:
                    snippet.downvotes.remove(request.user)
                    snippet.upvotes.add(request.user)
            else:
                snippet.upvotes.remove(request.user)
                snippet.downvotes.add(request.user)
            return JsonResponse({'status': 'ok', 'upvoted': upvoted,
                                 'downvoted': downvoted})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@ajax_required
@login_required
@require_POST
def bookmark_snippets(request):
    snippet_id = request.POST.get("id")
    action = request.POST.get("action")

    if snippet_id and action:
        try:
            snippet = Snippet.objects.get(id=snippet_id)
            if action == "bookmark":
                if request.user not in snippet.bookmarks.all():
                    snippet.bookmarks.add(request.user)

            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})
