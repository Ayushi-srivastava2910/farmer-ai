from django.db import models
from django.conf import settings

class Report(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disease = models.CharField(max_length=200)

    # ✅ ADD THESE FIELDS (IMPORTANT)
    description = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    causes = models.TextField(blank=True, null=True)
    solution = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    prevention = models.TextField(blank=True, null=True)
    soil = models.TextField(blank=True, null=True)

    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.disease