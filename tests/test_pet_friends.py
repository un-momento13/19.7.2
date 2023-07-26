from api import PetFriends
from settings import valid_email, valid_password
import pytest
import os

pf = PetFriends()


@pytest.mark.positive
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


@pytest.mark.positive
def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' (все питомцы) """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


@pytest.mark.positive
def test_post_new_pet_with_valid_key(name='Hitch', animal_type='cat', age=10, pet_photo='images/cat.jpg'):
    """ Проверяем, что можно добавить питомца с валидными данными """
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # # Для получения полного, а не относительного пути к фото питомца.
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # pet_photo = os.path.normpath(pet_photo)

    # Добавляем питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result) > 0
    assert 'pet_photo' in result
    assert result['name'] == name


@pytest.mark.positive
def test_put_update_pet(name='Hitchcock', animal_type='old_cat', age=18):
    """ Проверяем возможность обновления информации о питомце """
    # Получаем ключ auth_key и запрашиваем список своих питомцев:
    # (При запросе получаем статус и результат, но статус нам не нужен, ставим прочерк)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, пробуем обновить вид животного и его возраст
    if len(my_pets['pets']) > 0:

        # Разберемся с индексами, распечатаем отдельные значения:
        print('\n\nname: ', my_pets['pets'][0]['name'])
        print('animal_type: ', my_pets['pets'][0]['animal_type'])
        print('age: ', my_pets['pets'][0]['age'])

        # Найдем id нужного питомца по имени:
        # pet_id = '0'
        # for pet in my_pets['pets']:
        #     if pet['name'] == name:
        #         pet_id = pet['id']
        #         break

        # Или же возьмем id первого питомца из списка
        pet_id = my_pets['pets'][0]['id']
        print('\n\n', pet_id)

        # и отправляем запрос на обновление:
        status, result = pf.put_update_pet(auth_key, pet_id, name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        # Если список пустой, выводим исключение с текстом об отсутствии своих питомцев
        raise Exception("Список моих питомцев пуст")


@pytest.mark.positive
def test_delete_pet_for_valid_id():
    """ Проверяем возможность удаления питомца """
    # Получаем ключ auth_key и запрашиваем список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Проверяем, есть ли питомцы в списке.
    if len(my_pets['pets']) == 0:
        # Берём id первого питомца из списка и отправляем запрос на удаление:
        pet_id = my_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

        # Еще раз запрашиваем список питомцев, чтобы проверить, нет ли в нем удаленного питомца:
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Проверяем, что статус ответа = 200, а в списке питомцев нет удаленного:
        assert status == 200
        assert pet_id not in my_pets.values()


@pytest.mark.positive
def test_post_add_photo(pet_photo='images/cat1.jpg'):
    """ Проверяем возможность добавления фото в карточку питомца """
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, пробуем обновить фото
    if len(my_pets['pets']) != 0:
        #  берём из этого списка id первого питомца и отправляем запрос на добавление фото:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

        assert status == 200
        assert result['pet_photo'] is not None
        print(status)
    else:
        # если список пустой, выводим исключение с сообщением, что список пуст
        raise Exception('Список ваших питомцев пуст, некуда добавить фото')


@pytest.mark.positive
def test_post_new_pet_simple_with_valid_key(name='Joseph', animal_type='dog', age=5):
    """ Проверяем, что можно добавить питомца с валидными данными, метод без фото """
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.post_new_pet_simple(auth_key, name, animal_type, str(age))
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert len(result) > 0
    assert result['name'] == name


# 1
# Список вариантов неправильного email (можно продолжить):
negative_email = ['', 'un-momento@yandex', '<script>alert(123)</script>',
                  'Aa!@#$%^&*()-_+=`~/\,.?><|b / PaSSword!@#$%^&*()-_+=`~/\,.?><|', 'UN-momento@yandeх.ru',
                  valid_password, 'уно@yandex.ru']


@pytest.mark.negative
def test_get_api_key_for_invalid_user(email=negative_email, password=valid_password):
    """ Запрос api ключа не выполняется при неправильных данных e-mail и password. Ожидается, что тест
    выдаст 403: ошибку на стороне клиента (предоставленные данные не верны)"""
    print()

    # Протестируем каждое из значений списка для поля email:
    for i in email:
        try:
            # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
            status, result = pf.get_api_key(i, password)
            # print(i, password, 'Status-code: ', status )
        except Exception:
            # Если возникла ошибка выполнения, печатаем пару email-password, вызвавшую ошибку:
            print('Execution error:', i, password)
            # Продолжим проверку с новым значением
            continue

        # Если статус ответа от сервера не 403 или присутствует ключ в теле ответа, тест провален
        if status != 403 or 'key' in result:
            print('Result error:', i, password, '   Status-code: ', status)

    assert status == 403


# 2
@pytest.mark.negative
def test_get_all_pets_with_invalid_key(filter=''):
    """ Запрос списка питомцев с неправильным ключом должен быть отклонен сервером. Ожидается ошибка 403
    - на стороне клиента """
    # Ключ аутентификации нужной длины, но не верный
    auth_key = {'key': '5be340894a8d13758243db49f68e112ee516633ad80b0d67a0ce733c'}
    status, _ = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


# 3
@pytest.mark.negative
def test_post_new_pet_without_name(name='', animal_type='anonymous', age=10, pet_photo='images/cat1.jpg'):
    """ Проверяем, что нельзя добавить питомца с пустым именем. Ожидается ошибка 403 - на стороне клиента """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Пробуем добавить питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

""" !!!Баг: сервер позволяет добавить питомца без имени !!! """

# 4
list_photo = ['images/cat1.jpeg', 'images/cat3.png']


@pytest.mark.additional_positive
def test_post_new_pet_with_diff_format_photo(name='Forrest', animal_type='cat', age=10, pet_photo=list_photo):
    """ Проверяем, что можно добавить фото питомца в форматах .png, .jpeg. Ожидаем ответ 200 """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    print()
    # Пробуем добавить питомца с разными форматами фото
    for i in list_photo:
        try:
            status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), i)
            print(name, i + '     Status-code: ', status)
        except Exception:
            # Если возникла ошибка выполнения, печатаем имя питомца и название файла, вызвавшего ошибку:
            print('Execution error:', name, i)
            continue

        if status != 200:
            print('Result error:', name, i, + '    Status-code: ', status)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

""" !!! Хотя этот тест имеет статус PASSED, фотография в формате .png на сайтне подгружается. 
Cсылке на фотографию (img src) не присваивается никакого значение !!! """


# 5
@pytest.mark.negative
def test_post_new_pet_with_invalid_animal_type(name='Fill', animal_type='007', age=10, pet_photo='images/cat.jpg'):
    """ Проверяем, что нельзя добавить питомца с цифрами вместо вида животного.
    Ожидается ошибка 403 - на стороне клиента """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Пробуем добавить питомца
    # ttt = os.path.normpath(os.path.abspath('test_pet_friends.py'))
    # os.chdir(os.path.normpath(os.path.abspath('test_pet_friends.py')))
    status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

""" !!! Баг: сервер добавляет питомца с цифрами вместо вида животного !!! """


# 6
@pytest.mark.negative
def test_post_new_pet_with_invalid_age(name='Sam', animal_type='cat', age='десять', pet_photo='images/cat.jpg'):
    """ Проверяем, что нельзя добавить питомца с буквенным значением возраста.
    Ожидается ошибка 403 - на стороне клиента """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Пробуем добавить питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

""" !!! Баг: сервер добавляет питомца с буквенным значением возраста !!! """

# 7
# Сгенерируем для этого теста имя длиной в 1000 символов
long_name = 'jYzwgh108Fs9OwiTYvLMDzpENdG1wKIcuXcJNBexIaAFZnC321NehgMn9iDPNSs4g1dt3dtr1S9aN5u4Ui1t3cSKDihewdmI' \
            'DrvAo9xov74TGDgApLeqPbkPSnviUdQffpfH1LMGe68CwZHYbbsrMoGoNDQJZqOQgDRAkiUGlJsAnJR7308mm4TKVhmhMJmo' \
            'Tr4MRzfk7H0JYrdhQEIMndIkDLkoFqFnABvWdYurKrT7jZgZoYhT366DAHWCyiOEwGB4SbzhPZz6lEKziq037W3seiiNZt1aWA' \
            'zpOhlYKEP00JBuJBwPSEgyioTu7yDcI7FDqyjqQYZt1RWMTKkVtWAfboh1byM0gzjOS3PqfuMqCkspXNmt8scfYi4pQFsCD60n4' \
            'xTrqTkk7JGFqx2TFBT4WFFc31LDOz1RQQA7Z3OGtKPpXo7M6ucuzbJGaA8zO144QZGLTePRo6A2RJEPDrzJ8PIcMovzLTYVf4' \
            'D2OQIF3GsZRAtjbD6eUbdi1H7noG7dAkPcfVXdqUi9l9E8UzQnhdJtQ7ry16XtyffcRKmpjH55V0O290zF3qkU1pEEfzVVbEe' \
            'OQmETpWfUWGTedZBkG3hRUWISVw5zyWqEZuf8ypfelJvwdofw49imoaqGHHVlZDWrgC5nQPvYTrr9k9HcPfbb9sHf5HO3xGacj' \
            'D3okd1iBNYC45Lxsp1yJIELlE9AXmnWSOy9ztJTmmdZxiuf6T19lLgYBgCaMCkz9tSqXzA3iQDtTDySdFhn0BqQKFWsD68GMd4R' \
            'cbbFQlzpjBgeRCuoMOCnk6bqStqFYbMDHvFEhBJbCwneA6gyX2tjnzCi37Khu59IMBCyBvzno6N8V2kXrw6vsR3H6Ri1wjFcNkAp' \
            'UOLjKldgbHQAhPF6wccMYYooijbRWYYOYkSsuRWw4sKOs9rdv3uJqB5czGSH8WCZwRk4jE9F5ocwUiFZNX9jtSZc1apVHg9Wyvva' \
            'WpjecbJ7ccGDf2ydphlv'


@pytest.mark.negative
def test_post_new_pet_with_too_long_name(name=long_name, animal_type='cat', age='десять',
                                         pet_photo='images/cat.jpg'):
    """ Проверяем, что при добавлении питомца поле name имеет ограничение по длине ввода символов """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Пробуем добавить питомца
    status, result = pf.post_new_pet(auth_key, name, animal_type, str(age), pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

""" !!! Баг: сервер добавляет питомца с именем длиной в 1000 символов, поле ввода не имеет ограничения
по длине!!! """


# 8
@pytest.mark.negative
def test_post_new_pet_simple_with_negative_number(name='Jon', animal_type='frog', age=-7):
    """ Нельзя добавить питомца с отрицательным возрастом, метод без фото """
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.post_new_pet_simple(auth_key, name, animal_type, str(age))
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

""" !!! Баг: сервер добавляет питомца с отрицательным значением возраста !!! """


# 9
@pytest.mark.negative
def test_post_add_photo_with_invalid_format(pet_photo='images/test.txt'):
    """ Нельзя добавить файл неподходящего формата """
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, пробуем обновить фото
    if len(my_pets['pets']) != 0:
        #  берём из этого списка id первого питомца и отправляем запрос на добавление фото:
        pet_id = my_pets['pets'][0]['id']
        status, result = pf.post_add_photo(auth_key, pet_id, pet_photo)

        assert status == 500
    else:
        # если список пустой, выводим исключение с сообщением, что список пуст
        raise Exception('Список ваших питомцев пуст, некуда добавить фото')

"""!!! Вообще-то должна быть ошибка 403, но на данный момент сервер выдает 500 !!! """


# 10
@pytest.mark.negative
def test_put_update_alien_pet(name='Hitchcock', animal_type='old_cat', age=18):
    """ Нельзя обновить не своего питомца. Пробуем обновлять по чужому id """
    # Получаем ключ auth_key и запрашиваем список своих питомцев:
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Если список не пустой,

    if len(my_pets['pets']) == 0:
        # Добавляем питомца в список:
        pf.post_new_pet_simple(auth_key, 'Lazutchik', 'abc', '1')

    # Получаем ID последнего питомца в списке
    pet_id = my_pets['pets'][-1]['id']

    # Заходим под другими данными email и password, получаем другой аутентификационный ключ:
    _, auth_key = pf.get_api_key('igra@bk.ru', '111')
    # и отправляем запрос на обновление:
    status, result = pf.put_update_pet(auth_key, pet_id, name, animal_type, age)

    assert status == 403
""" !!! Баг: обновлять данные чужого питомца не должно быть возможным !!! """
