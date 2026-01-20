from rest_framework.routers import DefaultRouter

from .views import (
    TeaCategoryViewSet,
    OriginViewSet,
    TeaViewSet,
    OrderViewSet,
    OrderItemViewSet,
)

router = DefaultRouter()
router.register(r"categories", TeaCategoryViewSet)
router.register(r"origins", OriginViewSet)
router.register(r"teas", TeaViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"order-items", OrderItemViewSet)

urlpatterns = router.urls
