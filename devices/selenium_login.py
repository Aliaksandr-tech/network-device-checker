from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def try_web_login(ip, port, login, password):
    """
    Пытается зайти на Web-интерфейс с заданными логином/паролем.
    Возвращает True, если вход успешен, иначе False.
    """
    url = f"http://{ip}:{port}"

    options = Options()
    options.headless = True  # Не показывать браузер (можно отключить для отладки)
    driver = None

    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(10)
        driver.get(url)
        time.sleep(2)

        # ⚠️ Здесь надо адаптировать под HTML устройства!
        try:
            user_field = driver.find_element(By.NAME, "username")
            pass_field = driver.find_element(By.NAME, "password")
        except NoSuchElementException:
            return False

        user_field.send_keys(login)
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN)

        time.sleep(3)

        # Простейшая проверка успешного входа
        return "logout" in driver.page_source.lower() or "dashboard" in driver.page_source.lower()

    except WebDriverException as e:
        print(f"Selenium error: {e}")
        return False

    finally:
        if driver:
            driver.quit()

