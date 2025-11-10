from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import re


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        full_name = query_params.get('full_name', [''])[0]  # Полное имя
        age = query_params.get('age', [''])[0]  # Получаем возраст
        height = query_params.get('height', [''])[0]  # Получаем рост

        # Валидация полного имени
        if not full_name or not re.match("^[a-zA-Za-яА-ЯёЁ\s\-]+$", full_name):
            message = "❌ Некорректное полное имя: должно содержать только буквы, пробелы и дефисы (латиница или кириллица)"
            status = 400
        else:
            # Валидация возраста
            try:
                age_int = int(age)
                if not 1 <= age_int <= 120:
                    message = "❌ Некорректный возраст: должен быть числом от 1 до 120"
                    status = 400
                else:
                    # Валидация роста
                    if not height:
                        message = "❌ Некорректный рост: не может быть пустым"
                        status = 400
                    elif not re.match("^[a-zA-Za-яА-ЯёЁ0-9\s\.\-]+$", height):
                        message = "❌ Некорректный рост: содержит недопустимые символы"
                        status = 400
                    else:
                        # Дополнительная проверка числового роста
                        if re.match("^\d+$", height.strip()):
                            height_int = int(height)
                            if not 50 <= height_int <= 250:
                                message = "❌ Некорректный числовой рост: должен быть от 50 до 250 см"
                                status = 400
                            else:
                                message = f"✅ Все данные валидны!<br>Полное имя: {full_name}<br>Возраст: {age_int} лет<br>Рост: {height}"
                                status = 200
                        else:
                            # Для текстового описания роста
                            message = f"✅ Все данные валидны!<br>Полное имя: {full_name}<br>Возраст: {age_int} лет<br>Рост: {height}"
                            status = 200
            except ValueError:
                message = "❌ Некорректный возраст: должен быть целым числом"
                status = 400

        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html_response = f"""
        <html>
            <head>
                <title>Результат валидации</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .success {{ color: green; font-size: 18px; }}
                    .error {{ color: red; font-size: 18px; }}
                    .info {{ margin-top: 20px; padding: 10px; background: #f5f5f5; }}
                    .block {{ margin: 10px 0; padding: 10px; border-left: 4px solid #007cba; }}
                </style>
            </head>
            <body>
                <h1>Результат проверки данных</h1>
                <div class="{'success' if status == 200 else 'error'}">{message}</div>
                <div class="info">
                    <strong>Проверяемые параметры:</strong>
                    <div class="block">
                        <strong>Основные данные:</strong><br>
                        Полное имя: {full_name}<br>
                        Возраст: {age}<br>
                        Рост: {height}
                    </div>
                </div>
                <div class="info">
                    <strong>Примеры валидных запросов:</strong>
                    <ul>
                        <li><a href="/?full_name=Артём Зимин&age=19&height=185">Артём Зимин 19 лет рост 185</a></li>
                        <li><a href="/?full_name=Елкина Диана&age=19&height=170">Елкина Диана 19 лет рост 170</a></li>
                        <li><a href="/?full_name=Шабалов Артём Михайлович&age=25&height=176">Шабалов Артём Михайлович рост 176</a></li>
                        <li><a href="/?full_name=Вячеслав Морская Пехота&age=30&height=3 километра">Вячеслав Морская Пехота рост 3 километра</a></li>
                        <li><a href="/?full_name=Исаева Влада Евгеньевна&age=22&height=метр с кепкой">Исаева Влада Евгеньевна рост метр с кепкой</a></li>
                    </ul>
                </div>
            </body>
        </html>
        """
        self.wfile.write(bytes(html_response, "utf-8"))


# Функция для тестирования валидации
def test_data(full_name, age, height):
    """Тестирует валидацию данных без запуска сервера"""
    # Валидация полного имени
    if not full_name or not re.match("^[a-zA-Za-яА-ЯёЁ\s\-]+$", full_name):
        return "❌ Некорректное полное имя"
    
    # Валидация возраста
    try:
        age_int = int(age)
        if not 1 <= age_int <= 120:
            return "❌ Некорректный возраст"
    except ValueError:
        return "❌ Некорректный возраст"
    
    # Валидация роста
    if not height:
        return "❌ Некорректный рост"
    elif not re.match("^[a-zA-Za-яА-ЯёЁ0-9\s\.\-]+$", height):
        return "❌ Некорректный рост"
    
    # Дополнительная проверка числового роста
    if re.match("^\d+$", height.strip()):
        height_int = int(height)
        if not 50 <= height_int <= 250:
            return "❌ Некорректный числовой рост"
    
    return f"✅ Все данные валидны: {full_name}, {age} лет, рост {height}"


if __name__ == "__main__":
    # Тестирование валидации
    print("=== ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ===")
    test_cases = [
        ("Артём Зимин", "19", "185"),
        ("Елкина Диана", "19", "170"),
        ("Шабалов Артём Михайлович", "25", "176"),
        ("Вячеслав Морская Пехота", "30", "3 километра"),
        ("Исаева Влада Евгеньевна", "22", "метр с кепкой"),
        ("Анна-Мария", "28", "165"),  # имя с дефисом
        ("John Smith", "35", "180"),  # имя на латинице
        ("Петр", "150", "175"),  # ошибка: возраст вне диапазона
        ("", "25", "180"),  # ошибка: пустое имя
        ("Иван123", "25", "180"),  # ошибка: цифры в имени
        ("Мария", "25", ""),  # ошибка: пустой рост
        ("Олег", "abc", "175"),  # ошибка: не число в возрасте
        ("Сергей", "25", "45"),  # ошибка: рост слишком маленький
        ("Дмитрий", "25", "300"),  # ошибка: рост слишком большой
    ]

    for full_name, age, height in test_cases:
        result = test_data(full_name, age, height)
        print(f"Тест: {full_name}, {age} лет, рост {height} -> {result}")

    # Запуск сервера
    print("\n=== ЗАПУСК СЕРВЕРА ===")
    port = 8000
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Сервер запущен на порту {port}')
    print(f'Для тестирования перейдите по адресу: http://localhost:{port}/?full_name=Артём Зимин&age=19&height=185')
    print('Для остановки сервера нажмите Ctrl+C')

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")