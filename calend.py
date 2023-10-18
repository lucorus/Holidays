import datetime
import random
import time
import bs4
import requests
from catolic_celebration import today_christian_holidays
from birth import today_birthday_man
start = time.time()


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
def delete_excess_symbols(holidays: list) -> list:
    holidays = no_eng(str(holidays))
    # обрезаем лишний текст + лишние пробелы в начале и конце
    holidays = holidays[20:]
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


if __name__ == '__main__':
    congratulation = delete_excess_symbols(list(parse_holidays()))
    christian_congratulation = today_christian_holidays()
    data = datetime.datetime.now()
    file = open(f'поздравления/{data.day}-{data.month}-{data.year}file{ random.randint(0, 100) }.txt', 'a')

    file.write('Приветствую всех, а так же хочу поздравить вас с такими ЧУДЕСНЫМИ праздниками, как: ' + \
               ', '.join(congratulation + christian_congratulation))

    file.write('\nПриветствую всех, а так же хочу поздравить вас с такими ЧУДЕСНЫМИ праздниками, как: ' + \
                     ', '.join(congratulation + christian_congratulation) + '. А так же сегодня родились такие ВЫДАЮЩИЕСЯ личности, как: ' + \
                     ', '.join(today_birthday_man()))

    file.write('\nхай! знаешь, у меня такое ПРЕКРАСНОЕ настроение! думаю, что стоит поздравить тебя с такими ЧУДЕСНЫМИ праздниками, как: ' + \
                     ', '.join(congratulation + christian_congratulation) + '. А так же сегодня родились такие ВЫДАЮЩИЕСЯ личности, как: ' + \
                     ', '.join(today_birthday_man()))
    file.write('\n!!!')
    file.close()

    print('Время выполнения: ', time.time() - start)

