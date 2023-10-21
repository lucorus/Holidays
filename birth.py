import time
import bs4
import requests
start = time.time()


# парсим именинников
def parse_birthday_man():
    response = requests.get('https://celebers.com/birthday/').text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    data = soup.find_all('span', {'class': 'name'})
    return data


def no_eng(text):
    answer = ''
    for item in text:
        if item not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'\
                and item not in '+-*/<>=[]":;.,(){}1234567890__!' \
                and item not in "'" and item not in ' ':
            answer += item
    return answer


# удаляем лишнее
def delete_excess_symbols(holidays: list) -> list:
    holidays = no_eng(str(holidays))
    # обрезаем лишний текст + лишние пробелы в начале и конце
    holidays = holidays.strip()

    holi = ''
    arr = []
    # удаляем лишние пробелы между словами
    for item in range(len(holidays)):
        if holidays[item] != ' ':
            holi += holidays[item]
        elif holidays[item + 1] != ' ' and holi != '':
            holi += holidays[item]
        elif holi != '':
            arr.append(holi)
            holi = ''

    return arr


# возвращает список именинников
def today_birthday_man():
    birth = delete_excess_symbols((list(parse_birthday_man())))
    return birth

