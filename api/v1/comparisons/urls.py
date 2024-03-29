from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.v1.comparisons.views import (
    ComparisonsDestroyView,
    ComparisonCreateView,
    ComparisonListView,
    ComparisonGroupViewSet,
    ComparisonGroupsChangeOrderView,
)

app_name = "comparisons"

router = DefaultRouter()
router.register("groups", ComparisonGroupViewSet, basename="comparison-groups")

urlpatterns = [
    path(
        "groups/change-order/",
        ComparisonGroupsChangeOrderView.as_view(),
        name="change-groups-order",
    ),
    path("", include(router.urls)),
    path("list/", ComparisonListView.as_view(), name="list"),
    path("add/", ComparisonCreateView.as_view(), name="add"),
    path("remove/", ComparisonsDestroyView.as_view(), name="remove"),
]
