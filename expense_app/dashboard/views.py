
# dashboard/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DashboardSerializer
from .services import DashboardService
from expense_app.accounts.permissions import IsRegularUserOnly

class DashboardView(APIView):
    permission_classes = [ IsRegularUserOnly]

    def get(self, request):
        service = DashboardService(user=request.user)
        data = service.get_dashboard_data()
        serializer = DashboardSerializer(data)
        return Response(serializer.data)



