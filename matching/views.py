from pathlib import Path
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from matching.serializers import MatchingRequestSerializer
from matching.services.matching_orchestrator import MatchingConfig, MatchingOrchestrator
from matching.services.excel_processor import ExcelProcessor
from matching.services.data_validator import DataValidator
from matching.services.matching_service import MatchingService
from matching.services.result_writer import ResultWriter


class MatchingView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        excel_processor = ExcelProcessor()

        self.orchestrator = MatchingOrchestrator(
            excel_processor=ExcelProcessor(),
            data_validator=DataValidator(),
            matching_service=MatchingService(),
            result_writer=ResultWriter(excel_processor=excel_processor),
        )

    def post(self, request):
        serializer = MatchingRequestSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Konwersja danych na instancję MatchingConfig
                validated_data = serializer.validated_data

                # W tymczasowym rozwiązaniu definiujemy domyślne wartości dla nowych parametrów
                # Te wartości zostaną zastąpione rzeczywistymi danymi z serializera po jego aktualizacji
                config = MatchingConfig(
                    working_file_path=Path(validated_data["working_file"]["file_path"]),
                    reference_file_path=Path(
                        validated_data["reference_file"]["file_path"]
                    ),
                    matching_threshold=validated_data["matching_threshold"],
                    # Używamy wartości z zagnieżdżonej struktury
                    wf_description_column=validated_data["working_file"][
                        "description_column"
                    ],
                    wf_description_range=validated_data["working_file"][
                        "description_range"
                    ],
                    wf_price_target_column=validated_data["working_file"][
                        "price_target_column"
                    ],
                    ref_description_column=validated_data["reference_file"][
                        "description_column"
                    ],
                    ref_description_range=validated_data["reference_file"][
                        "description_range"
                    ],
                    ref_price_source_column=validated_data["reference_file"][
                        "price_source_column"
                    ],
                )

                # Wywołanie procesu dopasowania
                report_path = self.orchestrator.process_matching_request(config)
                return Response({"report_path": report_path}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
