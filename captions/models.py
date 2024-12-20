from django.db import models

class CaptionData(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploaded_images/', null=True, blank=True)
    caption = models.TextField()
    tags = models.TextField()  # Stores tags in JSON format
    related_images = models.TextField() # Stores related image links in JSON format

    def __str__(self):
        return f"Caption on {self.uploaded_at}"
