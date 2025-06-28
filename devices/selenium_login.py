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





# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException, WebDriverException
# import time
#
# def try_web_login(ip, port, login, password):
#
#     url = f"http://{ip}:{port}"
#     options = Options()
#     options.headless = True
#     driver = None
#
#     try:
#         driver = webdriver.Chrome(options=options)
#         driver.set_page_load_timeout(10)
#         driver.get(url)
#         time.sleep(2)
#
#         # Попытка найти поля логина и пароля
#         try:
#             user_field = driver.find_element(By.NAME, "username")
#             pass_field = driver.find_element(By.NAME, "password")
#         except NoSuchElementException:
#             return False
#
#         user_field.send_keys(login)
#         pass_field.send_keys(password)
#         pass_field.send_keys(Keys.RETURN)
#         time.sleep(3)  # Ждём загрузку
#
#         page = driver.page_source.lower()
#
#         # Универсальные признаки успешного входа
#         success_indicators = [
#             "logout", "выход", "dashboard", "mainframe", "topframe", "настройки", "панель", "home"
#         ]
#
#         # Если хотя бы один индикатор найден — считаем успешным вход
#         if any(indicator in page for indicator in success_indicators):
#
#             return True
#
#         # Доп. попытка: проверить наличие кнопки "Logout" по id/class
#         try:
#             logout_btn = driver.find_element(By.XPATH, "//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'logout')]")
#             return True
#         except NoSuchElementException:
#             pass
#
#         return False
#
#     except WebDriverException as e:
#         print(f"Selenium error: {e}")
#         return False
#
#     finally:
#         if driver:
#             driver.quit()

# # относительно рабочий
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import (
#     NoSuchElementException,
#     WebDriverException,
#     TimeoutException
# )
# import time
#
# def try_web_login(ip, port, login, password):
#     """
#     Открывает браузер, логинится на устройство по IP и порт,
#     проверяет успешность входа, затем пытается корректно выйти
#     с учётом всплывающего confirm().
#     """
#     url = f"http://{ip}:{port}"
#     options = Options()
#     options.headless = True  # Поставьте False для отладки, чтобы видеть браузер
#     driver = None
#
#     try:
#         # 1) Запускаем браузер и открываем страницу
#         driver = webdriver.Chrome(options=options)
#         driver.set_page_load_timeout(10)
#         driver.get(url)
#         time.sleep(2)
#
#         # 2) Ищем поля для логина и пароля
#         try:
#             user_field = driver.find_element(By.NAME, "username")
#             pass_field = driver.find_element(By.NAME, "password")
#         except NoSuchElementException:
#             print("Поля логина/пароля не найдены")
#             return False
#
#         # 3) Вводим учётные данные и отправляем форму
#         user_field.send_keys(login)
#         pass_field.send_keys(password)
#         pass_field.send_keys(Keys.RETURN)
#         time.sleep(3)  # Дождаться загрузки после входа
#
#         # 4) Проверяем успешность входа по ключевым индикаторам
#         page = driver.page_source.lower()
#         success_indicators = [
#             "logout", "выход", "dashboard",
#             "mainframe", "topframe", "настройки",
#             "панель", "home"
#         ]
#         if not any(ind in page for ind in success_indicators):
#             print("Вход не удался")
#             return False
#
#         print("Вход успешен — переопределяем confirmlogout и выходим")
#
#         # 5) Переопределяем функцию confirmlogout, чтобы она возвращала true сразу
#         driver.execute_script("""
#             window.confirmlogout = function() {
#                 return true;
#             };
#         """)
#
#         # 6) Отправляем форму logout
#         try:
#             logout_form = driver.find_element(By.NAME, "cmlogout")
#             driver.execute_script("arguments[0].submit();", logout_form)
#             print("Форма logout отправлена без confirm()")
#
#             # 7) Ждём появления alert до 3 секунд и принимаем, если он есть
#             try:
#                 WebDriverWait(driver, 3).until(EC.alert_is_present())
#                 alert = driver.switch_to.alert
#                 alert.accept()
#                 print("Алерт подтверждения принят")
#             except TimeoutException:
#                 print("Алерт не появился или исчез слишком быстро")
#
#             # 8) Короткая пауза для завершения разлогина
#             time.sleep(1)
#
#         except NoSuchElementException:
#             print("Форма logout не найдена — возможно, другая структура")
#
#         return True
#
#     except WebDriverException as e:
#         print(f"Selenium ошибка: {e}")
#         return False
#
#     finally:
#         if driver:
#             driver.quit()



