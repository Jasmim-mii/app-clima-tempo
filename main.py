from clima_tempo import (get_code_local, get_coordinates, get_temperature,
                         get_WeekDay, Seachlocal)

check_location = 's'

def see_weather_forecast(lat, long):
    try:
        localization = get_code_local(lat, long)
        climaAtual = get_temperature(localization['local_code'],localization['localName'])
        print('Clima atual: ' + climaAtual['localName'])
        print(climaAtual['textClima'])
        print('Temperatura: ' + str(climaAtual['temperature']) + "\xb0" + "C")
    except:
        print('Erro, não foi possível obter previsão atual')


    options =  input('Deseja ver a previsão para os proximos dias? (s ou n) = ').lower()

    if options == 's':

        print('\n Previsão para os proximos dias. \n')
        try:
            weather_forecast = get_WeekDay(localization['local_code'])
            for day in weather_forecast:
                print(day['day'])
                print('Minuma: '+ str(day['min']) + "\xb0" + "C")
                print('Máxima: '+ str(day['max']) + "\xb0" + "C")
                print('Previsão: ' + day['clima'])
                print('\n')
        except:
            print('Erro ao obter a previsão para os proximos dias')                   

try:
    check_coordinates = get_coordinates() 
    see_weather_forecast(check_coordinates['lat'], check_coordinates['long'])
    while check_location == 's':
        check_location = input('Deseja consultar a previsão de outro local? (s ou n): ').lower()
        if check_location != 's':
            break
        local = input('Digite a cidade e o estado = ').lower()
        try:
            coordinate_response = Seachlocal(local)
            see_weather_forecast(check_coordinates['lat'], check_coordinates['long'])
        except:
            print(' Local não encontrado.')

except:
    print(' Erro ao processar a solicitação.')

