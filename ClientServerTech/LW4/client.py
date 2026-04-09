import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

SERVER_URL = "http://localhost:8000"

def main():
    print("1. Получить токен")
    print("2. Получить защищенные данные")
    print("3. Получить данные о токене")
    print("4. Выход")
    
    token = None
    
    while True:
        choice = input("Выберите действие: ")
        
        if choice == "1":

            while(1):
                username = input("Логин: ")
                password = input("Пароль: ")

                if (len(username) == 0 or len(password) == 0):
                    print("Логин и пароль не могут быть пустыми!")
                else:
                    break
            
            try:
                response = requests.post(
                    f"{SERVER_URL}/token",
                    data={"username": username, "password": password},
                    timeout=10  # таймаут 10 секунд
                )
                
                if response.status_code == 200:
                    token = response.json()["access_token"]
                    print("Токен получен!")
                else:
                    error_msg = response.json().get("detail", "Неизвестная ошибка")
                    print(f"Ошибка {response.status_code}: {error_msg}")
                    
            except ConnectionError:
                print("Ошибка: Не удалось подключиться к серверу. Убедитесь, что сервер запущен.")
            except Timeout:
                print("Ошибка: Превышено время ожидания ответа от сервера.")
            except RequestException as e:
                print(f"Ошибка при выполнении запроса: {e}")
            except ValueError:
                print("Ошибка: Сервер вернул некорректный ответ.")
                
        elif choice == "2":
            if not token:
                print("Ошибка: Сначала получите токен")
                continue
                
            try:
                response = requests.get(
                    f"{SERVER_URL}/secure-data",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    print("Данные:", response.json())
                elif response.status_code == 401:
                    print("Ошибка 401: Токен недействителен или истек. Получите новый токен.")
                    token = None  # Сбрасываем недействительный токен
                else:
                    error_msg = response.json().get("detail", "Неизвестная ошибка")
                    print(f"Ошибка {response.status_code}: {error_msg}")
                    
            except ConnectionError:
                print("Ошибка: Не удалось подключиться к серверу.")
            except Timeout:
                print("Ошибка: Превышено время ожидания ответа от сервера.")
            except RequestException as e:
                print(f"Ошибка при выполнении запроса: {e}")
            except ValueError:
                print("Ошибка: Сервер вернул некорректный ответ.")

        elif choice == "3":
            if not token:
                print("Ошибка: Сначала получите токен")
                continue
            
            try:
                response = requests.get(
                    f"{SERVER_URL}/token-info",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    info = response.json()
                    print(f"Пользователь: {info['username']}")
                    print(f"Истекает: {info['expires_at']}")
                    print(f"Действителен: {info['is_valid']}")
                    print("Для просмотра этих данных выполняется проверка токена")
                    
                    if not info['is_valid']:
                        print("Внимание: Токен истек! Рекомендуется получить новый.")
                        token = None
                        
                elif response.status_code == 401:
                    print("Ошибка 401: Токен недействителен или истек. Получите новый токен.")
                    token = None
                else:
                    error_msg = response.json().get("detail", "Неизвестная ошибка")
                    print(f"Ошибка {response.status_code}: {error_msg}")
                    
            except ConnectionError:
                print("Ошибка: Не удалось подключиться к серверу.")
            except Timeout:
                print("Ошибка: Превышено время ожидания ответа от сервера.")
            except RequestException as e:
                print(f"Ошибка при выполнении запроса: {e}")
            except ValueError:
                print("Ошибка: Сервер вернул некорректный ответ.")
            except KeyError as e:
                print(f"Ошибка: В ответе сервера отсутствует поле {e}")

        elif choice == "4":
            break

        else:
            print("Ошибка: Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

if __name__ == "__main__":
    main()