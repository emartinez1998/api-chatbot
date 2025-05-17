from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import requests
from django.core.exceptions import ValidationError
import time
import json
from difflib import SequenceMatcher


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







## -----------------------------   *. LIIFFE API  -------------------------------------------

## -----------------------------   *. VALIDAR USUARIO  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserByEmail(request):
    email = request.query_params.get('email', None)

    if not email:
        return Response({'error': 'El parámetro "email" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/users/clients/find-by-email/{email}/"

    headers = {
        "Content-Type": "application/json"        
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        # Devuelve tal cual lo que devuelve el endpoint externo (cuerpo y status)
        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        # En caso de que no haya respuesta (timeout, red, etc.)
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        
        

## -----------------------------   *. VALIDAR GUIA  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getGuideById(request):
    
    id = request.query_params.get('id', None)

    if not id:
        return Response({'error': 'El parámetro "id" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guides/{id}/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"      
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        # Devuelve tal cual lo que devuelve el endpoint externo (cuerpo y status)
        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        # En caso de que no haya respuesta (timeout, red, etc.)
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        
        

## -----------------------------   *. OBTENER DIAS DE UNA GUIA  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDaysGuide(request):
    guide = request.query_params.get('guide', None)

    if not guide:
        return Response({'error': 'El parámetro "guide" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guide-days/?guide={guide}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"
    }

    try:
        external_response = requests.get(external_url, headers=headers)
        data = external_response.json()

        # Si hay menos de 5, completar con objetos por defecto
        while len(data) < 5:
            data.append({
                "id": 0,
                "translations": {
                    "es": {
                        "title": "",
                        "content": ""
                    },
                    "en": {
                        "title": "",
                        "content": ""
                    }
                },
                "createdAt": None,
                "updatedAt": None,
                "dayNumber": None,
                "isActive": False,
                "image": None,
                "guide": int(guide) if guide.isdigit() else None
            })

        # Si hay más de 5, truncar (opcional, pero por si acaso)
        data = data[:5]

        return Response(data=data, status=external_response.status_code)

    except requests.RequestException as e:
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)



## -----------------------------   *. OBTENER LOS LUGARES DE UN DIA POR ID  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlacesByDay(request):
    
    guideDay = request.query_params.get('guideDay', None)

    if not guideDay:
        return Response({'error': 'El parámetro "guideDay" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guide-day-pois/?guideDay={guideDay}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"      
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        # Devuelve tal cual lo que devuelve el endpoint externo (cuerpo y status)
        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        # En caso de que no haya respuesta (timeout, red, etc.)
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        
        
## -----------------------------   *. OBTENER SUGERENCIAS DE LUGARES DE PARA UN DIA  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRecommendedPlaces(request):
    
    id = request.query_params.get('id', None)

    if not id:
        return Response({'error': 'El parámetro "id" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guide-day-pois/{id}/backup-places/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"      
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        # Devuelve tal cual lo que devuelve el endpoint externo (cuerpo y status)
        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        # En caso de que no haya respuesta (timeout, red, etc.)
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        


## -----------------------------   *. OBTENER INFORMACION DE UN LUGAR POR SU ID  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPlaceById(request):
    
    id = request.query_params.get('id', None)

    if not id:
        return Response({'error': 'El parámetro "id" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/destinations/places/{id}/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"      
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        # Devuelve tal cual lo que devuelve el endpoint externo (cuerpo y status)
        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        # En caso de que no haya respuesta (timeout, red, etc.)
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        
        
        

## -----------------------------   *. ACTUALIZAR LUGAR DE INTERES DE UNA GUIA  -------------------------------------------
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def updateGuide(request):
    id = request.data.get('id', None)
    place = request.data.get('place', None)

    if not id or not place:
        return Response({'error': 'Los parámetros "id" y "place" son requeridos'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guide-day-pois/{id}/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"
    }

    payload = {
        "place": place
    }

    try:
        external_response = requests.patch(external_url, headers=headers, data=json.dumps(payload))

        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)



## -----------------------------   *. OBTENER DATOS DE MULTIPLES LUGARES  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDataPlaces(request):
    
    ids = request.query_params.getlist('id')

    if not ids:
        return Response({'error': 'Debe proporcionar al menos un parámetro "id"'}, status=400)

    # Construir la URL con múltiples ids
    params = '&'.join([f'id={i}' for i in ids])
    external_url = f"https://back-staging.liiffe.com/api/destinations/places/?{params}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"
    }

    try:
        external_response = requests.get(external_url, headers=headers)

        return Response(
            data=external_response.json(),
            status=external_response.status_code
        )

    except requests.RequestException as e:
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)
        
        


## -----------------------------   *. OBTENER DATOS DE MULTIPLES LUGARES  -------------------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSearchPlaceDay(request):
    
    guideDay = request.query_params.get('guideDay', None)
    name = request.query_params.get('name', None)

    if not guideDay:
        return Response({'error': 'El parámetro "guideDay" es requerido'}, status=400)

    external_url = f"https://back-staging.liiffe.com/api/products/guide-day-pois/?guideDay={guideDay}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "api-key s34Qs8vN.APOQ13YTmpyRSLGmIVVsgiTjxuAO8eAf"
    }

    try:
        external_response = requests.get(external_url, headers=headers)
        data = external_response.json()

        if name:
            name = name.strip().lower()
            best_match = None
            highest_ratio = 0.0

            # 1. Buscar coincidencia por substring exacta (prioridad)
            for item in data:
                place_name = item.get("placeData", {}).get("name", "").strip().lower()
                if name in place_name:
                    return Response(item, status=200)

            # 2. Si no hay coincidencia directa, usar similitud
            for item in data:
                place_name = item.get("placeData", {}).get("name", "").strip().lower()
                ratio = SequenceMatcher(None, name, place_name).ratio()
                if ratio > highest_ratio:
                    highest_ratio = ratio
                    best_match = item

            if best_match and highest_ratio > 0.3:
                return Response(best_match, status=200)
            else:
                return Response(
                    {'error': f'No se encontró ninguna coincidencia razonable para el nombre "{name}"'},
                    status=404
                )

        return Response(data, status=external_response.status_code)

    except requests.RequestException as e:
        return Response({
            'error': 'Error al consultar el endpoint externo',
            'detalle': str(e)
        }, status=500)