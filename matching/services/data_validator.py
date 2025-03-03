from pathlib import Path
from typing import Dict, List
import openpyxl
from matching.exceptions import ValidationError


class DataValidator:
    """
    Klasa odpowiedzialna za walidację danych wejściowych
    """

    MAX_FILE_SIZE_MB = 10
    ALLOWED_EXTENSIONS = (".xlsx", ".xls")
    MIN_SHEETS = 1
    MAX_SHEETS = 10
    BYTES_IN_MB = 1024 * 1024

    def __init__(self):
        self.validation_errors: List[str] = []

    def validate_files(
        self, working_file_path: Path, reference_file_path: Path
    ) -> None:
        """Sprawdza poprawność plików wejściowych

        Args:
            working_file_path (Path): Ścieżka do pliku roboczego
            reference_file_path (Path): Ścieżka do pliku referencyjnego

        Raises:
            ValidationError: Gdy któryś z plików nie spełnia wymagań

        """
        print("DEBUG: *** validate_files *** was called from the DataValidator")
        files_to_validate = [
            ("Working File", working_file_path),
            ("Reference File", reference_file_path),
        ]

        for file_name, file_path in files_to_validate:
            # Sprawdzenie czy plik istnieje
            if not file_path.exists():
                raise ValidationError(f"{file_name} nie istnieje: {file_path}")

            # Sprawdzenie rozszerzenia
            if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                raise ValidationError(
                    f"Nieprawidłowe rozszerzenie pliku {file_name}"
                    f"Maksymalny rozmiar: {self.MAX_FILE_SIZE_MB}MB"
                )

            # Sprawdzenie rozmiaru pliku
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.MAX_FILE_SIZE_MB:
                raise ValidationError(
                    f"{file_name}jest za duży. "
                    f"Maksymalny rozmiar: {self.MAX_FILE_SIZE_MB}MB"
                )

    def validate_file_path(self, file_path: str) -> bool:
        """
        Sprawdza poprawność ścieżki do pliku Excel

        Args:
            file_path (str): Ścieżka do sprawdzenia

        Returns:
            bool: True jeśli plik jest poprawny, False w przeciwnym razie
        """
        print("DEBUG: *** wywołano metodę ===validate_file_path=== z DataValidator")
        try:
            path = Path(file_path)

            # Sprawdzenie czy plik istnieje
            if not path.exists():
                self.validation_errors.append(f"Plik {file_path} nie istnieje")
                return False

            # Sprawdzenie rozszerzenia
            if not path.suffix.lower() in self.ALLOWED_EXTENSIONS:
                self.validation_errors.append(
                    f"Niedozwolone rozszerzenie pliku {file_path}. "
                    f"Dozwolone: {', '.join(self.ALLOWED_EXTENSIONS)}"
                )
                return False

            # Sprawdzanie rozmiaru pliku
            file_size_mb = path.stat().st_size / self.BYTES_IN_MB
            if file_size_mb > self.MAX_FILE_SIZE_MB:
                self.validation_errors.append(
                    f"Plik {file_path} jest za duży."
                    f"Maksymalny rozmiar: {self.MAX_FILE_SIZE_MB}MB"
                )
                return False

            # sprawdzenie liczby arkuszy
            wb = openpyxl.load_workbook(file_path, read_only=True)
            sheet_count = len(wb.sheetnames)
            wb.close()

            if not (self.MIN_SHEETS <= sheet_count <= self.MAX_SHEETS):
                self.validation_errors.append(
                    f"Nieprawidlowa liczba arkuszy w pliku {file_path}."
                    f"Wymagane: od {self.MIN_SHEETS} do {self.MAX_SHEETS}"
                )
                return False

            return True

        except Exception as e:
            self.validation_errors.append(f"Błąd walidacji pliku {file_path}: {str(e)}")
            return False

    def validate_cell_range(self, cell_range: Dict[str, str], column: str) -> bool:
        """Sprawdza poprawnosc zakresu komorek

        Args:
            cell_range (Dict[str, str]): Słownik z kluczami 'start' i 'end'
            column (str): Kolumna, która powinna być użyuta w zakresie

        Returns:
            bool: True jesli zakres jest poporawny, False w przeciwnym razie
        """
        print("DEBUG: *** validate_cell_range *** was called from the DataValidator")

        try:
            start = cell_range["start"]
            end = cell_range["end"]

            # Sprawdzenie czy kolumna jest taka sama w zakrsue
            if not (start.startswith(column) and end.startswith(column)):
                self.validation_errors.append(
                    f"Zakres musi byc w kolumnie {column}" f"Podano {start}:{end}"
                )
                return False

            # Wydobycie numerów wierszy
            start_row = int("".join(filter(str.isdigit, start)))
            end_row = int("".join(filter(str.isdigit, end)))

            # sprawdzenie kolejności
            if start_row >= end_row:
                self.validation_errors.append(
                    f"Nieprawidłowy zakres {start}:{end} "
                    f"Wiersz początkowy musi być mniejszy niż końcowy"
                )
                return False

            return True

        except Exception as e:
            self.validation_errors.append(f"bład walidacji zakresu {str(e)}")
            return False

    def validate_price_column(self, price_column: str, description_column: str) -> bool:
        """Sprawdza poprawność kolumny z cenami

        Args:
            price_column (str): Kolumana z cenami
            description_column (str): Kolumna z opisami

        Returns:
            bool: True jeśli kolumna jest poprawna, False w przeciwnym razie
        """
        print("DEBUG: *** validate_price_column *** was called from the DataValidator")

        try:
            # Sprawdzenie czy kolumna jest pojedynczą literą A-Z (TODO: Zamienić na regular expressions ponieważ kolumny mogą być AA+)
            if not (len(price_column) == 1 and price_column.isalpha()):
                self.validation_errors.append(
                    f"Nieprawidłowa kolumna z cenami: {price_column}."
                    f"Wymaga pojedyncza litera A-Z"
                )
                return False
            # TODO: Kolumna cen NIE może być taka sama jak kolumna opisów
            return True

        except Exception as e:
            self.validation_errors.append(f"Błąd walidacji kolumny z cenami: {str(e)}")
            return False

    def validate_matching_request(self, request_data: Dict) -> None:
        """Główna metoda walidująca całe żądanie porównania

        Args:
            request_data (Dict): Dane żądania do zwalidowania

        Raises:
            validationError: Jeśli występują błędy walidacji
        """
        print(
            "DEBUG: *** validate_matching_request *** was called from the DataValidator"
        )

        # Reset lsity błędów
        self.validation_errors = []

        # Walidacja plików WF
        wf_config = request_data["working_file"]
        self.validate_file_path(wf_config["file_path"])
        self.validate_cell_range(
            wf_config["description_range"], wf_config["description_column"]
        )
        self.validate_price_column(
            wf_config["price_target_column"], wf_config["description_column"]
        )
        # Walidacja plików REF
        ref_config = request_data["reference_file"]
        self.validate_file_path(ref_config["file_path"])
        self.validate_cell_range(
            ref_config["description_range"], ref_config["description_column"]
        )
        self.validate_price_column(
            ref_config["price_source_column"], ref_config["description_column"]
        )

        # Jeśli są błędy, rzuć wyjątek
        if self.validation_errors:
            raise ValidationError(
                "Błąd walidacji:\n" + "\n".join(self.validation_errors)
            )
