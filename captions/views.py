import os
import logging
from io import BytesIO
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from transformers import GitProcessor, GitForCausalLM
from PIL import Image
import base64
import requests
import spacy
from gtts import gTTS
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from django.core.files.base import ContentFile
from .models import CaptionData

# Initialize logging
logger = logging.getLogger(__name__)

# Load the spaCy model with caching
@lru_cache(maxsize=1)
def get_spacy_model():
    return spacy.load("en_core_web_sm")

# Load the pre-trained GIT model and processor with caching
@lru_cache(maxsize=1)
def get_git_model():
    processor = GitProcessor.from_pretrained("microsoft/git-base")
    model = GitForCausalLM.from_pretrained("microsoft/git-base")
    return processor, model

# Load Google API credentials from environment variables
API_KEY = ""# Replace with your Google API key
CX = "" # Replace with your Custom Search Engine ID
IMG_CNT = 8

# Temp directory for saving images
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)

def process_image(image_data):
    """Process image and generate caption, tags, and related image links."""
    processor, model = get_git_model()
    image = Image.open(BytesIO(image_data)).convert("RGB")
    caption = caption_image(image, processor, model)
    tags = generate_tags(caption)
    image_links = get_google_image_links(API_KEY, CX, caption, num_results=IMG_CNT)
    return caption, tags, image_links

def caption_image(image, processor, model):
    """Generate a caption for the uploaded image."""
    inputs = processor(images=image, return_tensors="pt", legacy=True)
    out = model.generate(**inputs, max_new_tokens=80, num_beams=5, no_repeat_ngram_size=2, length_penalty=1.5)
    return processor.decode(out[0], skip_special_tokens=True)

def generate_tags(caption):
    """Generate tags (nouns and adjectives) from the image caption."""
    try:
        doc = get_spacy_model()(caption)
        tags = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
        return list(set(tags))  # Remove duplicates
    except Exception as e:
        logger.error(f"Error generating tags: {e}")
        return []

def get_google_image_links(api_key, cx, query, num_results=IMG_CNT):
    """Fetch related image links using Google Custom Search API."""
    cache_key = f"google_images:{query}"
    images = cache.get(cache_key)
    if not images:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "searchType": "image",
            "num": num_results,
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            images = list({item["link"] for item in data.get("items", [])})
            cache.set(cache_key, images, timeout=3600)  # Cache for 1 hour
        except requests.RequestException as e:
            logger.error(f"Error fetching Google images: {e}")
            images = []
    return images

def image_captioner_view(request):
    """Handles the image upload, caption generation, tags, and related images."""
    context = {}

    if request.method == 'POST':
        if 'image' in request.FILES:
            # Handle uploaded image
            uploaded_image = request.FILES['image']
            image_data = uploaded_image.read()

            # Process image
            caption, tags, image_links = process_image(image_data)

            # Save data to CaptionData model
            caption_data = CaptionData(
                caption=caption,
                tags=tags,
                related_images=image_links
            )
            caption_data.image.save(uploaded_image.name, ContentFile(image_data))
            caption_data.save()

            # Convert image to base64 and store in session
            base64_string = base64.b64encode(image_data).decode('utf-8')
            request.session['image_data'] = base64_string

            # Update context
            context.update({
                'caption': caption,
                'tags': tags,
                'image_links': image_links
            })

        elif 'captured_image' in request.POST:
            # Handle captured image data
            try:
                captured_data = request.POST['captured_image']
                format, imgstr = captured_data.split(';base64,')
                image_data = base64.b64decode(imgstr)

                # Process captured image
                caption, tags, image_links = process_image(image_data)

                # Save data to CaptionData model
                caption_data = CaptionData(
                    caption=caption,
                    tags=tags,
                    related_images=image_links
                )
                caption_data.image.save("captured_image.jpg", ContentFile(image_data))
                caption_data.save()

                # Convert to base64
                base64_string = base64.b64encode(image_data).decode('utf-8')
                request.session['image_data'] = base64_string

                context.update({
                    'caption': caption,
                    'tags': tags,
                    'image_links': image_links
                })

            except Exception as e:
                logger.error(f"Error processing captured image: {e}")
                context['caption'] = "An error occurred with the captured image."

    # Retrieve image data from session
    if 'image_data' in request.session:
        context['image_data'] = request.session['image_data']

    return render(request, 'caption.html', context)


def text_to_speech_view(request):
    """Converts the caption text to speech."""
    caption = request.GET.get('caption', '')
    if caption:
        tts = gTTS(caption, lang='en')
        audio_path = os.path.join(TEMP_DIR, 'caption_audio.mp3')
        tts.save(audio_path)

        # Return audio file
        with open(audio_path, 'rb') as audio_file:
            response = HttpResponse(audio_file.read(), content_type="audio/mpeg")
            response['Content-Disposition'] = 'inline; filename="caption_audio.mp3"'
            return response
    return JsonResponse({'error': 'No caption provided'}, status=400)