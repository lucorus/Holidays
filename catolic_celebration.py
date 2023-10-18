import bs4
import requests


def parse_christian_holidays():
    response = requests.get('https://my-calend.ru/holidays').text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    data = soup.find('details')
    return data


def no_eng(text):
    answer = ''
    for item in text:
        if item not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'\
                and item not in '+-*/<>=[]":.,(){}1234567890__!' \
                and item not in "'" and item not in ' ':
            answer += item
    return answer


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

    # обрезаем лишнее
    arr = arr[1:]

    return arr


# возвращает список христианских праздников сегодня
def today_christian_holidays():
    return delete_excess_symbols((list(parse_christian_holidays())))
