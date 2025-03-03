from decimal import Decimal
from typing import List, Dict, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class MatchingConfig:
    """
    Konfiguracja procesu dopasowania
    """

    # Pliki
    working_file_path: Path
    reference_file_path: Path
    # Parametry dopasowania
    matching_threshold: float
    # Dodajemy konfigurację kolumn i zakresów
    wf_description_column: str
    wf_description_range: Dict[str, str]
    wf_price_target_column: str
    ref_description_column: str
    ref_description_range: Dict[str, str]
    ref_price_source_column: str


class MatchingOrchestrator:
    """
    Koordynator procesu dopasowania, implementujący wzorzec Facade.
    Odpowiada za kolejność i koordynację wykonywania operacji przez pozostałe serwisy.
    """

    def __init__(
        self,
        excel_processor,  # wstrzykiwanie zależności przez konstruktor
        data_validator,  # ułatwia testowanie i rozszerzanie
        matching_service,
        result_writer,
    ):
        """
        Inicjalizacja orchestratora z wszystkimi wymaganymi serwisami.
        Wykorzystuje wzorzec Dependency Injection dla łatwiejszego testowania.
        """
        self.excel_processor = excel_processor
        self.data_validator = data_validator
        self.matching_service = matching_service

        # Przekazujemy excel_processor do result_writer
        if not hasattr(result_writer, "excel_processor"):
            result_writer.excel_processor = excel_processor
        self.result_writer = result_writer

        # Status dla każdego zadania
        self._processing_status: Dict[str, str] = {}

    def process_matching_request(self, config: MatchingConfig) -> str:
        """
        Główna metoda koordynująca cały proces dopasowania.
        Zwraca ścieżkę do pliku raportu.

        Args:
            config: Pełna konfiguracja procesu dopasowania

        Returns:
            str: Ścieżka do wygenerowanego pliku raportu

        Raises:
            Exception: W przypadku błędów w trakcie przetwarzania
        """
        print(
            "DEBUG: *** process_matching_request *** was called from the MatchingOrchestrator"
        )

        try:
            # 1. Walidacja danych wejściowych
            self.data_validator.validate_files(
                config.working_file_path, config.reference_file_path
            )

            # 2. Wczytanie plików Excel
            self.excel_processor.load_files(
                working_file=config.working_file_path,
                reference_file=config.reference_file_path,
            )

            # 3. Pobieramy dane z plików Excel za pomocą metody extract_excel_data
            wf_descriptions, ref_descriptions, ref_prices, ref_price_column = (
                self._extract_excel_data(config)
            )

            # 4. Wykonanie dopasowania
            matching_results = self.matching_service.process_descriptions(
                wf_descriptions=wf_descriptions,
                ref_descriptions=ref_descriptions,
                ref_prices=ref_prices,
                ref_price_column=ref_price_column,
                threshold=config.matching_threshold,
            )

            print(
                f"DEBUG: BEFORE saving: matching_results: {matching_results} \n wf_price_target_column: {config.wf_price_target_column} \n *** process_matching_request *** at matching_orchestrator"
            )

            # 5. Zapis wyników - ResultWriter został już zaktualizowany do korzystania z ExcelProcessor
            report_path = self.result_writer.write_results(
                matching_results,
                config.working_file_path,
                config.wf_price_target_column,
            )

            # 6. Zamknięcie plików po zakończeniu
            self.excel_processor.close_all_workbooks()

            return report_path

        except Exception as e:
            # Centralne miejsce obsługi błędów
            self._handle_error(str(e))
            # Upewnij się, że pliki są zamknięte nawet w przypadku błędu
            self.excel_processor.close_all_workbooks()
            raise

    def _extract_excel_data(
        self, config: MatchingConfig
    ) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]], Dict[str, Decimal], str]:
        """
        Pobiera dane z plików Excel potrzebne do procesu dopasowania.

        Args:
            config: Konfiguracja zawierająca ścieżki i zakresy

        Returns:
            Tuple zawierająca:
            - Lista krotek (opis, adres_komórki) z pliku WF
            - Lista krotek (opis, adres_komórki) z pliku REF
            - Słownik {adres_komórki: cena} z pliku REF
        """
        print(
            "DEBUG: *** _extract_excel_data *** was called from the MatchingOrchestrator"
        )

        # Pobierz opisy z pliku WF
        wf_descriptions = self.excel_processor.read_descriptions(
            file_path=config.working_file_path,
            column=config.wf_description_column,
            cell_range=config.wf_description_range,
        )

        # Pobierz opisy z pliku REF
        ref_descriptions = self.excel_processor.read_descriptions(
            file_path=config.reference_file_path,
            column=config.ref_description_column,
            cell_range=config.ref_description_range,
        )
        print(
            f"DEBUG: matching_orchestrator: column taken from REF ***{config.ref_description_column}***"
        )
        print(
            f"DEBUG: matching_orchestrator: cell_range taken from REF ***{config.ref_description_range}***"
        )

        # Pobierz ceny z pliku REF
        ref_prices = self.excel_processor.read_prices(
            file_path=config.reference_file_path,
            price_column=config.ref_price_source_column,
            row_range=config.ref_description_range,  # używamy tego samego zakresu wierszy co dla opisów
        )
        print(
            f"DEBUG: matching_orchestrator: read_prices taken from REF ***{config.ref_price_source_column}***"
        )

        return (
            wf_descriptions,
            ref_descriptions,
            ref_prices,
            config.ref_price_source_column,
        )

    def _handle_error(self, error_message: str) -> None:
        """
        Centralna obsługa błędów - w przyszłości można dodać:
        - Logowanie do pliku/systemu
        - Powiadomienia (email, Slack)
        - Metryki błędów
        """
        # TODO: Implementacja logowania błędów
        pass

    def get_processing_status(self, job_id: str) -> str:
        """
        Zwraca status przetwarzania dla danego zadania

        Args:
            job_id: Identyfikator zadania

        Returns:
            str: Status przetwarzania
        """
        return self._processing_status.get(job_id, "UNKNOWN")
