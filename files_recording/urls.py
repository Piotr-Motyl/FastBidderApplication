from django.urls import path
from .views import UploadExcelFileView

urlpatterns  = [
    path('upload/<str:category>/', UploadExcelFileView.as_view(), 
         name='upload_excel_file'),
]
