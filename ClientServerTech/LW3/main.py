import requests


def health_check():
    response = requests.get("https://restful-booker.herokuapp.com/ping")

    print('Проверка доступности, код ответа:', response.status_code)


def get_token():
    header = {
            'Content-Type': 'application/json'
        }
    data = {
            'username': 'admin',
            'password': 'password123'
        }

    response = requests.post('https://restful-booker.herokuapp.com/auth', headers=header, json=data)
    token = response.json()['token']

    print('Получение токена, код ответа:', response.status_code)
    print('Токен:', token)

    return token


def get_booking_list():
    response = requests.get('https://restful-booker.herokuapp.com/booking')
    id = response.json()[0]['bookingid']

    print('Получение списка бронирований, код ответа:', response.status_code)

    for booking in response.json():
        print(booking['bookingid'], end=' ')
    print()

    return id


def get_booking_info_by_id(id):
    response = requests.get(f'https://restful-booker.herokuapp.com/booking/{id}')

    print(f'Получение информации о бронировании с id={id}, код ответа:', response.status_code)

    if response.status_code == 404:
        print(f"Запись с id={id} не найдена")
    else:
        booking_info = response.json()
        print(booking_info)


def create_booking():
    header = {
        'Content-Type': 'application/json'
    }
    data = {
        'firstname': 'Ryan',
        'lastname': 'Gosling',
        'totalprice': 120,
        'depositpaid': True,
        'bookingdates': {
            'checkin': '2014-01-01',
            'checkout': '2015-02-02'
        },
        'additionalneeds': 'anti-stab-gear'
    }

    response = requests.post('https://restful-booker.herokuapp.com/booking', headers=header, json=data)

    if response.status_code == 200:
        id = response.json()['bookingid']
    else:
        id = -1
        return

    print('Создание нового бронирования, код ответа:', response.status_code)
    print('id созданного бронирования: ', id)
    
    get_booking_info_by_id(id)

    with open('created_id.txt', mode='w', encoding='utf-8') as f:
        f.write(str(id))


def update_booking_by_id(token, id):
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={token}'
    }
    data = {
        'firstname': 'Bruce',
        'lastname': 'Lee',
        'totalprice': 150,
        'depositpaid': False,
        'bookingdates': {
            'checkin': '2016-02-02',
            'checkout': '2018-03-03'
        },
        'additionalneeds': 'kung-fu-stuff'
    }

    response = requests.put(f'https://restful-booker.herokuapp.com/booking/{id}', headers=header, json=data)

    print(f'Обновление бронирования с id={id}, код ответа:', response.status_code)
    get_booking_info_by_id(id)


def patch_booking_by_id(token, id):
    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cookie': f'token={token}'
    }
    data = {
        'firstname': 'Jackie'
    }

    response = requests.patch(f'https://restful-booker.herokuapp.com/booking/{id}', headers=header, json=data)

    print(f'Частичное обновление бронирования с id={id}, код ответа:', response.status_code)
    get_booking_info_by_id(id)


def delete_booking_by_id(token, id):
    header = {
        'Content-Type': 'application/json',
        'Cookie': f'token={token}'
    }

    response = requests.delete(f'https://restful-booker.herokuapp.com/booking/{id}', headers=header)

    print(f'Удаление бронирования с id={id}, код ответа:', response.status_code)


def main():
    print("Задание 1")
    health_check()
    print()

    print("Задание 2")
    token = get_token()
    print()

    print("Задание 3")
    id = get_booking_list()
    print()

    print("Задание 4")
    get_booking_info_by_id(id)
    print()

    print("Задание 5")
    create_booking()
    print()

    print("Задание 6")
    update_booking_by_id(token, id)
    print()

    print("Задание 7")
    patch_booking_by_id(token, id)
    print()

    print("Задание 8")
    delete_booking_by_id(token, id)
    get_booking_info_by_id(id)


if __name__ == '__main__':
    main()