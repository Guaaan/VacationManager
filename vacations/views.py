from rest_framework import viewsets, permissions, decorators, response, status
from .models import VacationRequest
from .serializers import VacationRequestSerializer
from decimal import Decimal

class VacationRequestViewSet(viewsets.ModelViewSet):
    queryset = VacationRequest.objects.all()
    serializer_class = VacationRequestSerializer
    permission_classes = [permissions.AllowAny]  # cambiar a IsAuthenticated / IsAdminUser luego

    @decorators.action(detail=True, methods=['post'], url_path='approve')
    def approve(self, request, pk=None):
        vr = self.get_object()
        if vr.status != VacationRequest.STATUS_PENDING:
            return response.Response({'detail': 'Ya procesado'}, status=status.HTTP_400_BAD_REQUEST)

        user = vr.user
        # validar saldo
        if user.vacation_days < vr.days_requested:
            return response.Response({'detail': 'No hay suficientes días'}, status=status.HTTP_400_BAD_REQUEST)

        # restar días y cambiar estado
        user.vacation_days = Decimal(user.vacation_days) - Decimal(vr.days_requested)
        user.save()

        vr.status = VacationRequest.STATUS_APPROVED
        vr.save()
        return response.Response(self.get_serializer(vr).data, status=status.HTTP_200_OK)
