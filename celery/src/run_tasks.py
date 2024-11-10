"""
Модуль: run_tasks

Разовый запуск задач.

Использование:
    Для обновления курса:
    docker exec parcel_celery python run_tasks.py --update-exchange-rate

    Для пересчета стоимости доставки:
    docker exec parcel_celery python run_tasks.py --update-shipping-costs
"""

import sys
from tasks import update_exchange_rate, update_shipping_costs


def main():
    if len(sys.argv) < 2:
        print("Пожалуйста, укажите задачу для выполнения.")
        return

    task = sys.argv[1]

    if task == "--update-exchange-rate":
        update_exchange_rate.apply_async()
        print("Обновление курса валют запущено.")
    elif task == "--update-shipping-costs":
        update_shipping_costs.apply_async()
        print("Пересчет стоимости доставки запущен.")
    else:
        print("Неизвестная задача. Используйте --update-exchange-rate или --update-shipping-costs.")


if __name__ == "__main__":
    main()