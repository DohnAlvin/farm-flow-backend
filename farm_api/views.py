import requests
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FarmTask, Field, Livestock, Transaction
from .serializers import FarmTaskSerializer, FieldSerializer, LivestockSerializer, TransactionSerializer

class FarmTaskViewSet(viewsets.ModelViewSet):
    serializer_class = FarmTaskSerializer
    permission_classes = [IsAuthenticated] # 🔐 Block unauthenticated users

    def get_queryset(self):
        # 🔐 Only return tasks owned by the logged-in user
        return FarmTask.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 🔐 Automatically assign the logged-in user to the new task
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n" + "="*50)
            print("🚨 TASK CREATION FAILED (400 Bad Request)!")
            print("React sent this data:", request.data)
            print("Django rejected it because:", serializer.errors)
            print("="*50 + "\n")
            
        return super().create(request, *args, **kwargs)

class FieldViewSet(viewsets.ModelViewSet):
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Field.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LivestockViewSet(viewsets.ModelViewSet):
    serializer_class = LivestockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Livestock.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# --- CUSTOM ENDPOINTS ---

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Real user endpoint! Returns the data of the currently logged-in user."""
    user = request.user
    return Response({
        "id": user.id, 
        "username": user.username, 
        "first_name": user.first_name,
        "email": user.email,
        "is_staff": user.is_staff
    })

@api_view(['GET'])
def weather_forecast(request):
    """Fetches real-time weather and forecast data from WeatherAPI"""
    location = request.GET.get('location', 'Nairobi, Kenya')
    API_KEY = "8fe4b3b6440447b686e112259261803"

    try:
        url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={location}&days=3&aqi=no&alerts=no"
        api_response = requests.get(url)
        data = api_response.json()

        if 'error' in data:
            return Response({"error": data['error']['message']}, status=400)

        forecast_days = []
        if 'forecast' in data:
            for day in data['forecast']['forecastday'][1:]: 
                forecast_days.append({
                    "day": day['date'], 
                    "temp": day['day']['avgtemp_c'],
                    "condition": day['day']['condition']['text']
                })

        return Response({
            "location": f"{data['location']['name']}, {data['location']['country']}",
            "temperature": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
            "humidity": data['current']['humidity'],
            "wind_speed": data['current']['wind_kph'],
            "forecast": forecast_days
        })

    except Exception as e:
        print("🚨 Weather API Error:", e)
        return Response({"error": "Could not fetch weather data right now."}, status=500)