from django.db import models


class MatchingSession(models.Model):
    """Model przechowujący informacje o sesjii do porownywania"""

    created_at = models.DateTimeField(auto_now_add=True)
    working_file_path = models.CharField(max_length=255)
    reference_file_path = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "W trakcie"),
            ("COMPLETED", "Zakończone"),
            ("ERROR", "Błąd"),
        ],
        default="PENDING",
    )
    error_message = models.TextField(null=True, blank=True)


class MatchingResult(models.Model):
    """Model przechowujacy wyniki porownania"""

    session = models.ForeignKey(MatchingSession, on_delete=models.CASCADE)

    # Dane z pliku WF "Working File"
    wf_description = models.TextField()
    wf_cell = models.CharField(max_length=10)
    price_target_cell = models.CharField(
        max_length=10
    )  # Komórka gdzie będzie wpisana cena
    source_info_cell = models.CharField(
        max_length=10
    )  # Komórka gdzie będzie info o źródle

    # Dane z pliku REF (Reference File)
    ref_description = models.TextField()
    ref_cell = models.CharField(max_length=10)
    ref_file_name = models.CharField(max_length=255)

    # Informacje o dopasowaniu
    match_score = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Metadane
    created_at = models.DateTimeField(auto_now_add=True)  # timestamp utworzenia wpisu

    class Meta:
        ordering = ["-match_score"]  # sortowanie po score malejąco
        indexes = [
            models.Index(fields=["session", "match_score"]),
            models.Index(fields=["wf_cell"]),
        ]

    def __str__(self):
        return f"Dopasowanie: {self.wf_cell} -> {self.ref_cell} (score: {self.match_score}%)"

    @property
    def source_info(self) -> str:
        """Generuje informację o źródle ceny (komórka i nazwa pliku)"""

        return (
            f"Cena z {self.ref_file_name}"
            f"komórka {self.ref_cell}"
            f"(podobieńśtwo: {self.match_score:.1f}%)"
        )
