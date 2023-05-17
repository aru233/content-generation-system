from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('content/', views.contentRequest),
    path('content/view/', views.contentResponse),
    path('worker/text', views.mockTextWorker),
    path('worker/image', views.mockImageWorker)
]