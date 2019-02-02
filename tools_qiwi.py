import json, csv, calendar, time, requests


def sending_to_api(phone, token, setting):
    '''Суть данной функции сформировать заголовок запроса к API, и вернуть json с ответом'''
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + token
    h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + str(phone) + '/payments', params=setting)
    return json.loads(h.text)


def get_month_days(data):
    '''Принимает даут в формате ГГГГ-ММ-ДД, отдает количество дней в месяце'''

    value = data.split('-')
    y = int(value[0])
    m = int(value[1])
    days = calendar.monthrange(y, m)
    return days[1]


def format_data(start_data, stop_data):
    '''Принимает на вход дату начала и конца выгрузки в форме ГГГГ-ММ-ДД'''

    sorted_list = []

    start = start_data.split('-')
    stop = stop_data.split('-')

    iter_data = start_data.split('-')
    firs = int(iter_data[1])
    iter_data[1] = str(firs)

    nums = int(start[1])

    for i in range(int(start[1]), int(stop[1]) + 1):  # Число итераций равно промежутку от первого месяца до последнего.
        data = '-'.join(iter_data)
        days = get_month_days(data)

        iter_data[2] = str(days)
        data2 = '-'.join(iter_data)
        sorted_list.append(data2)
        iter_data[1] = str(nums + 1)
        nums += 1

    return sorted_list  # Возвращает список с датами


def get_value(data, token, phone, seting):
    '''Принимаемет список из дат, токкен, телефон и настройки. Отдаёт список словарей'''
    api_access_token = str(token)  # токен можно получить здесь https://qiwi.com/api
    my_login = str(phone)  # номер QIWI Кошелька в формате 79991112233 (БЕЗ знака плюс)
    s = requests.Session()
    strt = data.split('-')
    data = []
    month = strt[1]
    if int(month) < 10:
        strt[1] = '0{}'.format(month)

    max_day = int(strt[2])
    day = int(2)
    day_one = int(1)
    while day <= max_day:

        iter_day = '01'
        start_day = ''

        if int(day) < 10:
            iter_day = '0{}'.format(day)
        elif int(day) > 9:
            iter_day = str(day)
        if int(day_one) < 10:
            start_day = '0{}'.format(day_one)
        elif int(day_one) > 9:
            start_day = str(day_one)

        # Заголовок POST запроса.
        s.headers['authorization'] = 'Bearer ' + api_access_token

        s_data = '{}-{}-{}T00:00:00Z'.format(strt[0], strt[1], start_day)
        d_data = '{}-{}-{}T00:00:00Z'.format(strt[0], strt[1], iter_day)
        day += 1
        day_one += 1

        # такая запись выгружает все валюты, и типы запросов.
        parameters = {'startDate': s_data,
                      'endDate': d_data,
                      'rows': 50}

        parameters.update(seting)  # Добавляем настройки если требуется.

        h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + my_login + '/payments', params=parameters)
        time.sleep(1)  # Задержка между запросами в 1у секунду. Лимит api qiwi 100 запросов в минуту.
        value = json.loads(h.text)

        # Проверям если данные не пусты, то добавляем.
        if len(value.get('data')) > 0:
            data.append(value)

    return data


def last50(option, phone, tokken):
    '''Вызывает выгрузку данныйх последнй 50 транзакций с опциями,
    в качестве опций возможность выбора типа транзакии'''

    if option == 'IN':  # Пополенине
        options = {'operation': 'IN',
                   'rows': 50}  # Количество операций
        value = sending_to_api(phone, tokken, options)
        return value

    elif option == 'OUT':  # Расходы
        options = {'operation': 'OUT',  # Тип транзакции
                   'rows': 50}  # Количество операций
        value = sending_to_api(phone, tokken, options)
        return value

    elif option == 'ALL':
        options = {'rows': 50}
        value = sending_to_api(phone, tokken, options)
        return value


def get_year(data, token, phone, seting):
    '''Данная функция служит для выдачи данных за год'''
    start = data[0]  # ['2016-01-01', '2017-12-01']
    stop = data[1]
    value = []

    spsok = format_data(start, stop)

    for i in spsok:
        print('Начал парсить', i)
        a = get_value(i, token, phone, seting)  # Инциируем зауск парсера.
        value.append(a)

    return value


def write_csv(value, name):
    '''Запись упорядоченных данных в csv файл'''
    with open('{}.csv'.format(name), "w", encoding='cp1251', newline="") as file:
        columns = ["Дата транзакции", "Типа транзакции", "Статус", "Значение", "Комиссия", "Сумма", "Код валюты",
                   "Краткое наименование", "Полное название", "Комментарий", "Логотип компании", "URL"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for _ in value:
            for i in _:
                for x in i.get('data'):
                    user = {'Дата транзакции': x.get('date'),
                            'Типа транзакции': x.get('type'),
                            'Статус': x.get('status'),
                            'Значение': x.get('sum').get('amount'),
                            'Комиссия': x.get('commission').get('amount'),
                            'Сумма': x.get('total').get('amount'),
                            'Код валюты': x.get('sum').get('currency'),
                            'Краткое наименование': x.get('provider').get('shortName'),
                            'Полное название': x.get('provider').get('longName'),
                            'Комментарий': x.get('comment'),
                            'Логотип компании': x.get('provider').get('logoUrl'),
                            'URL': x.get('provider').get('siteUrl')}
                    writer.writerow(user)


def write_csv2(value, name):
    '''Запись упорядоченных данных в csv файл'''
    with open('{}.csv'.format(name), "w", encoding='cp1251', newline="") as file:
        columns = ["Дата транзакции", "Типа транзакции", "Статус", "Значение", "Комиссия", "Сумма", "Код валюты",
                   "Краткое наименование", "Полное название", "Комментарий", "Логотип компании", "URL"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()

        for i in value.get('data'):
            user = {'Дата транзакции': i.get('date'),
                    'Типа транзакции': i.get('type'),
                    'Статус': i.get('status'),
                    'Значение': i.get('sum').get('amount'),
                    'Комиссия': i.get('commission').get('amount'),
                    'Сумма': i.get('total').get('amount'),
                    'Код валюты': i.get('sum').get('currency'),
                    'Краткое наименование': i.get('provider').get('shortName'),
                    'Полное название': i.get('provider').get('longName'),
                    'Комментарий': i.get('comment'),
                    'Логотип компании': i.get('provider').get('logoUrl'),
                    'URL': i.get('provider').get('siteUrl')}
            writer.writerow(user)


def write_json(value):
    '''Запись данных в json файл'''
    with open('transaction.json', 'w') as file:
        json.dump(value, file, indent=1, ensure_ascii=False)
