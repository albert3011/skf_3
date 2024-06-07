import re
import requests

help_hello_mess = ('Приветствуем вас в телеграм-боте, который предназначен для конвертации валют!\n'
                   'Для того, чтобы узнать курс одной валюты к другой, необходимо отправить сообщение'
                   ' следующего вида:\n'
                   '25 RUB USD\n'
                   'где 25 RUB - это кол-во валюты, которую вы хотите конвертировать, а '
                   'USD - это валюта, в которую вы хотите произвести конвертацию.\n'
                   'Для того, чтобы узнать информацию о всех доступных валютах, необходимо'
                   'воспользоваться командой /values')


class APIException(Exception):
    pass


def create_db():
    val_dict = {}

    r = requests.get('https://www.cbr-xml-daily.ru/daily_utf8.xml')
    content = r.content.decode('utf-8')

    char_code = re.findall('<CharCode[^/]*', content)
    value_list = re.findall('<VunitRate[^/]*', content)

    for i in range(len(char_code)):
        val_dict[char_code[i].replace('<CharCode>', '').replace('<', '')] = float(
            value_list[i].replace('<VunitRate>', '').replace('<', '').replace(',', '.'))
    return val_dict


class Transform:
    @staticmethod
    def get_price(amount, from_val, to_val):
        val_dict = create_db()
        if from_val != 'RUB':
            try:
                if from_val not in val_dict:
                    raise APIException(f'Не найдена валюта {from_val}.')
            except APIException as e:
                return e
        if to_val != 'RUB':
            try:
                if to_val not in val_dict:
                    raise APIException(f'Не найдена валюта {to_val}.')
            except APIException as e:
                return e
        if to_val == 'RUB':
            result = amount*val_dict[from_val]
        elif from_val == 'RUB':
            result = amount/val_dict[to_val]
        else:
            result = amount * (val_dict[from_val] / val_dict[to_val])
        result = round(result, 2)
        return f'{amount} {from_val} = {result} {to_val}'


def check_message(message):
    spaces = re.split(' ', message)
    try:
        if len(spaces) != 3:
            raise APIException('Неверный формат ввода. Необходимо ввести число и две валюты.')
    except APIException as e:
        return e
    try:
        num = float(spaces[0].replace(',', '.'))
    except ValueError:
        return f'{spaces[0]} не является числом.'
    if spaces[1] == spaces[2]:
        try:
            raise APIException('Введите две разные валюты.')
        except APIException as e:
            return e
    return Transform.get_price(num, spaces[1].upper(), spaces[2].upper())


def create_values(val_dict):
    result = ''
    for val in val_dict:
        result = result + f'1 {val} = {val_dict[val]} RUB\n'
    return result
