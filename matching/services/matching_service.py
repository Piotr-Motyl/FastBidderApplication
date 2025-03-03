from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from rapidfuzz import fuzz

from matching.exceptions import MatchingError


@dataclass
class MatchingCandidate:
    """Klasa pomocnicza przechwoująca kondydata do dopasowania"""

    description: str
    cell_address: str
    price: Decimal
    match_score: float = 0.00


class MatchingService:
    """Serwis odpowiedzialny za porównanie opisów i znajdowanie najlepszych dopasowań"""

    def __init__(self, matching_function=fuzz.ratio):
        """Inicjalizacja serwisu

        Args:
            matching_function: Funkcja porównująca z RapidFuzz (domyślnie ratio)
        """
        self.matching_function = matching_function

    def find_best_match(
        self,
        wf_description: Tuple[str, str],
        ref_descriptions: List[Tuple[str, str]],
        ref_prices: Dict[str, Decimal],
        ref_price_column: str,
        threshold: int,
    ) -> Optional[Dict]:
        """Znajduje najlepsze dopasowanie dla opisu z pliku WF

        Args:
            wf_description: (opis, adres_komórki) z pliku WF
            ref_descriptions: lista (opis, adres_komórki) z pliku REF
            ref_prices: słownik {adres_komórki: cena} z pliku REF
            threshold: próg podobieństwa (0-100)

        Returns:
            Dict z informacjami o najlepszym dopasowaniu lub None jeśli nie znaleziono
        """
        print("DEBUG: *** find_best_match *** was called from the MatchingService")

        wf_desc, wf_cell = wf_description
        best_match = None
        best_score = -1

        # Debugowanie - sprawdź co otrzymaliśmy
        print(f"DEBUG: ref_price_column = {ref_price_column}")
        print(
            f"DEBUG: ref_prices keys = {list(ref_prices.keys())[:5]}"
        )  # Pierwsze 5 kluczy

        # szukamy najlepszego dopasowania
        for ref_desc, ref_cell in ref_descriptions:
            try:
                # Obliczanie podobieństwa za pomocą RapidFuzz
                score = self.matching_function(wf_desc, ref_desc)

                # Wyciągamy numer wiersza z adresu komórki (np. '4' z 'C4')
                # TODO: Zamienić na regular expressions ponieważ kolumny mogą być AA+
                ref_row = ref_cell[1:]

                # Tworzymy adres komórki z ceną (np. 'E4')
                price_cell = f"{ref_price_column}{ref_row}"

                # Debugowanie - sprawdź konkretny klucz
                if ref_desc == ref_descriptions[0][0]:  # tylko dla pierwszego elementu
                    print(f"DEBUG: price_cell = {price_cell}")
                    print(
                        f"DEBUG: price_cell exists in ref_prices: {price_cell in ref_prices}"
                    )

                # Aktualizacja najlepszego dopasowania
                if score > best_score:
                    best_score = score
                    best_match = MatchingCandidate(
                        description=ref_desc,
                        cell_address=ref_cell,
                        # ref_prices: Dict[str, Decimal]
                        price=ref_prices.get(price_cell, Decimal("0")),
                        match_score=score,
                    )

            except Exception as e:
                raise MatchingError(f"Błąd podczas porównywania opisów: {str(e)}")

        if best_match and best_match.match_score >= threshold:
            return {
                "wf_description": wf_desc,
                "wf_cell": wf_cell,
                "ref_description": best_match.description,
                "ref_cell": best_match.cell_address,
                "match_score": best_match.match_score,
                "price": best_match.price,
            }

        return None

    def process_descriptions(
        self,
        wf_descriptions: List[Tuple[str, str]],
        ref_descriptions: List[Tuple[str, str]],
        ref_prices: Dict[str, Decimal],
        ref_price_column: str,
        threshold: int = 80,
    ) -> List[Dict]:
        """
        Przetwarza wszystkie opisy i znajduje najlepsze dopasowania

        Args:
            wf_descriptions: lista (opis, adres_komórki) z pliku WF
            ref_descriptions: lista (opis, adres_komórki) z pliku REF
            ref_prices: słownik {adres_komórki: cena} z pliku REF
            ref_price_column: kolumna, z której pochodzą ceny
            threshold: próg podobieństwa (domyślnie 80)

        Returns:
            Lista słowników z informacjami o dopasowaniach
        """
        print("DEBUG: *** process_descriptions *** was called from the MatchingService")

        results = []

        for wf_desc in wf_descriptions:
            match = self.find_best_match(
                wf_desc, ref_descriptions, ref_prices, ref_price_column, threshold
            )
            if match:
                results.append(match)

        print(
            f"DEBUG: AFTER for+in: ref_descriptions: {ref_descriptions} / ref_prices: {ref_prices} *** process_descriptions *** in matching_service"
        )
        return results

    def get_matching_statistics(self, results: List[Dict]) -> Dict:
        """
        Oblicza statystyki dopasowań (przygotowane pod przyszłe rozszerzenia)

        Args:
            results: Lista wyników dopasowania

        Returns:
            Słownik ze statystykami
        """
        print(
            "DEBUG: *** get_matching_statistics *** was called from the MatchingService"
        )

        if not results:
            return {
                "total_matches": 0,
                "average_score": 0,
                "min_score": 0,
                "max_score": 0,
            }

        scores = [r["match_score"] for r in results]
        return {
            "total_matches": len(results),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
        }
