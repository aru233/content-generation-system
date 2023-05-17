# For app.autodiscover_tasks() to work as described, the Celery tasks are defined in a separate tasks.py module inside of each app of the Django project.
from celery import shared_task
from time import sleep
import random
import time

from contentGenerator.models import RequestInfo
import requests
from django.urls import reverse

MAX_RETRIES = 5

@shared_task()
def generate_content_task(prompt, tag, request_id):

    if(tag == 'text'):
        generated_text = mock_text_worker(prompt, tag)

        try:
            request_info = RequestInfo.objects.filter(id=request_id).first()
            request_info.text = generated_text
            request_info.text_status = "Completed"
            request_info.save()
        except RequestInfo.DoesNotExist:
            print("Something is wrong with how the db was handled!!") # Can decide how to handle something like this; can throw a more relevant/useful exception etc.

    elif(tag == 'image'):
        generated_image_uri = mock_image_worker(prompt, tag)
        try:
            request_info = RequestInfo.objects.filter(id=request_id).first()
            request_info.image_uri = generated_image_uri
            request_info.image_status = "Completed"
            request_info.save()
        except RequestInfo.DoesNotExist:
            print("Something is wrong with how the db was handled!!") # Can decide how to handle something like this; can throw a more relevant/useful exception etc.

    elif(tag == 'instagram'):
        generated_text = mock_text_worker(prompt, tag)
        generated_image_uri = mock_image_worker(prompt, tag)
        try:
            request_info = RequestInfo.objects.filter(id=request_id).first()
            request_info.text = generated_text
            request_info.text_status = "Completed"
            request_info.image_uri = generated_image_uri
            request_info.image_status = "Completed"
            request_info.save()
        except RequestInfo.DoesNotExist:
            print("Something is wrong with how the db was handled!!") # Can decide how to handle something like this; can throw a more relevant/useful exception etc.


def mock_text_worker(prompt, tag):
    url = 'http://127.0.0.1:8000/worker/text'
    payload = {'prompt': prompt,'tag': tag}
    response = requests.post(url, data = payload)
    return response.json()['response']

def mock_image_worker(prompt, tag):
    url = 'http://127.0.0.1:8000/worker/image'
    payload = {'prompt': prompt,'tag': tag}
    response = requests.post(url, data = payload)
    return response.json()['response']