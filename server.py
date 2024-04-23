from http.server import SimpleHTTPRequestHandler, HTTPServer
import os  # Импорт необходимых библиотек


class MyHTTPServer(HTTPServer):  # Определение пользовательского HTTP-сервера
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)


class MyHandler(SimpleHTTPRequestHandler):  # Определение пользовательского обработчика запросов
    def do_GET(self):  # Обработка GET-запросов
        path = self.translate_path('index.html')  # Получение пути к файлу 'index.html'
        with open(path, 'rb') as file:  # Открытие файла для чтения в бинарном режиме
            content = file.read()  # Чтение содержимого файла
            self.send_response(200)  # Отправка успешного HTTP-ответа
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)  # Отправка содержимого файла клиенту

    def translate_path(self, path):  # Перевод пути к файлу
        if not os.path.exists(path):  # Если файл не существует
            return 'index.html'  # Возвращает путь к файлу 'index.html'
        return super().translate_path(path)


with MyHTTPServer(('localhost', 80), MyHandler) as httpd:  # Создание экземпляра HTTP-сервера
    print('Сервер запущен на порту 80...')  # Вывод сообщения о запуске сервера
    httpd.serve_forever()  # Запуск бесконечного цикла обработки запросов
