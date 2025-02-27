import re
from rest_framework import serializers

from matching.models import MatchingSession, MatchingResult


class CellRangeSerializer(serializers.Serializer):
    """Serializer dla zakresu komórek"""

    start = serializers.CharField(
        max_length=10, help_text="Początkowa komórka zakresu (np. '2')"
    )
    end = serializers.CharField(
        max_length=10, help_text="Końcowa komórka zakresu (np. '10')"
    )

    def validate(self, data):
        # Walidacja, czy start i end to liczby
        for field_name in ["start", "end"]:
            if not data[field_name].isdigit():
                raise serializers.ValidationError(
                    f"Nieprawidłowy numer wiersza dla {field_name}. Musi być liczbą."
                )

        # Sprawdzenie czy start jest mniejszy niż end
        if int(data["start"]) >= int(data["end"]):
            raise serializers.ValidationError(
                "Wiersz początkowy musi być przed końcowym"
            )

        return data


class FileConfigSerializer(serializers.Serializer):
    """Serializer dla konfiguracji pliku Excel"""

    file_path = serializers.CharField(
        max_length=255, help_text="Ścieżka do pliku Excel"
    )
    description_column = serializers.CharField(
        max_length=1, help_text="Kolumna zawierająca opisy (np. 'A')"
    )
    description_range = CellRangeSerializer(help_text="Zakres wierszy z opisami")

    def validate_description_column(self, value):
        # Walidacja, czy kolumna to pojedyncza litera A-Z
        if not re.match(r"^[A-Z]$", value):
            raise serializers.ValidationError(
                "Kolumna musi być pojedynczą wielką literą (A-Z)"
            )
        return value


class WorkingFileConfigSerializer(FileConfigSerializer):
    """Serializer dla konfiguracji pliku WF"""

    price_target_column = serializers.CharField(
        max_length=1, help_text="Kolumna docelowa dla cen (np. 'F')"
    )

    def validate_price_target_column(self, value):
        # Walidacja, czy kolumna to pojedyncza litera A-Z
        if not re.match(r"^[A-Z]$", value):
            raise serializers.ValidationError(
                "Kolumna musi być pojedynczą wielką literą (A-Z)"
            )
        return value


class ReferenceFileConfigSerializer(FileConfigSerializer):
    """Serializer dla konfiguracji pliku REF"""

    price_source_column = serializers.CharField(
        max_length=1, help_text="Kolumna źródłowa z cenami (np. 'D')"
    )

    def validate_price_source_column(self, value):
        # Walidacja, czy kolumna to pojedyncza litera A-Z
        if not re.match(r"^[A-Z]$", value):
            raise serializers.ValidationError(
                "Kolumna musi być pojedynczą wielką literą (A-Z)"
            )
        return value


class MatchingRequestSerializer(serializers.Serializer):
    """Główny serializer dla żądania porównania"""

    working_file = WorkingFileConfigSerializer()
    reference_file = ReferenceFileConfigSerializer()
    matching_threshold = serializers.IntegerField(
        min_value=1,
        max_value=100,
        default=80,
        help_text="Próg podobieństwa w procentach (domyślnie 80)",
    )

    def validate(self, data):
        """Dodatkowa walidacja całości danych"""
        wf_range = data["working_file"]["description_range"]
        ref_range = data["reference_file"]["description_range"]

        # sprawdzenie czy zakresy są poprawne (start < end)
        if wf_range["start"] >= wf_range["end"]:
            raise serializers.ValidationError(
                "Zakres WF: komórka początkowa musi być przed końcową"
            )

        if ref_range["start"] >= ref_range["end"]:
            raise serializers.ValidationError(
                "Zakres REF: komórka początkowa musi być przed końcową"
            )

        return data


class MatchingSessionSerializers(serializers.ModelSerializer):
    """Serializer dla modelu MatchingSession"""

    class Meta:
        model = MatchingSession
        fields = [
            "id",
            "created_at",
            "working_file_path",
            "reference_file_path",
            "status",
            "error_message",
        ]


class MatchingResultSerializer(serializers.ModelSerializer):
    """Serializer dla modelu MachingResult"""

    class Meta:
        model = MatchingResult
        fields = [
            "id",
            "session",
            "wf_description",
            "wf_cell",
            "ref_description",
            "ref_cell",
            "match_score",
            "price",
        ]
