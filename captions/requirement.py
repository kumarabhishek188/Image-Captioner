# Django-related dependencies
django>=4.0,<5.0
# Logging (Standard library, no external package needed)

# Transformers library for GitProcessor and GitForCausalLM
transformers>=4.30.0,<5.0

# Image processing
Pillow>=9.0.0,<10.0

# Natural language processing
spacy>=3.0.0,<4.0

# Google Text-to-Speech
gTTS>=2.0.0,<3.0

# Requests for API calls
requests>=2.28.0,<3.0

# Cache utilities (Standard library cache, but add if Django-specific caching backend is used)
django-redis-cache>=3.0.0,<4.0  # If you're using Redis as a cache backend

# Thread-safe utilities
concurrent-futures; python_version<"3.9"

# For handling files
filelock>=3.0.0,<4.0
#pip install -r requirement.py
