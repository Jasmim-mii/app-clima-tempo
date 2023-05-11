import json
from datetime import date
import urllib.parse
import requests
from apiKey import (myToken,accuweatherApiKey)

weeks = ['domingo:','Segunda-Feira: ','Teça-Feira:','Quarta-Feira:','Quinta-Feira:','Sexta-Feira:','Sabado:'] 


def get_coordinates(): 

    r = requests.get('http://www.geoplugin.net/json.gp')

    if r.status_code != 200:
        print('Não foi possivel obter sua coordenadas')
        return None
    else:
        try:
            location = json.loads(r.text)
            coordinates = {}
            coordinates['lat'] = location['geoplugin_latitude']
            coordinates['long'] = location['geoplugin_longitude']
            return coordinates
        except:
            return None

 
def get_code_local(lat,long):

        # Obtendo local, Estado, cidade
    locationsApiUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=" + accuweatherApiKey + "%20&q=" + lat + "%2C%20" + long + "&language=pt-br"

    r = requests.get(locationsApiUrl)
    if r.status_code != 200:
        print('Não foi possivel obter o codigo do local, Limite de requisição da Api = 50. Tente mais tarde.')
        return None
    else:
        try:
            locationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['localName'] = locationResponse['LocalizedName'] + " , " \
                + locationResponse['AdministrativeArea']['LocalizedName'] + "." \
                + locationResponse['Country']['LocalizedName']
            infoLocal['local_code'] = locationResponse['Key']
            return infoLocal
        except:
            return None


def get_temperature(local_code, localName):

# obtendo a tempertura e o clima
    CurrentConditionsApiUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + local_code  + "?apikey=" + accuweatherApiKey + "&language=pt-br"


    r = requests.get(CurrentConditionsApiUrl)

    if r.status_code != 200:
        print('Não foi possivel obter o clima atual')
        return None
    else:
        try:
            CurrentConditionsResponse = json.loads(r.text)
            infoClima = {}
            infoClima['textClima'] = CurrentConditionsResponse[0]['WeatherText']
            infoClima['temperature'] = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
            infoClima['localName'] = localName
            return infoClima
        except:
            return None

def get_WeekDay(local_code):

    DailyResponseUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/" \
                              + local_code + "?apikey=" + accuweatherApiKey \
                              + "&metric=true&language=pt-br&details=true&getphotos=false"

    r = requests.get(DailyResponseUrl)
    if r.status_code != 200:
        print('Não foi possivel obter o dia atual')
        return None
    else:
        try: 
            DailyResponse = json.loads(r.text)
            info = []


            for day in DailyResponse['DailyForecasts']:  
                dayTime = {}  
                dayTime['max'] = day['Temperature']['Maximum']['Value']
                dayTime['min']  = day['Temperature']['Minimum']['Value']
                dayTime['clima']  = day['Day']['IconPhrase']
                weekDay = int(date.fromtimestamp(day['EpochDate']).strftime("%w"))
                dayTime['day'] = weeks[weekDay]
                info.append(dayTime)   
            return info

        except:
            return None

def Seachlocal(local):
    query = urllib.parse.quote(local)
    geocodeUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/" + query + ".json?access_token=" 
    
    r = requests.get(geocodeUrl)

    if r.status_code != 200:
        print('Não foi possivel obter o local atual')
        return None
    else:
        try:  
            geocodeResponse = json.loads(r.text)  
            coordinate_response = {}
            coordinate_response['long'] =  str(geocodeResponse['features'][0]['geometry']['coordinates'][0])
            coordinate_response['lat'] =  str(geocodeResponse['features'][0]['geometry']['coordinates'][0])
            return coordinate_response
        except:
            print('Erro ao pesquisar local')

       

