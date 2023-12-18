from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet
from django.db.models.functions import Greatest
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.views import APIView


class TrigramSimilaritySearchFilter(SearchFilter):
    DEFAULT_TRIGRAM_SIMILARITY = 0.2

    def get_trigram_similarity(self, view: APIView) -> float:
        return getattr(view, "trigram_similarity", self.DEFAULT_TRIGRAM_SIMILARITY)

    def filter_queryset(
        self, request: Request, queryset: QuerySet, view: APIView
    ) -> QuerySet:
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)
        trigram_similarity = self.get_trigram_similarity(view)

        if not search_fields or not search_terms:
            return queryset

        conditions = []
        for search_term in search_terms:
            conditions.extend(
                [
                    TrigramSimilarity(search_field, search_term)
                    for search_field in search_fields
                ]
            )

        return queryset.annotate(similarity=Greatest(*conditions)).filter(
            similarity__gte=trigram_similarity
        )
