import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    """ библиотека API к приложению PetFriends """
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """ Метод делает запрос к API сервера и возвращает статус запроса, а также результат в формате
        json с уникальным ключом пользователя, найденного по указанным email и password"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = '') -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса, а также результат в формате json
        со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр может иметь либо
        пустое значение - получить список всех питомцев. Либо 'my_pets' - получить список собственных питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:
        """Метод посылает на API сервера POST-запрос, принимает в поле 'data' параметры питомца:
          кличку, вид животного, возраст, в заголовках - аутентификационный ключ, в файлах отправляет
        фотографию животного. Возвращает статус-код запроса и отправленные данные питомца в формате json"""

        # data = {'name': name,
        #         'animal_type': animal_type,
        #         'age': age,
        #         }
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })

        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        # file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def put_update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер об обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлёнными данными питомца"""

        data = dict(name=name, animal_type=animal_type, age=age)
        headers = {'auth_key': auth_key['key'], 'pet_id': pet_id}

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указаному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def post_add_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """ Метод отправляет на сервер фото и добавляет его в карточку ранее созданного питомца.
        Возвращает статус запроса и данные питомца в json"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        # file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpg')}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code

        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_new_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод посылает на API сервера POST-запрос на создание нового питомца без фото.
          Возвращает статус-код запроса и отправленные данные питомца в формате json"""

        # data = {'name': name,
        #         'animal_type': animal_type,
        #         'age': age,
        #         }

        # data = MultipartEncoder(
        #     fields={
        #         'name': name,
        #         'animal_type': animal_type,
        #         'age': age,
        #         'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        #     })
        data = {'name': name, 'animal_type': animal_type, 'age': age}
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


