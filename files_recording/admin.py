from django.contrib import admin
from .models import UploadedFile

#@admin.register(UploadedFile)
#class UploadedFileAdmin(admin.ModelAdmin):
#    admin.site.register

admin.site.register(UploadedFile)
