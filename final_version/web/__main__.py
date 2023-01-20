"""
Запуск сервера

Запускать через `python3 -m web` в папке проекта
"""

from . import app

app.run(host='0.0.0.0', debug=True)
