from rest_framework import routers

from lot.views import LotListView

router = routers.SimpleRouter()

router.register('lot', LotListView, basename='lot')
urlpatterns = router.urls
