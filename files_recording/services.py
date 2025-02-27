# import openpyxl
#
#
# def validate_column_exists(file_path, column_name):
#     """
#     Sprawdza, czy podana kolumna istnieje w pliku Excel.
#     :param file_path: Ścieżka do przesłanego pliku Excel.
#     :param column_name: Nazwa kolumny do sprawdzenia.
#     :return: True, jeśli kolumna istnieje; False w przeciwnym razie.
#     """
#     try:
#         # Otwieranie pliku Excel
#         workbook = openpyxl.load_workbook(file_path)
#         sheet = workbook.active # TODO: Pobiera pierwszą zakładkę, dodać możliwośc wskazania zakładki jeśli jest wiecej niz jedna
#
#         # Pobiera nagłówki (pierwszy wiersz)
#         headers = [cell.value for cell in sheet[1]]
#         return column_name in headers # Sprawdza, czy kolumna istnieje
#     except Exception as e:
#         raise ValueError(f"Błąd podczas przetwarzania plików Excel: {str(e)}")
#
