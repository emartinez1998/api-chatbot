

from django.http import JsonResponse
from django.contrib import admin
from django.urls import path, include

def health_check(request):
    return JsonResponse({"status": "ok", "message": "API Chatbot Liiffe funcionando"})

urlpatterns = [        
    path('', health_check),  # <- nueva vista para "/"
    path('api/', include('chatbot.urls')),   
    path('admin/', admin.site.urls),
]