from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from django.views import View
# from contentGen import celery
import time
import random

from contentGenerator.tasks import generate_content_task
from contentGenerator.models import RequestInfo

def home(request):
    return HttpResponse("Hello! Welcome! Go to /content/ to request content generation. If you've already requested content, got to /content/view with the request-id")


@method_decorator(csrf_exempt, name='dispatch')
def contentRequest(request):
    prompt =  request.POST.get('prompt')
    tag = request.POST.get('tag')

    info = RequestInfo(prompt=prompt, tag=tag)
    info.save()

    request_id = info.id

    task_id = generate_content_task.delay(prompt, tag, request_id)
    # print("this is the TASK ID from Redis queue: ", task_id)

    json_response = {
        "message": "Hello! Your content is being generated. Use the request id to know status",
        "RequestId": request_id
    }

    # Return the response
    return JsonResponse(json_response)


@method_decorator(csrf_exempt, name='dispatch')
def contentResponse(request):
    request_id = request.POST.get('request-id')
    try:
        request_info = RequestInfo.objects.get(id=request_id)
        tag = request_info.tag
        if(tag == 'text'):
            if(request_info.text_status == "Completed"):
                json_response = {
                    "status": "Response is available now!",
                    "text": request_info.text
                }
            else:
                json_response = {
                    "status": "Response is not yet available. Try again!"
                }
        elif(tag == 'image'):
            if(request_info.image_status == "Completed"):
                json_response = {
                    "status": "Response is available now!",
                    "imageUri": request_info.image_uri
                }
            else:
                json_response = {
                    "status" : "Response is not yet available. Try again!"
                }
        elif(tag == 'instagram'):
            if(request_info.text_status == "Completed" and request_info.image_status == "Completed"):
                json_response = {
                    "status": "Response is available now!",
                    "text": request_info.text,
                    "imageUri": request_info.image_uri
                }
            else:
                json_response = {
                    "status": "Response is not yet available. Try again!"
                }
    except RequestInfo.DoesNotExist: # Bad request
        json_response = {
            "error": "Request-id does not exist", 
            "status_code": 400
        }       

    return JsonResponse(json_response)


@method_decorator(csrf_exempt, name='dispatch')
def mockTextWorker(request):
    prompt = request.POST.get('prompt')
    tag = request.POST.get('tag')
    time.sleep(random.randint(1, 10))
    sample_gen_text = "This text has been generated for you"
    return JsonResponse({"response": sample_gen_text})

@method_decorator(csrf_exempt, name='dispatch')
def mockImageWorker(request):
    prompt = request.POST.get('prompt')
    tag = request.POST.get('tag')
    time.sleep(random.randint(1, 10))
    sample_gen_img_uri = "s3://my-bucket/my-file.txt"
    return JsonResponse({"response": sample_gen_img_uri})
