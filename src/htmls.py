login_page_html = """
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Страница Логина</title>
    <style>
        {styles}
    </style>
</head>
<body>
    <div class="registration-cssave">
        <form method="post" action="{base_url}/login">
            <h3>Вход в аккаунт</h3>
            <div class="item">
                <input type="text" id="username" name="username" placeholder="Логин" required><br>
            </div>
            <div class="item">
                <input type="password" id="password" name="password" placeholder="Пароль" required>
            </div>
            <input type="submit" class="create-account" value="Войти">
        </form>
    </div>
</body>
</html>
"""

file_page_html = """
<html>
<head>
    <style>
        {styles}
    </style>
    </head>
    <body>
        <div class="content">
            <h1>{file_name}</h1>
            <pre>{file_content}</pre>
        </div>
        <footer>
            <a href="{base_url}">
                <button>В корневую директорию</button>
            </a>
            <br>
            <a href="{base_url}/download/{path}" download>
                <button>Скачать файл</button>
            </a>
        </footer>
        <deepl-input-controller></deepl-input-controller>
    </body>
</html>
"""
