from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import AllowAny 
from api_chatbot.authentication import APIKeyAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import requests
from django.core.exceptions import ValidationError
import time

@api_view(['GET'])
@permission_classes([HasAPIKey])
def chatbotGet(request):
    data = {"definicion": "Liiffe es una plataforma de viajes que ofrece itinerarios detallados de 3 días diseñados por lugareños para una experiencia auténtica."}
    return Response(data, status=200)  # Se devuelve JSON con código 200 OK

@api_view(['GET'])
@permission_classes([AllowAny]) 
def chatbotGuides(request):
    external_url = "https://liiffe.com/chatbot_rest.getGuias"  # URL real del endpoint externo

    # Obtener parámetros desde la URL, por ejemplo: ?pagina=2
    pagina = request.query_params.get('pagina', '1')  # valor por defecto '1'
    params = {'pagina': pagina}

    try:
        external_response = requests.get(external_url, params=params)
        external_response.raise_for_status()

        data = external_response.json()
        return Response(data, status=200)

    except requests.RequestException as e:
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)


@api_view(['POST'])
@permission_classes([HasAPIKey])
def chatbotPost(request):
    dato = request.data.get('dato')  # Obtiene el valor de 'dato' del request
    if not dato:
        return Response({"error": "El parámetro 'dato' es obligatorio."}, status=400)
    
    mensaje = f"El parámetro 'dato' ha sido recibido: {dato}"
    return Response({"mensaje": mensaje}, status=200)



@api_view(['GET'])
@permission_classes([AllowAny])
def chatbotGetPublic(request):
    time.sleep(4)  # Espera 4 segundos
    return Response({
        "status": "success",
        "data": {
            "definicion": "Liiffe es una plataforma de viajes que ofrece itinerarios detallados de 3 días diseñados por lugareños para una experiencia auténtica."
        }
    }, status=200)




@api_view(['GET'])
@authentication_classes([APIKeyAuthentication])
@permission_classes([AllowAny]) 
def pruebaApi(request):
    return Response({'mensaje': 'Autenticación correcta'})



@api_view(['GET'])
@authentication_classes([])  # Si quieres usar APIKeyAuthentication, déjala aquí
@permission_classes([AllowAny]) 
def validateUser(request):
    email = request.GET.get('email')

    if not email:
        return Response({'error': 'The field "email" is empty'}, status=400)

    try:
        if validate_email(email)=='true':        
            return Response({'mensaje': 'Valid email address', 'valid': 'true', 'first_name': 'Enrique'})
        else:
            return Response({'mensaje': 'Invalid email', 'valid': 'false', 'first_name': 'null'})
    except ValidationError:
        return Response({'error': 'Email no válido'}, status=400)



def validate_email(email):
    if email=='enrique@gmail.com':
        return 'true'
    else:
        return 'false'