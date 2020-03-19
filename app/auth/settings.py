SETTINGS = {
    'PASSWORD_LEN': (6, 30),
    'LOGIN_REDIRECT': 'index',
    'LOGOUT_REDIRECT': 'index',

    'BACK_URL_QS_KEY': 'index',
    'SESSION_USER_KEY': 'user',
    'REQUEST_USER_KEY': 'user',
}

MESSAGES = {
    'LOGGED_IN': 'Вы успешно авторизовались.',
    'LOGGED_OUT': 'Вы вышли из системы.',
    'ACTIVATED': 'Ваш аккаунт активирован.',
    'UNKNOWN_EMAIL': 'Данный адрес email не зарегистрирован.',
    'WRONG_PASSWORD': 'Пароль неверный.',
    'EMAIL_EXISTS': 'Данный адрес email уже зарегитрирован.',
    'PASSWORDS_NOT_MATCH': 'Пароли должны совпадать.',
    'AUTH_FAILED': 'Аутентификация завершилась неудачно',
}
