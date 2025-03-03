from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .models import UploadedFile
from .serializers import UploadedFileSerializer
import os


class UploadExcelFileView(APIView):
    """
    Klasa obsługująca przesyłanie plików Excel do aplikacji.
    """

    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        summary="Przesłanie pliku Excel",
        description="Endpoint umożliwiający przesyłanie pliku Excel "
        "Walidajcja rozrzerzemoa .xls lub .xlsx.",
        responses={
            201: {"message": "Plik został przesłany."},
            400: {"message": "Nieprawidłowy plik."},
        },
    )
    def post(self, request, category):
        """
        Obsługuje przesyłanie plików Excel.
        """
        file_category = ("uploaded", "reference", "working")
        if category not in file_category:
            return Response(
                {
                    "error": "Nieprawidlowa kategoria zapisu. Dozwolone: 'uploaded', 'reference', 'working'"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_serializer = UploadedFileSerializer(data=request.data)

        if file_serializer.is_valid():
            uploaded_file = request.FILES["file"]

            if not uploaded_file.name.endswith((".xls", ".xlsx")):
                return Response(
                    {"error": "Tylko pliki Excel są obsługiwane!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            directory = f"uploaded_files/{category}_files"
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, uploaded_file.name)
            with open(file_path, "wb") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            instance = UploadedFile(file=file_path)
            instance.save()

            return Response(
                {
                    "message": f"Plik Excel został przesłany i zapisany w katalogu '{directory}'",
                    "data": file_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(file_serializer.errors, status=HTTP_400_BAD_REQUEST)
