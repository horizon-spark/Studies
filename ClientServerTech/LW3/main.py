import requests
import os.path


def main():
    #1
    print('Task 1')

    health_check_response = requests.get("https://restful-booker.herokuapp.com/ping")
    print(health_check_response.status_code)


    #2
    print('Task 2')

    if os.path.exists('token.txt'):
        with open('token.txt', mode='r', encoding='utf-8') as f:
            token = f.readline()
            print('Токен был прочитан из файла')
    else:
        header = {
            'Content-Type': 'application/json'
        }
        data = {
            'username': 'admin',
            'password': 'password123'
        }

        token_response = requests.post('https://restful-booker.herokuapp.com/auth', headers=header, json=data)
        token = token_response.json()['token']

        print(token_response.status_code)

        with open('token.txt', mode='w', encoding='utf-8') as f:
            f.write(token)

    print('Токен:', token)

    #3
    print('Task 3')

    if os.path.exists('first_id.txt'):
        with open('first_id.txt', mode='r', encoding='utf-8') as f:
            id = f.readline()
    else:
        booking_response = requests.get('https://restful-booker.herokuapp.com/booking')
        id = booking_response.json()[0]['bookingid']

        print(booking_response.status_code)

        with open('first_id.txt', mode='w', encoding='utf-8') as f:
            f.write(str(id))

    print(id)


    #4
    print('Task 4')

    booking_id_response = requests.get(f'https://restful-booker.herokuapp.com/booking/{id}')
    booking_info = booking_id_response.json()

    print(booking_info)


    #5
    # print('Task 5')
    # booking_header = {
    #     'Content-Type': 'application/json'
    # }
    # booking_data = {
    #     'firstname': 'Ryan',
    #     'lastname': 'Gosling',
    #     'totalprice': 120,
    #     'depositpaid': True,
    #     'bookingdates': {
    #         'checkin': '2014-01-01',
    #         'checkout': '2015-02-02'
    #     },
    #     'additionalneeds': 'anti-stab-gear'
    # }
    # add_booking_response = requests.post('https://restful-booker.herokuapp.com/booking', headers=booking_header, json=booking_data)

    # print(add_booking_response.status_code)

    # if add_booking_response.status_code == 200:
    #     with open('created_id', mode='w', encoding='utf-8') as f:
    #         f.write(str(add_booking_response.json()['bookingid']))

    
    #6
    # print('Task 6')
    # put_header = {
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json',
    #     'Cookie': f'token={token}'
    # }
    # put_data = {
    #     'firstname': 'Bruce',
    #     'lastname': 'Lee',
    #     'totalprice': 150,
    #     'depositpaid': False,
    #     'bookingdates': {
    #         'checkin': '2016-02-02',
    #         'checkout': '2018-03-03'
    #     },
    #     'additionalneeds': 'kung-fu-stuff'
    # }

    # put_response = requests.put(f'https://restful-booker.herokuapp.com/booking/{id}', headers=put_header, json=put_data)

    # print(put_response.status_code)


    #7
    # print('Task 7')
    # patch_header = {
    #     'Content-Type': 'application/json',
    #     'Accept': 'application/json',
    #     'Cookie': f'token={token}'
    # }
    # patch_data = {
    #     'firstname': 'Jackie',
    #     'lastname': 'Chan'
    # }

    # patch_response = requests.patch(f'https://restful-booker.herokuapp.com/booking/{id}', headers=patch_header, json=patch_data)

    # print(patch_response.status_code)


    #8
    print('Task 8')
    delete_header = {
        'Content-Type': 'application/json',
        'Cookie': f'token={token}'
    }

    delete_response = requests.delete(f'https://restful-booker.herokuapp.com/booking/{id}', headers=delete_header)

    print(delete_response.status_code)

if __name__ == '__main__':
    main()