# © moonz


import time
import tools_qiwi


# import pdb
# pdb.set_trace()

def hello():
    print(r'''
               ::::    ::::   ::::::::   ::::::::  ::::    ::: ::::::::: 
               +:+:+: :+:+:+ :+:    :+: :+:    :+: :+:+:   :+:      :+:  
               +:+ +:+:+ +:+ +:+    +:+ +:+    +:+ :+:+:+  +:+     +:+   
               +#+  +:+  +#+ +#+    +:+ +#+    +:+ +#+ +:+ +#+    +#+    
               +#+       +#+ +#+    +#+ +#+    +#+ +#+  +#+#+#   +#+     
               #+#       #+# #+#    #+# #+#    #+# #+#   #+#+#  #+#      
               ###       ###  ########   ########  ###    #### ######### 
               ---------------------------------------------------------
                            для связи https://vk.com/moonzlo
                             или телега https://t.me/moonZlo
    ''')

    print('''
             Добро пожаловать в киви парсер. Для корректной работы программы 
    Вам необходим иметь токкен и номер телефона того аккаунта на который он был выдан.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!!                                                                            !!!
    !!!                   Если по какой-то причине у Вас нету токкена,             !!!
    !!!          его можно получить перейдя по этой ссылке https://qiwi.com/api    !!!
    !!!                                                                            !!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n''')


def menu():
    # Приветствие
    hello()
    tokken = input('Скопируйте и вставьте свой токкен, затем нажмите ввод (Enter) : ')

    phone = int(input('''
Скопируйте и вставьте номер телефона на который получен токкен
!!!ВАЖНО!!! Формат записи должен быть вида 79112223344
+'''))

    while True:

        print('''
        
        =============================================
        Все данные по умолчанию пишутся в csv формат!
        =============================================
        
        Выберите действие:
        
        1 - Выгрузить последние 50 транзакций 
        2 - Выгрузить историю транзакций за год
        3 - Выгрузить историю транзакций за конкретный период (в рамках одного года, с опциями)
        
        ----------------------------------------------------------------------------------------
        Примечание: qiwi api позволяет делать только 100 запросов в минуту, 
        поэтому если Вы собираетесь получить данные за год то придётся подождать 7 минут.
        ----------------------------------------------------------------------------------------
        ''')
        try:
            menu_global = int(input('Введите число и нажмите Enter : '))

            if menu_global == 1:
                print('''
                Выберите какой тип операция Вам необходимо выгрузить.
                
                1 - Полученные средства
                2 - Отправленные средства
                3 - Все
                0 - Назад
                ''')
                menu1 = int(input('Введите число: '))
                if menu1 == 0:
                    continue
                file_name = input('Введите название для csv файлй, он будет лежать в той же папки что и скрипт: ')
                if menu1 == 1:
                    value = tools_qiwi.last50('IN', phone, tokken)
                    tools_qiwi.write_csv2(value, file_name)

                elif menu1 == 2:
                    value = tools_qiwi.last50('OUT', phone, tokken)
                    tools_qiwi.write_csv2(value, file_name)

                elif menu1 == 3:
                    value = tools_qiwi.last50('ALL', phone, tokken)
                    tools_qiwi.write_csv2(value, file_name)

                else:
                    print('Такого пункта меню нет!')

            elif menu_global == 2:
                print('Весь процесс занимает 7 минут, по этому вводите год ПРАВИЛЬНО')
                data = int(input('Введите год: '))
                print('''
                Вы можете выбрать тип выгружаемых транзакций
                
                1 - Пополнение
                2 - Расход
                3 - Все
                0 - Назад
                ''')
                menu2 = int(input('Введите число: '))
                if menu2 == 0:
                    continue
                file_name = input('Введите имя файла с данными: ')
                print('Можете не беспокоится, программа работает. По завершению Вы будете возвращены в основное меню.')
                year = ['{}-01-01'.format(data), '{}-12-01'.format(data)]

                if menu2 == 1:
                    options = {'operation': 'IN'}
                    value = tools_qiwi.get_year(year, tokken, phone, options)
                    tools_qiwi.write_csv(value, file_name)

                elif menu2 == 2:
                    options = {'operation': 'OUT'}
                    value = tools_qiwi.get_year(year, tokken, phone, options)
                    tools_qiwi.write_csv(value, file_name)

                elif menu2 == 3:
                    options = {}
                    value = tools_qiwi.get_year(year, tokken, phone, options)
                    tools_qiwi.write_csv(value, file_name)

                else:
                    print('Такого пункта меню нет!')
                    time.sleep(1)

            elif menu_global == 3:

                def get_data(valuta='', type='ALL'):
                    '''Принимает на валюту и тип операции, выполняет инициацию сбора данных'''

                    year = int(input('Введите год: '))
                    strt_data = input('Введите месяц начала сбора: ')
                    stop_data = input('Введите месяц конца сбора: ')
                    file_name = input('Введите имя файла в который будут сохранены данные: ')

                    if int(strt_data) >= 1 and int(stop_data) <= 12:
                        data = ['{}-{}-01'.format(year, strt_data), '{}-{}-01'.format(year, stop_data)]

                        if valuta == '':
                            options = {'operation': type}

                        else:
                            options = {'operation': type,
                                       'sources': valuta, }

                        value = tools_qiwi.get_year(data, tokken, phone, options)
                        tools_qiwi.write_csv(value, file_name)
                        print('Данные успешно записаны в файл!')
                        time.sleep(2)

                print('''
                Данная опция поможет выгрузить данные в диапозоне месяцов, в рамках одного года.
                Все данные будут сохранены в csv файл, название которого Вы сможете задать далее.
                
                1 - Выгрузить диапазон (все типы транзакций - с выбором валюты)
                2 - Выгрузить диапазон (Пополнение - с выбором валюты)
                3 - Выгрузить диапазон (Расходы - с выбором валюты) 
                0 - Выйти в основное меню
                ''')
                menu3 = int(input('Введите число: '))
                if menu3 == 0:
                    continue

                elif menu3 == 1:
                    print('''
                    Выбире валюту:

                    1 - Рубли
                    2 - Доллары
                    3 - Евро
                    4 - Привязанные и непривязанные к кошельку банковские карты
                    5 - Счет мобильного оператора
                    6 - Все
                    ''')
                    vluta = int(input('Введите число: '))

                    if vluta == 6:
                        get_data()
                    elif vluta == 1:
                        get_data('QW_RUB', 'ALL')
                    elif vluta == 2:
                        get_data('QW_USD', 'ALL')
                    elif vluta == 3:
                        get_data('QW_EUR', 'ALL')
                    elif vluta == 4:
                        get_data('CARD', 'ALL')
                    elif vluta == 5:
                        get_data('MK', 'ALL')


                elif menu3 == 2:
                    print('''
                    Выбире валюту:

                    1 - Рубли
                    2 - Доллары
                    3 - Евро
                    4 - Привязанные и непривязанные к кошельку банковские карты
                    5 - Счет мобильного оператора
                    6 - Все
                    ''')
                    vluta = int(input('Введите число: '))

                    if vluta == 6:
                        get_data()
                    elif vluta == 1:
                        get_data('QW_RUB', 'IN')
                    elif vluta == 2:
                        get_data('QW_USD', 'IN')
                    elif vluta == 3:
                        get_data('QW_EUR', 'IN')
                    elif vluta == 4:
                        get_data('CARD', 'IN')
                    elif vluta == 5:
                        get_data('MK', 'IN')

                elif menu3 == 3:
                    print('''
                    Выбире валюту:

                    1 - Рубли
                    2 - Доллары
                    3 - Евро
                    4 - Привязанные и непривязанные к кошельку банковские карты
                    5 - Счет мобильного оператора
                    6 - Все
                    ''')
                    vluta = int(input('Введите число: '))

                    if vluta == 6:
                        get_data()
                    elif vluta == 1:
                        get_data('QW_RUB', 'OUT')
                    elif vluta == 2:
                        get_data('QW_USD', 'OUT')
                    elif vluta == 3:
                        get_data('QW_EUR', 'OUT')
                    elif vluta == 4:
                        get_data('CARD', 'OUT')
                    elif vluta == 5:
                        get_data('MK', 'OUT')

            else:
                print('Такого пункта меню нет!')
                time.sleep(1)

        except ValueError:
            print('СКОРЕЕ ВСЕГО ВАШ ТОККЕН НЕВЕРНЫЙ, ПЕРЕЗАПУСТИТЕ ПРОГРАММУ')
            time.sleep(2)
            continue


menu()
