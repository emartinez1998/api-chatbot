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
    if email=='enrique@gmail.comenrique@gmail.com':
        return 'true'
    else:
        return 'false'
    
    
    
## -----------  *. VALIDA CORREO -----------
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



## -----------  *. VALIDA NUMERO DE RESERVA -----------
def validate_reservation_number(reservation_number):
    if reservation_number=='323235443534':
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
    
    
    

## -----------  *. VALIDA LUGAR DE ITENARIO A MODIFICAR  -----------  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validateItineraryPlace(request):
    reservation_number = request.data.get('reservation_number') 
    place_description = request.data.get('place_description') 

    if not (reservation_number and place_description):        
        return Response({'status': 'ERROR', 'message': 'All fields are required: reservation_number, place_description', 'id_place': 'null'}, status=400)
    
    if place_description.casefold() == 'diurnothe retiro park'.casefold():
        return Response({'status': 'OK', 'message': 'Place found', 'id_place': 23489 }, status=200)

    # Este return faltaba
    return Response({ 'status': 'ERROR', 'message': 'Place not found', 'id_place': 'null'}, status=404)




    
    
## -----------  *. OBTIENE LUGARES ADECUADOS  -----------   
def get_suitiable_places(conditions, id_place):
        
    if conditions.casefold() == 'boring'.casefold():
        places = {
            "places_found": "true",
            "suitiable_places":[
                {
                    "id_place":1,
                    "title":"COMMERCIAL COFFEE",
                    "description":"This cozy café is the perfect spot for those who appreciate a great cup of coffee in a relaxed, modern setting. With a carefully curated selection of beans and expert preparation, every sip here is an experience. "
                },
                {
                    "id_place":2,
                    "title":"FARADAY",
                    "description":"Store located in the Plaza del Cordon, in the heart of Madrid, selling a selection of sweets made in convents and monasteries in Spain.  "
                },
                {
                    "id_place":3,
                    "title":"SAN GINÉS",
                    "description":"Great location near Plaza Mayor. You can choose from a mix of churros and porras."
                }
            ]
        }
    else:
        places = {
            "places_found": "false",
            "suitiable_places":[
                {
                    "id_place":"null",
                    "title":"null",
                    "description":"null"
                },
                {
                    "id_place":"null",
                    "title":"null",
                    "description":"null"
                },
                {
                    "id_place":"null",
                    "title":"null",
                    "description":"null"
                }
            ]
        }
        
    return places
    
    

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getSuitablePlaces(request):
    
    id_place = request.data.get('id_place')
    conditions = request.data.get('conditions')  # Cambiado a .data para POST

    if not conditions:
        return Response({'error': 'The field "conditions" is empty'}, status=400)

    try:        
        places = get_suitiable_places(conditions=conditions, id_place=id_place)                
        return Response(places, status=200)
    except ValidationError:
        return Response({'error': 'Invalid reservation number'}, status=400)
    
    
    

## -----------  *. OBTIENE LUGARES ABIERTOS O DISPONIBLES  -----------   
def get_availability_places():
    
    places = {
        "places_found": "true",
        "availability_places":[
            {
                "id_place":1,
                "title":"CASA BOTIN",
                "description":"This historic spot is much more than just a restaurant; it's a true culinary institution with centuries of tradition. Known for its classic ambiance and unparalleled legacy "
            },
            {
                "id_place":2,
                "title":"LHARDY",
                "description":"Emblematic and historical place of a must-see in Madrid.  "
            },
            {
                "id_place":3,
                "title":"PRADO MUSEUM",
                "description":"This is one of the most outstanding museums in the world, and is also among the most visited. "
            }
        ]
    }

        
    return places
    
    

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAvailabilityPlaces(request):  

    id_place = request.data.get('id_place')   

    if not (id_place):        
        return Response({'status': 'ERROR', 'message': 'All fields are required: id_place'}, status=400) 

    try:        
        places = get_availability_places()        
        return Response(places, status=200)
    except ValidationError:
        return Response({'error': 'Invalid reservation number'}, status=400)
    
    


## -----------  *. ACTUALIZAR ITINERARIO - LUGARES ADECUADOS  -----------  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateItinerarySuitable(request):
    id_reservation = request.data.get('id_reservation') 
    id_previous_place = request.data.get('id_previous_place')  
    id_new_place = request.data.get('id_new_place')  

    if not (id_reservation and id_previous_place and id_new_place):
        return Response(
            {'error': 'All fields are required: id_reservation, id_previous_place, id_new_place'},
            status=400
        )

    # Aquí puedes insertar tu lógica de actualización real del itinerario

    return Response({'status':'OK', 'message': 'Itinerary successfully updated'}, status=200)


## -----------  *. ACTUALIZAR ITINERARIO - LUGARES DISPONIBLES  -----------  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateItineraryAvailable(request):
    id_reservation = request.data.get('id_reservation') 
    id_previous_place = request.data.get('id_previous_place')  
    id_new_place = request.data.get('id_new_place')  

    if not (id_reservation and id_previous_place and id_new_place):
        return Response(
            {'error': 'All fields are required: id_reservation, id_previous_place, id_new_place'},
            status=400
        )

    # Aquí puedes insertar tu lógica de actualización real del itinerario

    return Response({'status':'OK', 'message': 'Itinerary successfully updated'}, status=200)



## -----------  *. CONSULTAR POLITICA DE CANCELACION  -----------  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getCancellationPolicy(request):
    id_reservation = request.data.get('id_reservation')     

    if not (id_reservation):
        return Response(
            {'status': 'ERROR', 'message': 'All fields are required: id_reservation'},
            status=400
        )

    # Aquí puedes insertar tu lógica de actualización real del itinerario

    return Response({'status':'OK', 'message': 'Itinerary successfully updated', 'cancellation_policy':'Las cancelaciones deben realizarse con al menos 24 horas de antelación a la fecha programada del servicio para recibir un reembolso completo. Cancelaciones realizadas con menos de 24 horas de aviso o en caso de no presentarse, no serán reembolsadas. Esta política busca garantizar una adecuada planificación y respeto por el tiempo de nuestros guías.'}, status=200)





## -----------  *. OBTIENE FECHAS DISPONIBLES  -----------   
def get_available_dates(id_reservation):
        
    if id_reservation!='':
        available_dates = {
            "available_dates_guide": "true",
            "dates":[
                {
                    "date_1": "06-12-2025 12:00:00",
                    "date_2": "06-13-2025 11:00:00",
                    "date_3": "06-14-2025 15:00:00",
                }
            ]
        }
    else:
        available_dates = {
            "available_dates_guide": "false",
            "dates":[
                {
                    "date_1": "null",
                    "date_2": "null",
                    "date_3": "null",
                }
            ]
        }
        
    return available_dates
    
    

 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAvailableDates(request):
    
    id_reservation = request.data.get('id_reservation') 

    try:        
        dates = get_available_dates(id_reservation)                
        return Response(dates, status=200)
    except ValidationError:
        return Response({'error': 'Invalid reservation number'}, status=400)
    
    


## -----------  *. CONSULTAR POLITICA DE CANCELACION  -----------  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateReservationDate(request):
    
    id_reservation = request.data.get('id_reservation')    
    date =  request.data.get('date')

    if not (id_reservation and date):
        return Response(
            {'error': 'All fields are required: id_reservation, date'},
            status=400
        )

    # Aquí puedes insertar tu lógica de actualización real del itinerario

    return Response({'status':'OK', 'message': 'Reservation date successfully updated'}, status=200)