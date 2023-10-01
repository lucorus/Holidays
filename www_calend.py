import datetime
import random
import time
import bs4
import requests
start = time.time()


# парсим праздники
def parse_holidays():
    response = requests.get('https://www.calend.ru/').text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    #data = soup.find('section')
    #data = soup.find('li', {'class': 'one_three'})
    data = soup.find_all('span', {'class': 'title'})
    return data


def parse_trash():
    response = requests.get('https://www.calend.ru/').text
    soup = bs4.BeautifulSoup(response, 'html.parser')
    data = soup.find_all('div', {'class': 'hinted'})
    return data


# убирает все английские слова и лишние символы из текста
def no_eng(text):
    answer = ''
    for item in text:
        if item not in 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'\
                and item not in '+-*/<>=[]":.,(){}1234567890_!' \
                and item not in "'" and item not in ' ':
            answer += item
    return answer


# удаляем лишнее
def delete_excess_symbols(holidays: list, delete_trash=True) -> list:
    holidays = no_eng(str(holidays))
    # обрезаем лишний текст + лишние пробелы в начале и конце
    # если нужно удалить мусор, то удаляем
    if delete_trash:
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
    try:
        while arr.count('Профессиональный праздник') > 0:
            arr.remove('Профессиональный праздник')
    except:
        pass

    try:
        while arr.count('Народный праздник') > 0:
            arr.remove('Народный праздник')
    except:
        pass

    return arr


# удаляем мусор из праздников
def delete_trash(holidays: list, trash: list):
    for item in trash:
        for holiday in range(len(holidays)):
            if item == holidays[holiday]:
                holidays[holiday] = 1

    try:
        while holidays.count(1) > 0:
            holidays.remove(1)
    except:
        pass

    return holidays


if __name__ == '__main__':
    congratulation = delete_excess_symbols(list(parse_holidays()))
    trash = delete_excess_symbols(list(parse_trash()), False)
    congratulation = delete_trash(congratulation, trash)
    data = datetime.datetime.now()

    congratulation = congratulation[27:-42]
    congratulation = 'Приветствую всех, а так же хочу поздравить вас с такими ЧУДЕСНЫМИ праздниками, как: ' + ', '.join(congratulation) + '!!!'
    file = open(f'celebration/{data.day}-{data.month}-{data.year}file{ random.randint(0, 100) }.txt', 'a')
    file.write(congratulation)
    file.close()
    print(congratulation)
    print('Время выполнения: ', time.time() - start)

