import requests
import xlrd


def print_menu(book):
    book = xlrd.open_workbook(book)
    sheet = book.sheet_by_index(0)
    priem_pishi, menu = [], ''
    ne_school = True
    problems = [42, '', None]
    try:
        for i in range(4, 25):
            if sheet.cell_value(i - 1, 0) == "Школа":
                ne_school = False
            if ne_school:
                if sheet.cell_value(i - 1, 0) not in problems:
                    priem_pishi.append(sheet.cell_value(i - 1, 0))
    except IndexError:
        pass
    i = 3
    for elem in priem_pishi:
        chto_dayt = ''
        if elem != priem_pishi[-1]:
            i += 1
            while sheet.cell_value(i, 0) != priem_pishi[priem_pishi.index(elem) + 1]:
                chto_dayt += f'{sheet.cell_value(i - 1, 3)} ({int(sheet.cell_value(i - 1, 4))} гр.)\n'
                i += 1
            chto_dayt += f'{sheet.cell_value(i - 1, 3)} ({int(sheet.cell_value(i - 1, 4))} гр.)\n'

        else:
            try:
                if i < 4:
                    i += 1
                while sheet.cell_value(i + 1, 3) not in problems and sheet.cell_value(i + 1, 0) != 'Школа':
                    chto_dayt += f'{sheet.cell_value(i, 3)} ({int(sheet.cell_value(i, 4))} гр.)\n'
                    i += 1
                chto_dayt += f'{sheet.cell_value(i, 3)} ({int(sheet.cell_value(i, 4))} гр.)\n'
            except IndexError:
                chto_dayt += f'{sheet.cell_value(i, 3)} ({int(sheet.cell_value(i, 4))} гр.)\n'
        menu += f'{elem}:\n{chto_dayt}\n'
    return menu


def give_menu(url=''):
    try:
        response = requests.get(url=url)
        with open("menu.xlsx", 'wb') as f:
            f.write(response.content)
    except:
        return 'Ё-моё, у нас проблемы'
