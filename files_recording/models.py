from django.db import models


class UploadedFile(models.Model):
    file = models.FileField()
    uploaded_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.file.name.split('/')[-1]} (ID: {self.id})"
    
