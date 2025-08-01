# usuarios/views.py

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):   
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']
    
    def get_permissions(self):
        """
        Permitir acceso sin autenticación para ciertos métodos
        """
        if self.action in ['login', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:  # create, update, partial_update, destroy
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Endpoint personalizado para login
        """
        # Usar el serializador personalizado para validar las credenciales
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generar tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )