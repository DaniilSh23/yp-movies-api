import requests


def make_request_session():
    """
    Функция с логикой создания сессии для запроса.
    """
    # Путь к файлу с SSL серификатом
    ca_cert_path = "http_ca.crt"
    # Создаем объект сессии
    session = requests.Session()
    # Устанавливаем путь к CA-сертификату
    session.verify = ca_cert_path
    # Подготавливаем HTTP-аутентификацию
    return session
