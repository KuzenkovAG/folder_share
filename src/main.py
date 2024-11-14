import base64
import os
import logging

from aiohttp import web

from settings import PORT, USERNAME, PASSWORD, SHARED_PATH, BASE_PATH

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger()


async def handle(request):
    logger.info("in handle")
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return web.Response(status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

    # Проверка авторизации
    auth_type, encoded_credentials = auth_header.split(" ", 1)
    if auth_type.lower() != "basic":
        return web.Response(status=401, headers={"WWW-Authenticate": 'Basic realm="Login Required"'})

    credentials = base64.b64decode(encoded_credentials).decode("utf-8")
    username, password = credentials.split(":", 1)

    if username == USERNAME and password == PASSWORD:
        path = request.match_info.get("path", "")
        full_path = os.path.join(SHARED_PATH, path)

        if os.path.isfile(full_path):
            # Отображение содержимого файла
            with open(full_path) as f:
                file_content = f.read()
            return web.Response(
                text=f"""
                <html>
                <head>
                    <style id="monica-reading-highlight-style">
                        .monica-reading-highlight {{
                            animation: fadeInOut 1.5s ease-in-out;
                        }}

                        @keyframes fadeInOut {{
                            0%, 100% {{ background-color: transparent; }}
                            30%, 70% {{ background-color: rgba(2, 118, 255, 0.20); }}
                        }}

                        body {{
                            display: flex;
                            flex-direction: column;
                            min-height: 100vh;
                            margin: 0;
                        }}

                        .content {{
                            flex: 1;
                        }}

                        footer {{
                            background-color: #f1f1f1;
                            text-align: center;
                            padding: 10px;
                            position: fixed;
                            bottom: 0;
                            width: 100%;
                            display: flex;
                            justify-content: center;
                            gap: 20px; /* расстояние между кнопками */
                        }}

                        button {{
                            padding: 10px 20px;
                            font-size: 16px;
                        }}

                        a {{
                            text-decoration: none; /* убрать подчеркивание */
                        }}

                    </style>
                    </head>
                    <body>
                        <div class="content">
                            <h1>{os.path.basename(full_path)}</h1>
                            <pre>{file_content}</pre>
                        </div>
                        <footer>
                            <a href="{BASE_PATH}">
                                <button>В корневую директорию</button>
                            </a>
                            <br>
                            <a href="{BASE_PATH}/download/{path}" download>
                                <button>Скачать файл</button>
                            </a>
                        </footer>
                        <deepl-input-controller></deepl-input-controller>
                    </body>
                </html>
                """,
                content_type="text/html",
            )
        elif os.path.isdir(full_path):
            # Возврат списка файлов и папок в директории
            items = sorted([f for f in os.listdir(full_path) if not f.startswith(".")])
            file_links = [f'<a href="{BASE_PATH}/{os.path.join(path, item)}">{item}</a>' for item in items]
            return web.Response(text="<br>".join(file_links), content_type="text/html")
        else:
            return web.Response(status=404, text="File or directory not found.")
    else:
        return web.Response(status=401, text="Invalid credentials.")


async def download_file(request):
    path = request.match_info.get("path", "")
    full_path = os.path.join(SHARED_PATH, path)
    if os.path.isfile(full_path):
        return web.FileResponse(full_path)
    else:
        return web.Response(status=404, text="File not found.")


async def init_app():
    app = web.Application()
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
