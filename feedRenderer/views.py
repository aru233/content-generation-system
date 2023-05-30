from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.core.exceptions import BadRequest

from .controller import initialiseFeed, getFeedList

def home(request):
    initialiseFeed()
    return HttpResponse("Hello! Welcome! Go to /feed/ to fetch feed items")

@method_decorator(csrf_exempt, name='dispatch')
def feedRequest(request):
    try:
        feedItems = getFeedList(request)
        print("Feed Items ", feedItems)
        return JsonResponse(feedItems, safe=False, status=status.HTTP_200_OK)
    except BadRequest:
        return JsonResponse({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)