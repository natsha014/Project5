from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from study.permissions import IsOwner
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer, UserPublicSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)

    ordering_fields = ('payment_date',)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            instance = self.get_object()
            if instance != self.request.user:
                return UserPublicSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwner]
        return super().get_permissions()
