class MatchingError(Exception):
    """ Klasa bazowa dla wyjątkó aplikacji matching"""
    pass

class ValidationError(MatchingError):
    """Wyjątek dla błęów walidacji"""
    pass

class ExcelProcessingError(MatchingError):
    """Wyjątek dla błędów przetwarzania Excela"""
    pass



