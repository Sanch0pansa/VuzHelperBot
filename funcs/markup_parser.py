from jinja2 import Template
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def prepare_markup(rows):
    markup = InlineKeyboardMarkup(row_width=8)
    for row in rows:
        buttons = []
        for button in row:
            buttons.append(InlineKeyboardButton(**button))
        markup.add(*buttons)

    return markup


def get_markup(filename, data=dict()):
    try:
        f = open(filename, encoding="utf-8")
        template = Template(f.read())
        text = template.render(**data)
        return text
    except Exception as e:
        return "<msg>Упс :( </msg>"


def parse_markup(text):
    message = {
        'text': "Message text here",
        'parse_mode': "html"
    }

    soup = BeautifulSoup(text, 'xml')

    # Получение текста сообщения
    msg = soup.find('msg')
    if msg:
        # message['text'] = str(msg).replace("<msg>", "", 1).replace("</msg>", "")
        message['text'] = msg.encode_contents()

    # Получение разметки клавиатуры
    markup = soup.find('markup')
    if markup:
        rows_els = markup.find_all('row')
        rows = []
        for row_el in rows_els:
            row = []
            for btn_el in row_el.find_all('button'):
                button = {
                    'text': btn_el.text
                }

                if btn_el.get('ev'):
                    button['callback_data'] = btn_el.get('ev')

                if btn_el.get('url'):
                    button['callback_data'] = btn_el.get('url')

                row.append(button)

            rows.append(row)

        message['reply_markup'] = prepare_markup(rows)
    return message


def view(template, data):
    return parse_markup(get_markup(template, data))