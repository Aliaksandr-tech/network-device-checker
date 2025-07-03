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

def normalize_text(text):
    # Удаляем дефисы, символы точки, кавычки и лишние пробелы, приводим к нижнему регистру
    return re.sub(r'[-‑–]', ' ', text).lower()

# Словарь синонимов и вариантов написания для разных сетевых функций
FEATURE_SYNONYMS = {
    'ICMP тип 0,8 (ping)': [
        'icmp', 'ping', 'icmp echo request', 'icmp echo reply',
        'icmpv4', 'icmpv6', 'ping only', 'traceroute', 'lookup operations'
    ],
    'DHCP-сервер': [
        'dhcp сервер', 'dhcp server', 'dhcpserver', '•dhcp ',
        'layer 3 services', 'centralized ipv4 address management',
        'provides dhcp', 'supports dhcp server'
    ],
    'DHCP-клиент': [
        'dhcp клиент', 'dhcp client', 'dhcpclient',
        'supports dhcp-based provisioning', 'dhcp-based process',
        'dhcp relay', 'dhcp snooping', 'dhcpv6 client'
    ],
    'Поддержка DHCP snooping': [
        'dhcp snooping', 'поддержка dhcp snooping',
        'supports dhcp snooping', 'dhcpv6 protection',
        'dhcpv6 snooping', 'dynamic ipv6 lockdown', 'ra guard'
    ],
    'Реализация RIP': [
        'rip', 'ripv1', 'ripv2', 'ripng',
        'routing information protocol', 'layer 3 routing', 'ipv6 routing ripng',
        'static, rip and access ospf routing'
    ],
    'Реализация IGMP': [
        'igmp', 'igmp snooping', 'igmpv2', 'igmpv3', 'multicast',
        'ip multicast', 'protocol independent multicast', 'pim',
        'ip multicast snooping', 'mld snooping', 'multicast listener discovery'
    ],
    'Реализация SNMP': [
        'snmp', 'snmpv1', 'snmpv2', 'snmpv3', 'rmon', 'xrmon',
        'management information base', 'mib', 'snmp manager',
        'snmp protocol operations', 'snmp transport mappings', 'snmp mib'
    ]
}


def parse_feature_in_datasheet(filepath, feature_name):
    """
    Поиск feature_name и его синонимов в datasheet.
    Выводит результат в консоль и возвращает True/False.
    """
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        normalized_text = normalize_text(text)

        # Получаем список синонимов или используем оригинальное имя
        variants = FEATURE_SYNONYMS.get(feature_name, [feature_name])
        normalized_variants = [normalize_text(v) for v in variants]

        for variant in normalized_variants:
            if variant in normalized_text:
                print(f"[parse_feature_in_datasheet] '{feature_name}' найдено как: '{variant}'")
                return True

        print(f"[parse_feature_in_datasheet] '{feature_name}' НЕ найдено. Проверены варианты: {normalized_variants}")
        return False

    except Exception as e:
        print(f"Ошибка парсера: {e}")
        return False





