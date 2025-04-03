import json
import urllib.request
from urllib.error import HTTPError, URLError


def exchange_rate_app(environ, start_response):
    # Получаем путь запроса (например, '/USD')
    path = environ.get("PATH_INFO", "").strip("/")

    if not path or len(path) != 3:
        # Неправильный запрос - возвращаем 400
        status = "400 Bad Request"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [b"Invalid currency code. Use 3-letter code like /USD"]

    currency = path.upper()
    api_url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    try:
        # Делаем запрос к внешнему API
        with urllib.request.urlopen(api_url) as response:
            data = response.read()
            # Проверяем, что ответ JSON
            json.loads(data)

            # Возвращаем успешный ответ
            status = "200 OK"
            headers = [
                ("Content-type", "application/json"),
                ("Content-length", str(len(data))),
            ]
            start_response(status, headers)
            return [data]

    except HTTPError as e:
        # Ошибка от API
        status = f"{e.code} {e.reason}"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [f"API error: {e.reason}".encode("utf-8")]

    except URLError:
        # Проблемы с соединением
        status = "502 Bad Gateway"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [b"Failed to connect to exchange rate API"]

    except json.JSONDecodeError:
        # Невалидный JSON в ответе
        status = "502 Bad Gateway"
        headers = [("Content-type", "text/plain")]
        start_response(status, headers)
        return [b"Invalid response from exchange rate API"]


if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    with make_server("", 8000, exchange_rate_app) as httpd:
        print("Serving on port 8000...")
        httpd.serve_forever()
