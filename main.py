from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt

page = requests.get('https://ruz.spbstu.ru/')
print("Успешное подключение к серверу\n") if page.status_code == 200 else print("Не удалось подключиться к серверу")

group = input("Введите номер группы -> ")
date = input("Введите дату (дд.мм.гггг) -> ")

request = requests.get(f'https://ruz.spbstu.ru/search/groups?q={group}')
soup = BeautifulSoup(request.text, "html.parser")
findGroups = soup.findAll('a', class_='groups-list__link')

data_url = date.split(".")
date = data_url[2] + "-" + data_url[1] + "-" + data_url[0]

for url in findGroups:
    href = url['href']
    id = href.split('/')[-1]

month = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
request = requests.get(f'https://ruz.spbstu.ru/api/v1/ruz/scheduler/{id}?date={date}')
schedule = request.json()
#print(schedule)

print("\nРасписание с",  schedule['week']['date_start'].split('.')[2], month[(int)(schedule['week']['date_start'].split('.')[1]) - 1] , "по", schedule['week']['date_end'].split('.')[2], month[(int)(schedule['week']['date_start'].split('.')[1]) - 1] , "(нечётная неделя)" if schedule['week']['is_odd'] else "(чётная неделя)")
classes_per_day = {day: 0 for day in ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]}

for day in schedule['days']:
    print(day['date'].split('-')[2], month[(int)(day['date'].split('-')[1]) - 1], days[day['weekday'] - 1], end=".,\n")
    classes_per_day[days[day['weekday'] - 1]] += len(day['lessons'])

    for lessons in day['lessons']:
        print("\t", lessons['time_start'], "-", lessons['time_end'], lessons['subject'], "\n\t\t\t", lessons['typeObj']['name'], "\n\t\t\t", lessons['additional_info'] if lessons['additional_info'] else lessons['groups'][0]['name'] )
        if lessons['teachers']:
            for teacher in lessons['teachers']:
                print("\t\t\t", teacher['full_name'])
        else: print("\t\t\t Преподаватель не указан")
        print("\t\t\t", lessons['auditories'][0]['building']['name'],", ауд.", lessons['auditories'][0]['name'],"\n")
days = list(classes_per_day.keys())
classes_counts = list(classes_per_day.values())

plt.figure(figsize=(10, 6))
plt.bar(days, classes_counts, color='skyblue')
plt.xlabel('День недели')
plt.ylabel('Количество занятий')
plt.title('Количество занятий по дням недели')
plt.show()
