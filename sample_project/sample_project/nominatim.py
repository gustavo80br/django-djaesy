import requests
from django.conf import settings


def nominatim_reverse_geolocation(point):

    try:

        nominatim_api = f'{settings.NOMINATIM_URL}/reverse?lat={point[1]}&lon={point[0]}&format=json&addressdetails=1'

        data = requests.get(nominatim_api, timeout=30).json()
        address = data['address']
        addr_segments = []

        for item in settings.NOMINATIM_ADDRESS_DISPLAY:
            value = ''
            if isinstance(item, tuple):
                for sub_item in item:
                    value = address.get(sub_item, None)
                    if value:
                        break
            else:
                value = address.get(item, None)
            if value:
                addr_segments.append(value)

        address = ', '.join(addr_segments)

        return address

    except:
        return 'Erro no reverse geocoding'
