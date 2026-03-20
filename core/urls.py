from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Import your farm logic views
from farm_api.views import (
    FarmTaskViewSet, 
    FieldViewSet, 
    LivestockViewSet, 
    TransactionViewSet, 
    current_user, 
    weather_forecast
)

# Import JWT views for authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView, 
    TokenRefreshView
)

# Import our custom Google Login view
from users.views import GoogleLogin

# 1. Setup the Router for CRUD operations
router = DefaultRouter()
router.register(r'tasks', FarmTaskViewSet, basename='farm-tasks')
router.register(r'fields', FieldViewSet, basename='fields')
router.register(r'livestock', LivestockViewSet, basename='livestock')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),

    # 🔐 Authentication & Identity (JWT)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 📝 User Registration & Management
    path('api/users/', include('users.urls')), 
    
    # 🌍 Standard & Social Auth
    path('api/auth/', include('dj_rest_auth.urls')), # login, logout, password reset
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')), # standard reg
    path('accounts/', include('allauth.urls')),
    
    # 🚀 Our Custom Google Login Endpoint
    path('api/auth/google/', GoogleLogin.as_view(), name='google_login'),
    
    # User Profile (Me endpoint)
    path('api/users/me/', current_user, name='current-user'),
    
    # 🚜 Farm Logic & Router URLs
    path('api/', include(router.urls)),
    
    # ☁️ External Services
    path('api/weather/', weather_forecast, name='weather-forecast'),
]