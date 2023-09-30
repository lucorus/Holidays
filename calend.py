import random
import bs4
import requests


# парсим праздники
def parse_holidays():
    response = requests.get('https://my-calend.ru/holidays').text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    data = soup.find('section')
    return data


# убирает все английские слова и лишние символы из текста
def no_eng(text):
    answer = ''
    for item in text:
        if item not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'\
                and item not in '+-*/<>=[]":.,(){}1234567890__!' \
                and item not in "'" and item not in ' ':
            answer += item
    return answer


# удаляем лишнее
def delete_excess_space(holidays: list) -> list:
    holidays = no_eng(str(holidays))
    # обрезаем лишний текст + лишние пробелы в начале и конце
    holidays = holidays[20:-2]
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

    # убираем категорию праздника
    arr.remove('Профессиональный праздник')
    arr.remove('Народный праздник')

    return arr


if __name__ == '__main__':
    congratulation = delete_excess_space(list(parse_holidays()))

    file = open(f'file{ random.randint(0, 100) }.txt', 'a')
    congratulation = 'Приветствую всех, а так же хочу поздравить вас с такими ЧУДЕСНЫМИ праздниками, как:' + ', '.join(congratulation) + '!!!'
    file.write(congratulation)
    file.close()


