from rest_framework.routers import SimpleRouter

from .views import VisitViewSet


visit_router = SimpleRouter()
visit_router.register('', VisitViewSet, basename='visit')

urlpatterns = (
    visit_router.urls +
    []
)
