login_page_styles = """
html {
    background-color: #214c84;
    background-blend-mode: overlay;
    display: flex;
    align-items: center;
    justify-content: center;
    background-image: url(../../assets/img/image4.jpg);
    background-repeat: no-repeat;
    background-size: cover;
    height: 100%;
}

body {
    background-color: transparent;
}

.registration-cssave {
    padding: 50px 0;
}

.registration-cssave form {
    max-width: 800px;
    padding: 50px 70px;
    border-radius: 10px;
    box-shadow: 4px 4px 15px rgba(0, 0, 0, 0.2);
    background-color: #fff;
}

.registration-cssave form h3 {
    font-weight: bold;
    margin-bottom: 30px;
}

.registration-cssave .item {
    border-radius: 10px;
    margin-bottom: 25px;
    padding: 10px 20px;
}

.registration-cssave .create-account {
    border-radius: 30px;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
    background-color: #3f93ff;
    border: none;
    color: white;
    margin-top: 20px;
}

@media (max-width: 576px) {
    .registration-cssave form {
        padding: 50px 20px;
    }
}
"""

file_page_style = """
.monica-reading-highlight {
    animation: fadeInOut 1.5s ease-in-out;
}

@keyframes fadeInOut {
    0%, 100% { background-color: transparent; }
    30%, 70% { background-color: rgba(2, 118, 255, 0.20); }
}

body {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0;
}

.content {
    flex: 1;
}

footer {
    background-color: #f1f1f1;
    text-align: center;
    padding: 10px;
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    gap: 20px; /* расстояние между кнопками */
}

button {
    padding: 10px 20px;
    font-size: 16px;
}

a {
    text-decoration: none; /* убрать подчеркивание */
}
"""