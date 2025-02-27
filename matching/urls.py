from django.urls import path
from matching.views import MatchingView

urlpatterns = [
    path("compare/rapidfuzz/", MatchingView.as_view(), name="compare-rapidfuzz"),
]
