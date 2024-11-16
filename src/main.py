import datetime
import os
import logging

import jwt
from aiohttp import web

from htmls import login_page_html, file_page_html
from settings import PORT, USERNAME, PASSWORD, SHARED_PATH, BASE_PATH, JWT_SECRET
from styles import login_page_styles, file_page_style

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


async def login_page(request):
    return web.Response(
        text=login_page_html.format(styles=login_page_styles, base_url=BASE_PATH),
        content_type="text/html",
    )


async def handle(request):
    logger.info("in handle")
    token = request.cookies.get("inspected")

    if not token:
        raise web.HTTPFound(location=f"{BASE_PATH}/login")

    try:
        jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        raise web.HTTPFound(location=f"{BASE_PATH}/login")

    path = request.match_info.get("path", "")
    full_path = os.path.join(SHARED_PATH, path)

    if os.path.isfile(full_path):
        # Отображение содержимого файла
        with open(full_path) as f:
            file_content = f.read()

        return web.Response(
            text=file_page_html.format(
                styles=file_page_style,
                file_name=os.path.basename(full_path),
                file_content=file_content,
                path=path,
                base_url=BASE_PATH,
            ),
            content_type="text/html",
        )
    elif os.path.isdir(full_path):
        # Возврат списка файлов и папок в директории с датой последнего обновления и размером
        items = sorted([f for f in os.listdir(full_path) if not f.startswith(".")])

        # Начало таблицы
        file_info = """
            <table>
                <thead>
                    <tr>
                        <th>Имя файла</th>
                        <th>Дата последнего обновления</th>
                        <th>Размер (байты)</th>
                    </tr>
                </thead>
                <tbody>
            """

        for item in items:
            item_path = os.path.join(full_path, item)
            last_modified = os.path.getmtime(item_path)
            size = os.path.getsize(item_path)

            # Форматирование даты
            last_modified_date = datetime.datetime.fromtimestamp(last_modified).strftime('%Y-%m-%d %H:%M:%S')
            file_info += f"""
                    <tr>
                        <td><a href="{BASE_PATH}/{os.path.join(path, item)}">{item}</a></td>
                        <td>{last_modified_date}</td>
                        <td>{size}</td>
                    </tr>
                """

        # Закрытие таблицы
        file_info += """
            </tbody>
        </table>
        """

        return web.Response(text=file_info, content_type="text/html")
    else:
        return web.Response(status=404, text="File or directory not found.")


async def handle_login(request):
    if request.method == 'POST':
        data = await request.post()
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        if username == USERNAME and password == PASSWORD:
            # Генерация JWT токена
            token = jwt.encode({
                'sub': username,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)
            }, JWT_SECRET, algorithm="HS256")

            response = web.HTTPFound(location=BASE_PATH)
            response.set_cookie('inspected', token, httponly=True)  # Установка cookie для авторизации
            return response
        else:
            return web.Response(text="Invalid credentials.", status=401)

    return await login_page(request)


async def download_file(request):
    path = request.match_info.get("path", "")
    full_path = os.path.join(SHARED_PATH, path)
    if os.path.isfile(full_path):
        return web.FileResponse(full_path)
    else:
        return web.Response(status=404, text="File not found.")


async def init_app():
    app = web.Application()
    app.router.add_get(f"{BASE_PATH}/login", login_page)  # Страница логина
    app.router.add_post(f"{BASE_PATH}/login", handle_login)  # Обработка логина
    app.router.add_get(f"{BASE_PATH}", handle)
    app.router.add_get(f"{BASE_PATH}/{{path:.*}}", handle)  # Обработка запросов на получение файлов и директорий
    app.router.add_get(f"{BASE_PATH}/download/{{path:.*}}", download_file)  # Обработка скачивания файлов
    return app


async def shutdown(app):
    logger.info("Shutting down the server...")
    await app.cleanup()


if __name__ == "__main__":
    logger.info("Starting server...")
    os.chdir(SHARED_PATH)

    app = init_app()
    web.run_app(app, port=PORT)
