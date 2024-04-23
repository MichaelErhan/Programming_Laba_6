from http.server import SimpleHTTPRequestHandler, HTTPServer
import os                                                               #Импорт необходимых библиотек


class MyHTTPServer(HTTPServer):                                         #Определение пользовательского HTTP-сервера
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)


class MyHandler(SimpleHTTPRequestHandler):                              #Определение пользовательского обработчика запросов
    def do_GET(self):                                                   #Обработка GET-запросов
        path = self.translate_path('index.html')                        #Получение пути к файлу 'index.html'
        if os.path.exists(path):                                        #Проверка существования файла
            with open(path, 'rb') as file:                              #Открытие файла для чтения в бинарном режиме
                content = file.read()                                   #Чтение содержимого файла
            self.send_response(200)                                     #Отправка успешного HTTP-ответа
            self.send_header('Content-type', 'text/html')
            self.send_header('Date', self.date_time_string())
            self.send_header('Server', 'MyHTTPServer')
            self.send_header('Content-length', str(len(content)))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(content)                                   #Отправка содержимого файла клиенту
        else:
            self.send_response(404)                                     #Отправка HTTP-ответа об ошибке 404
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"File not found")                         #Отправка сообщения об ошибке

    def translate_path(self, path):                                     #Перевод пути к файлу
        if not os.path.exists(path):                                    #Если файл не существует
            return 'index.html'                                         #Возвращает путь к файлу 'index.html'
        return super().translate_path(path)


with MyHTTPServer(('localhost', 80), MyHandler) as httpd:  #Создание экземпляра HTTP-сервера
    print('Сервер запущен на порту 80...')                              #Вывод сообщения о запуске сервера
    httpd.serve_forever()                                               #Запуск бесконечного цикла обработки запросов
