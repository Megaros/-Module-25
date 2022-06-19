import pytest
from selenium import webdriver

# python -m pytest -v --driver Chrome --driver-path chromedriver.exe  test_PetFrands.py


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    # Неявное ожидание готовности элементов перед попыткой взаимодействия
    pytest.driver.implicitly_wait(30)
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('meg@mail.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('1234')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()


    yield pytest.driver

    pytest.driver.quit()


def test_1():
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


def test_2():
    # Поиск фотографий
    images = pytest.driver.find_elements_by_css_selector('.card-img-top')
    # Поиск имени питомца
    names = pytest.driver.find_elements_by_css_selector('.card-deck.card-title')
    # Поиск вида и возроста
    descriptions = pytest.driver.find_elements_by_class_name('card-deck')

    for i in range(len(names)):
         assert images[i].get_attribute('src') != ''  # проверки существования фотографии
         assert names[i].text != ""  # проверки существования имени питомца
         assert descriptions[i].text != ' '  # проверки существования текста для вида и возроста
         assert ', ' in descriptions[i]  # проверки существования и вида и возроста
         parts = descriptions[i].text.split(", ")
         assert len(parts[0]) > 0  # проверки существования вида
         assert len(parts[1]) > 0  # проверки существования возроста

