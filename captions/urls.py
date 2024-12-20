# captions/urls.py
from django.urls import path
from .views import image_captioner_view, text_to_speech_view

urlpatterns = [
    path('', image_captioner_view, name='image_captioner'),
    path('text-to-speech/', text_to_speech_view, name='text_to_speech'),  # Add this line
]

