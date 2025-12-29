import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


# Функция для получения данных за прошлую неделю
def get_currency_data():
    dates_list = []
    rates_list = []

    print("Fetching data from NBU API...")

    # Собираем данные за последние 7 дней
    for i in range(7, -1, -1):
        # Вычисляем дату
        target_date = datetime.now() - timedelta(days=i)
        formatted_date = target_date.strftime('%Y%m%d')

        # Ссылка на API НБУ
        url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={formatted_date}&json"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Добавляем дату (день.месяц) и курс в списки
                    dates_list.append(target_date.strftime('%d.%m'))
                    rates_list.append(data[0]['rate'])
                    print(f"Done: {target_date.strftime('%Y-%m-%d')} -> {data[0]['rate']} UAH")
        except Exception as e:
            print(f"Error on {formatted_date}: {e}")

    return dates_list, rates_list


# Функция для отрисовки графика
def show_plot(dates, rates):
    # Настройки графика (Задание 3)
    plt.figure(figsize=(10, 5))
    plt.plot(dates, rates, marker='o', color='tab:blue', label='USD Rate')

    plt.title('USD Exchange Rate (Last 7 Days)')
    plt.xlabel('Date')
    plt.ylabel('Rate (UAH)')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Показать результат
    plt.show()


if __name__ == "__main__":
    # Запускаем сбор и отрисовку
    days, prices = get_currency_data()
    if days:
        show_plot(days, prices)