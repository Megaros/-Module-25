from selenium import webdriver
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# python -m pytest -v --driver Chrome --driver-path chromedriver.exe  test_my_pets.py
@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')

    yield pytest.driver

    pytest.driver.quit()
def test_my_pets():
    # Неявное ожидание готовности элементов перед попыткой взаимодействия
    # pytest.driver.implicitly_wait(30)
    # Вводим email ( c использованием явного ожидания)
    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    ).send_keys('meg@mail.ru')
    # pytest.driver.find_element_by_id('email').send_keys('meg@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('1234')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Заходим на страницу <Мои питомцы>
    pytest.driver.find_element_by_xpath('//a[@href="/my_pets"]').click()
    # Проверяем, что мы на странице <Мои питомцы>
    assert pytest.driver.find_element_by_tag_name('h2').text == 'OlegK'
    # Создаем список карточек питомцев с помощью локатора кнопки <удалить>
    list_may_pets = pytest.driver.find_elements_by_xpath('//div[@title = "Удалить питомца"]')
    # Cоздаем список фотографий соих питомцев
    images_list = pytest.driver.find_elements_by_xpath('//th/img')
    # Назначаем переменную для подсчёта количества питомцев пользователя с фотографией
    photo_presence_count = 0
    # Через проверку, что  attribute 'src' не пустое значение, определяем
    # количество питомцев с фотографией
    for i in range(len(list_may_pets)):
        if images_list[i].get_attribute('src') != '':
            photo_presence_count += 1
    # Проверяем, что как минимум половина всех питомцев имеет фотографию
    assert photo_presence_count >= (len(list_may_pets) / 2)
    # Проверяем, что у всех питомцев есть  имя, возраст и порода.
    names = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    breed = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    age = pytest.driver.find_elements_by_xpath('//*[@id="all_my_pets"]/table/tbody/tr/td[3]')
    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''
    # Проверяем, что у питомцев нет одинаковых имен
    names_set = tuple(names)
    for i in range(len(names)):
        assert len(names_set) == len(names)
    # Проверяем, что в списке нет питомцев с одинаковым именем, возрастом и породой
    breed_set = tuple(breed)
    age_set = tuple(age)
    names_set = tuple(names)
    print(breed_set, age_set, names_set, breed)
    assert (len(names_set) == len(names)) and (len(breed_set) == len(breed) and (len(age_set) == len(age))), "Есть одинаковые питомцы"
