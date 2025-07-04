# самый рабочий вариант
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
    TimeoutException
)
import time

def try_web_login(ip: str, port: int, login: str, password: str) -> bool:
    """
    Универсальная функция: открывает браузер, логинится (или считает уже залогиненным), и сразу пытается выйти.
    Возвращает True, если сессия активна (вход выполнен или уже был), False при явной ошибке.
    """
    url = f"http://{ip}:{port}"
    options = Options()
    options.headless = True  # Поменяйте на False для отладки
    driver = None

    try:
        # Создаём драйвер и открываем страницу
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)
        driver.get(url)
        time.sleep(2)

        # Пытаемся найти поля для логина
        user_field = None
        pass_field = None
        try:
            user_field = driver.find_element(By.NAME, "username")
            pass_field = driver.find_element(By.NAME, "password")
            print("Найдены поля для логина: выполняем вход")
        except NoSuchElementException:
            # Если поля не найдены, возможно, мы уже залогинены
            print("Поля логина/пароля не найдены — считаем уже авторизованным")

        # Если нашли поля — вводим учётные данные
        if user_field and pass_field:
            user_field.clear()
            user_field.send_keys(login)
            pass_field.clear()
            pass_field.send_keys(password)
            pass_field.send_keys(Keys.RETURN)
            time.sleep(3)  # Дождаться загрузки после входа

        # Проверяем успешность сессии по ключевым индикаторам
        page = driver.page_source.lower()
        indicators = [
            "logout", "выход", "dashboard", "mainframe",
            "topframe", "настройки", "панель", "home"
        ]
        if not any(ind in page for ind in indicators):
            print("⚠️ Сессия не активна (нет индикаторов)")
            return False

        print("✅ Сессия активна — теперь выход")

        # Инъектируем confirm override, чтобы окно не блокировало
        driver.execute_script("window.confirmlogout = ()=>true;")
        time.sleep(0.5)

        # Отправляем форму логаута
        try:
            form = driver.find_element(By.NAME, "cmlogout")
            driver.execute_script("arguments[0].submit();", form)
            print("🔄 Форма logout отправлена")

            # Ждём перенаправления обратно на страницу логина
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                print("✅ Logout успешен — поле логина найдено")
            except TimeoutException:
                print("⚠️ Поле логина не появилось после logout — возможно не полностью вышли")

        except NoSuchElementException:
            print("⚠️ Форма logout не найдена — возможно, другая структура")

        return True

    except WebDriverException as e:
        print(f"🚨 Selenium ошибка: {e}")
        return False

    finally:
        if driver:
            driver.quit()








