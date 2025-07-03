import fitz  # PyMuPDF
import re

def extract_auth_data_from_pdf(pdf_path):
    """
    Пытается найти логин и пароль в PDF.
    Возвращает (login, password) или (None, None).
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()

        # Регулярки: ищем что-то типа "login: admin", "password: 1234"
        login_match = re.search(r"(login|username|user)[^\w]{0,10}([a-zA-Z0-9@#\-\.]{3,})", text, re.IGNORECASE)
        password_match = re.search(r"(password)[^\w]{0,10}([a-zA-Z0-9@#\-\.\d]{3,})", text, re.IGNORECASE)

        login = login_match.group(2).strip() if login_match else None
        password = password_match.group(2).strip() if password_match else None

        # Чёрный список очевидного мусора
        bad_words = {
            'and', 'or', 'is', 'the', 'are', 'to', 'in', 'of',
            'protected', 'protected.', 'password', 'login', 'note', 'use', 'none', 'see'
        }

        if login and login.lower() in bad_words:
            login = None
        if password and password.lower() in bad_words:
            password = None

        return login, password
    except Exception as e:
        print(f"Ошибка при парсинге PDF: {e}")
        return None, None
# парсинг функций из даташитов:

def parse_feature_in_datasheet(filepath, feature_name):
    """
    Примерный парсер, который ищет feature_name в PDF-файле datasheet.
    Возвращает True, если функция найдена, иначе False.

    Тут можно использовать PyMuPDF, PyPDF2 или pdfplumber.
    """
    import fitz  # PyMuPDF

    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return feature_name.lower() in text.lower()
    except Exception as e:
        print(f"Ошибка парсера: {e}")
        return False
