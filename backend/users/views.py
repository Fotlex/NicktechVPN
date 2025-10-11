from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'], url_path='current')
    def current_user(self, request):
        user = request.tg_user 
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='ip')
    def get_user_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return Response({"ip": ip})
    
    
class ReferralViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def get_referrals(self, request):
        current_user = request.tg_user
        referrals = current_user.referrals.all()

        referral_data = []
        for referral in referrals:
            referred_user = referral.referred_by
            referral_data.append({
                'id': referred_user.id,
                'username': referred_user.username,
            })

        return Response(referral_data, status=status.HTTP_200_OK)