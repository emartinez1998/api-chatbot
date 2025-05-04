from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import requests
from django.core.exceptions import ValidationError
import time


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chatbotGet(request):
    data = {"definicion": "Liiffe es una plataforma de viajes que ofrece itinerarios detallados de 3 días diseñados por lugareños para una experiencia auténtica."}
    return Response(data, status=200)  # Se devuelve JSON con código 200 OK

@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def chatbotPost(request):
    dato = request.data.get('dato')  # Obtiene el valor de 'dato' del request
    if not dato:
        return Response({"error": "El parámetro 'dato' es obligatorio."}, status=400)
    
    mensaje = f"El parámetro 'dato' ha sido recibido: {dato}"
    return Response({"mensaje": mensaje}, status=200)



@api_view(['GET'])
@permission_classes([AllowAny])
def chatbotGetPublic(request):    
    return Response({
        "status": "success",
        "data": {
            "definicion": "Liiffe es una plataforma de viajes que ofrece itinerarios detallados de 3 días diseñados por lugareños para una experiencia auténtica."
        }
    }, status=200)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pruebaApi(request):
    return Response({'mensaje': 'Autenticación correcta'})


def validate_email(email):
    if email=='enrique@gmail.com':
        return 'true'
    else:
        return 'false'
    
    
    
## -----------  1. VALIDA CORREO -----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validateUser(request):
    email = request.data.get('email')  # Cambiado a .data para POST

    if not email:
        return Response({'error': 'The field "email" is empty'}, status=400)

    try:
        if validate_email(email) == 'true':
            return Response({'message': 'Valid email address', 'valid': 'true', 'first_name': 'Enrique'})
        else:
            return Response({'message': 'Invalid email', 'valid': 'false', 'first_name': 'null'})
    except ValidationError:
        return Response({'error': 'Invalid email'}, status=400)



## -----------  1. VALIDA NUMERO DE RESERVA -----------
def validate_reservation_number(reservation_number):
    if reservation_number==323235443534:
        return 'true'
    else:
        return 'false'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validateReservation(request):
    reservation_number = request.data.get('reservation_number')  # Cambiado a .data para POST

    if not reservation_number:
        return Response({'error': 'The field "reservation_number" is empty'}, status=400)

    try:
        if validate_reservation_number(reservation_number) == 'true':
            return Response({'message': 'Valid reservation number', 'valid': 'true'})
        else:
            return Response({'message': 'Invalid reservation number', 'valid': 'false'})
    except ValidationError:
        return Response({'error': 'Invalid reservation number'}, status=400)