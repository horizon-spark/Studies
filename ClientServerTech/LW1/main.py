import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os.path

def get_weather(api_key, city):
    """
    Получает текущую погоду и прогноз на 3 дня для указанного города
    """
    # URL для текущей погоды
    current_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ru"
    
    # URL для прогноза на 3 дня
    forecast_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3&lang=ru"

    today = datetime.today()
    astronomy_url = f"http://api.weatherapi.com/v1/astronomy.json?key={api_key}&q={city}&dt={today}&lang=ru"

    week = timedelta(7)
    history_url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={city}&dt={today - week}&end_dt={today}&lang=ru"
    
    try:
        # Получаем текущую погоду
        current_response = requests.get(current_url)
        current_data = current_response.json()
        
        # Получаем прогноз
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()

        astronomy_response = requests.get(astronomy_url)
        astronomy_data = astronomy_response.json()

        history_response = requests.get(history_url)
        history_data = history_response.json()
        
        # Проверяем наличие ошибок
        if 'error' in current_data:
            if current_data['error']['code'] == 1006:
                print("Ошибка: город не найден или название введено неправильно!")
            else:
                print(f"Ошибка: {current_data['error']['message']}")
            return
        
        # Выводим текущую погоду
        print("\n" + "="*50)
        print(f"Текущая погода в {current_data['location']['name']}, {current_data['location']['country']}")
        print(f"Локальное время: {current_data['location']['localtime']}")
        print(f"Температура: {current_data['current']['temp_c']}°C (ощущается как {current_data['current']['feelslike_c']}°C)")
        print(f"Погодные условия: {current_data['current']['condition']['text']}")
        print(f"Влажность: {current_data['current']['humidity']}%")
        print(f"Скорость ветра: {current_data['current']['wind_kph']} км/ч")
        print(f"Давление: {current_data['current']['pressure_mb']} мбар")

        print(f"Восход Солнца: {astronomy_data['astronomy']['astro']['sunrise']}")
        print(f"Закат Солнца: {astronomy_data['astronomy']['astro']['sunset']}")
        print("="*50)
        
        # Выводим прогноз на 3 дня
        print("\nПрогноз погоды на 3 дня:")
        print("="*50)
        
        for day in forecast_data['forecast']['forecastday']:
            date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            print(f"\nДата: {date}")
            print(f"Макс. температура: {day['day']['maxtemp_c']}°C")
            print(f"Мин. температура: {day['day']['mintemp_c']}°C")
            print(f"Средняя температура: {day['day']['avgtemp_c']}°C")
            print(f"Погодные условия: {day['day']['condition']['text']}")
            print(f"Вероятность дождя: {day['day']['daily_chance_of_rain']}%")
            print(f"Количество осадков: {day['day']['totalprecip_mm']} мм")
            print("-"*50)

        last_week_agv_temp = []
        last_week_dates = []

        for day in history_data['forecast']['forecastday']:
            date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%d.%m.%Y')
            last_week_dates.append(date)
            last_week_agv_temp.append(day['day']['avgtemp_c'])

        figure, axes = plt.subplots()

        axes.set_xlabel("День")
        axes.set_ylabel(f"Средняя температура, \u00b0С")

        axes.set_title(f"Средняя температура в городе {current_data['location']['name']} на прошлой неделе")

        axes.plot(last_week_dates, last_week_agv_temp)

        plt.show()

            
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка при обработке JSON: {e}")
    except KeyError as e:
        print(f"Ошибка в структуре полученных данных: {e}")

def main():
    # Ваш API ключ от WeatherAPI.com
    if os.path.exists('API_KEY.txt'):
        with open("API_KEY.txt", 'r') as f:
            API_KEY = f.readline()
        
        print("Программа прогноза погоды с использованием WeatherAPI.com")
        city = input("Введите название города: ")
        
        get_weather(API_KEY, city)

    else:
        print('Для работы программы необходимо создать файл API_KEY.txt и поместить в него ключ')

if __name__ == "__main__":
    main()