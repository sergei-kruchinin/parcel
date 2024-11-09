"""
Модуль: debug_run.py

Запускает app вне докер контейнера.
Контейнер app должен быть остановлен.
Контейнер с mysql должен быть запущен.

"""

from dotenv import load_dotenv
import uvicorn


load_dotenv()

if __name__ == "__main__":

    uvicorn.run("src.app:app", host="127.0.0.1", port=8000, reload=True)