from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ReferralViewSet


router = DefaultRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'referrals', ReferralViewSet, basename='referrals')

urlpatterns = router.urls