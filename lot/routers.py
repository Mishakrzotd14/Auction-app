from rest_framework.routers import DefaultRouter

from .views import LotListView

router = DefaultRouter()
router.register(r'lots', LotListView)
