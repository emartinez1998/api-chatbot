
from django.urls import path
from .views import chatbotGet, chatbotPost, chatbotGetPublic, chatbotGuides, pruebaApi, validateUser, validateReservation, getSuitablePlaces, getAvailabilityPlaces, updateItinerary, validateItineraryPlace, getCancellationPolicy  # Importa las funciones de vista

urlpatterns = [
    path('chatbot/get/', chatbotGet, name='chatbot-get'),  # Endpoint GET
    path('chatbot/post/', chatbotPost, name='chatbot-post'),  # Endpoint POST
    path('chatbot/guides/', chatbotGuides, name='chatbot-guides'),  # Endpoint POST
    path('chatbot/public/', chatbotGetPublic, name='chatbot-public'),  # Endpoint POST
    path('chatbot/prueba/', pruebaApi, name='chatbot-prueba'),  # Endpoint POST
    path('chatbot/validate-user/', validateUser, name='validate-user'),  # Endpoint POST
    path('chatbot/validate-reservation/', validateReservation, name='validate-reservation'),  # Endpoint POST
    path('chatbot/get-suitable-places/', getSuitablePlaces, name='get-suitable-places'),  # Endpoint GET
    path('chatbot/get-availability-places/', getAvailabilityPlaces, name='get-availability-places'),  # Endpoint GET
    path('chatbot/put-itinerary-user/', updateItinerary, name='put-itinerary-user'),  # Endpoint POST
    path('chatbot/validate-itinerary-place/', validateItineraryPlace, name='validate-itinerary-place'),  # Endpoint POST    
    path('chatbot/get-cancellation-policy/', getCancellationPolicy, name='get-cancellation-policy'),  # Endpoint POST
]

