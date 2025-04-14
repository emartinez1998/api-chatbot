
from django.urls import path
from .views import chatbotGet, chatbotPost, chatbotGetPublic, chatbotGuides, pruebaApi  # Importa las funciones de vista

urlpatterns = [
    path('chatbot/get/', chatbotGet, name='chatbot-get'),  # Endpoint GET
    path('chatbot/post/', chatbotPost, name='chatbot-post'),  # Endpoint POST
    path('chatbot/guides/', chatbotGuides, name='chatbot-guides'),  # Endpoint POST
    path('chatbot/public/', chatbotGetPublic, name='chatbot-public'),  # Endpoint POST
    path('chatbot/prueba/', pruebaApi, name='chatbot-prueba'),  # Endpoint POST
]

