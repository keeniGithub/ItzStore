import telebot
from telebot import types
from tokenbot import token
from pypayment import PayOkPayment, PayOkPaymentType, PaymentStatus, PayOkCurrency
import sqlite3 as sql3
from time import sleep as delay
from datetime import date
from datetime import datetime
from random import randint


bot = telebot.TeleBot(token)

db = sql3.connect('base.db')
sql = db.cursor()
markup = None

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id TEXT,
    status TEXT,
    balance BIGINT,
    total_buy BIGINT,
    spent_money BIGINT
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS product (
            check_id TEXT,
            user_id BIGINT,
            product TEXT,
            sum BIGINT
)
""")

sql.execute("""CREATE TABLE IF NOT EXISTS promo_codes (
            name TEXT,
            amount BIGINT,
            sum BIGINT
)
""")
db.commit()

@bot.message_handler(commands=['start'])
def start(message):        
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = message.chat.id

    sql.execute(f"SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (user_id, 'user', 0, 0, 0)) 
        db.commit()
    sql.execute(f"SELECT status FROM users WHERE user_id = ?", (user_id,))
    user_status = sql.fetchone()
    print(user_status)

    if user_status[0] == 'blocked':
        bot.send_message(message.chat.id, f"⛔Ваш аккаунт заблокирован!\nВам закрыт доступ к магазину с аккаунта <b>{user_id}</b>\n \n📞Если ваш аккаунт не является аккаунтом <b>1683841862</b> вы можете написать в тех. поддержку для разблокировки", parse_mode="html")

    if user_status[0] == 'user' or user_status[0] == 'admin':
            print("user")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('Профиль ✨')
            button2 = types.KeyboardButton('Магазин 🛒')
            button3 = types.KeyboardButton('Справка 📋')
            markup.row(button1)
            markup.row(button2)
            markup.row(button3)
            
            bot.send_message(message.chat.id, f"Привет {message.from_user.username}! 👋\n \nДобро Пожаловать в лучший магазин сертификатов для Steam, Xbox и PlayStation! 💜\n \nТех. Поддержка ➡️ @itzkeeni", reply_markup=markup)

@bot.message_handler(commands=['admin'])
def admin(message):
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = message.chat.id
    sql.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
    user_statsus = sql.fetchone()[0]

    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    user_idd = sql.fetchone()[0]

    if user_statsus != 'admin':
        bot.send_message(message.chat.id, f"У вас нету доступа!")

    if user_idd != '1643087866':
        if user_statsus == 'admin':
            status = user_statsus
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("Пополнить баланс",callback_data='balance_user_add')
            button2 = types.InlineKeyboardButton("Вычесть с баланса",callback_data='balance_user_unadd')
            button3 = types.InlineKeyboardButton("Заблокировать",callback_data='ban')
            button4 = types.InlineKeyboardButton("Разблокировать",callback_data='unban')
            button6 = types.InlineKeyboardButton("Проверить чек",callback_data='check_check')
            button7 = types.InlineKeyboardButton("Добавить Промо",callback_data='promo_add')
            markup.add(button1, button2)
            markup.add(button3, button4)
            markup.add(button6)
            markup.add(button7)
            bot.send_message(message.chat.id, f"Админ панель\nid: {user_id}\nStatus: {status}", reply_markup=markup)
    else:
        status = user_statsus
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Пополнить баланс",callback_data='balance_user_add')
        button2 = types.InlineKeyboardButton("Вычесть с баланса",callback_data='balance_user_unadd')
        button3 = types.InlineKeyboardButton("Заблокировать",callback_data='ban')
        button4 = types.InlineKeyboardButton("Разблокировать",callback_data='unban')
        button6 = types.InlineKeyboardButton("Проверить чек",callback_data='check_check')
        button5 = types.InlineKeyboardButton("Добавить/убрать администартора",callback_data='admin_set')
        button7 = types.InlineKeyboardButton("Добавить Промо",callback_data='promo_add')
        button8 = types.InlineKeyboardButton("Редактировать промо",callback_data='promo_edit')
        markup.add(button1, button2)
        markup.add(button3, button4)
        markup.add(button6)
        markup.add(button5)
        markup.add(button7, button8)
        bot.send_message(message.chat.id, f"Админ панель\nid: {user_id}\nStatus: {status}", reply_markup=markup)

@bot.message_handler(commands=['stop'])
def stop(message):    
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = message.chat.id
    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    users = sql.fetchone()[0]

    if users != '1643087866':
         bot.send_message(message.chat.id, text="У вас нет доступа!")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('✔', callback_data='bot_stop')
        button2 = types.InlineKeyboardButton("❌",callback_data='cancel')
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы уверены совершить экстренную остановку бота?", reply_markup=markup)

@bot.message_handler(content_types='photo')
def get_photo(message):
    bot.send_message(message.chat.id, 'Я не посмотреть эту картинку с котиками😢')
    
@bot.message_handler()
def menu(message):
    user_id = message.from_user.id
    db = sql3.connect('base.db')
    sql = db.cursor()
    if message.text == 'Профиль ✨':
        sql.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance = sql.fetchone()[0]

        sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
        total_buy = sql.fetchone()[0]

        sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
        spent_money = sql.fetchone()[0]

        sql.execute(f"SELECT status FROM users WHERE user_id = ?", (user_id,))
        status = sql.fetchone()[0]

        if status != 'admin':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("💸 Пополнить баланс",callback_data='balance_add')
            button2 = types.InlineKeyboardButton("📢 Написать отзыв",url='https://t.me/+Vgj-5isB5I9iZjdi')
            button3 = types.InlineKeyboardButton("🎁 Вввести промокод",callback_data='promo')
            markup.row(button1, button2)
            markup.row(button3)
            bot.send_message(message.chat.id, f"⚙ Профиль\n👾 ID: {message.from_user.id}\n \n🔑 Баланс: {balance}\n💳 Куплено товаров: {total_buy}\n😥 Всего потрачено: {spent_money}\n \n👑 Статус: {status}", reply_markup=markup)

        if status == 'admin':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton("💸 Пополнить баланс",callback_data='balance_add')
            button2 = types.InlineKeyboardButton("📢 Написать отзыв",url='https://t.me/+Vgj-5isB5I9iZjdi')
            button3 = types.InlineKeyboardButton("📢 Информация о пользователе",callback_data='user_info')
            button4 = types.InlineKeyboardButton("🎁 Вввести промокод",callback_data='promo')
            markup.row(button1, button2)
            markup.row(button4)
            markup.row(button3)
            bot.send_message(message.chat.id, f"⚙ Профиль\n👾 ID: {message.from_user.id}\n \n🔑 Баланс: {balance}\n💳 Куплено товаров: {total_buy}\n😥 Всего потрачено: {spent_money}\n \n👑 Статус: {status}", reply_markup=markup)

    elif message.text == 'Магазин 🛒':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="⬛ Steam",callback_data='steam')
        button2 = types.InlineKeyboardButton(text="🟩 Xbox",callback_data='xbox')
        button3 = types.InlineKeyboardButton(text="🟦 PS Store",callback_data='ps')
        button4 = types.InlineKeyboardButton(text="⬜ Apple Card",callback_data='apple')
        markup.add(button1)
        markup.add(button2)
        markup.add(button3)
        # markup.add(button4)
        bot.send_message(message.chat.id, "Выберите категорию:", reply_markup=markup)

    elif message.text == 'Справка 📋':
        sql.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
        status = sql.fetchone()[0]
        if status != 'admin':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="⬛ Как активировать Steam",url='https://telegra.ph/Kak-aktivirovat-Steam-06-29')
            button2 = types.InlineKeyboardButton(text="🟩 Как активировать Xbox",url='https://telegra.ph/Kak-aktivirovat-Xbox-06-26')
            button3 = types.InlineKeyboardButton(text="🟦 Как активировать PS",url='https://telegra.ph/Kak-aktivirovat-PS-Store-08-01')
            # button4 = types.InlineKeyboardButton(text="🟦 Как активировать Apple Card",url='https://www.youtube.com/')
            button5 = types.InlineKeyboardButton(text="📢 Наш Телеграм канал",url='t.me/itzstorenews')
            button6 = types.InlineKeyboardButton(text="📞 Поддержка",url='t.me/itzkeeni')
            button7 = types.InlineKeyboardButton(text="Для Администрации", url='https://telegra.ph/Stroenie-cheka-v-ItzStore-07-16')
            markup.add(button1)
            # markup.add(button4)
            markup.add(button2, button3)
            markup.add(button5, button6)
            bot.send_message(message.chat.id, "📋 Справка\n \nВ справке описано как активировать промо-коды на разные сервисы, наш телеграм канал и поддержка\n \nВыберите нужный вам сервис ниже ⬇", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="⬛ Как активировать Steam",url='https://telegra.ph/Kak-aktivirovat-Steam-06-29')
            button2 = types.InlineKeyboardButton(text="🟩 Как активировать Xbox",url='https://telegra.ph/Kak-aktivirovat-Xbox-06-26')
            button3 = types.InlineKeyboardButton(text="🟦 Как активировать PS",url='https://telegra.ph/Kak-aktivirovat-PS-Store-08-01')
            # button4 = types.InlineKeyboardButton(text="🟦 Как активировать Apple Card",url='https://www.youtube.com/')
            button5 = types.InlineKeyboardButton(text="📢 Наш Телеграм канал",url='t.me/itzstorenews')
            button6 = types.InlineKeyboardButton(text="📞 Поддержка",url='t.me/itzkeeni')
            button7 = types.InlineKeyboardButton(text="Для Администрации", url='https://telegra.ph/Stroenie-cheka-v-ItzStore-07-16')
            markup.add(button1)
            # markup.add(button4)
            markup.add(button2, button3)
            markup.add(button5, button6)
            markup.add(button7)
            bot.send_message(message.chat.id, "📋 Справка\n \nВ справке описано как активировать промо-коды на разные сервисы, наш телеграм канал и поддержка\n \nВыберите нужный вам сервис ниже ⬇", reply_markup=markup)

def process_data(message):
    global sum_to_pay
    sum_to_pay = message.text
    if sum_to_pay.isdigit() and int(sum_to_pay) > 100:
        PayOkPayment.authorize("Api-key", "Api-ID", "Shop-ID", "Secret-key",
                            payment_type=PayOkPaymentType.CARD,
                            currency=PayOkCurrency.RUB,
                            success_url="https://sites.google.com/view/itzstorealerts/ok")
        global payment
        payment = PayOkPayment(amount=sum_to_pay,
                            description="Pay to ItzStore",
                            payment_type=PayOkPaymentType.CARD,
                            currency=PayOkCurrency.RUB,
                            success_url="https://sites.google.com/view/itzstorealerts/ok")
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Оплатить', url=payment.url)
        button7 = types.InlineKeyboardButton("Проверить",callback_data='check')
        markup.row(button1)
        markup.row(button7)
        bot.send_message(chat_id=message.chat.id, text=f"Платеж создан\nСумма оплаты: {sum_to_pay}\nВремя для оплаты: 60мин", reply_markup=markup)
    elif sum_to_pay is not sum_to_pay.isdigit():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Назад",callback_data='balance_add')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text="❌ Неправильно значения или сумма меньше 100 рублей")

def admin_set(message):
    global user_id_for_admin_set
    user_id_for_admin_set = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"SELECT user_id FROM users WHERE user_id = ?", (user_id_for_admin_set,))
    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='admin_set')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Добавить администраторы', callback_data='set_admin')
        button2 = types.InlineKeyboardButton('Убрать из администраторов', callback_data='remove_admin')
        markup.row(button1)
        markup.row(button2)
        bot.send_message(chat_id=message.chat.id, text="Выберите действия:", reply_markup=markup)

def promo(message):
    promo = message.text
    user_id = message.chat.id
    db = sql3.connect('base.db')
    sql = db.cursor()
    
    sql.execute("SELECT name FROM promo_codes WHERE name = ?", (promo,))
    if sql.fetchone() is None:
        bot.send_message(chat_id=message.chat.id, text="❌ Такого промокода нету")
    else:
        sql.execute("SELECT name FROM promo_codes WHERE name = ?", (promo,))
        name = sql.fetchone()[0]

        sql.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
        balance = sql.fetchone()[0]

        sql.execute("SELECT amount FROM promo_codes WHERE name = ?", (name,))
        amount = sql.fetchone()[0]

        sql.execute("SELECT sum FROM promo_codes WHERE name = ?", (name,))
        sym = sql.fetchone()[0]
        if amount <= 0:
            bot.send_message(chat_id=message.chat.id, text="❌ Промкод не действителен")
        else:
            sql.execute("UPDATE users SET balance = ? WHERE user_id = ?", (balance + int(sym), user_id))
            sql.execute("UPDATE promo_codes SET amount = ? WHERE name = ?", (amount - 1, name))
            db.commit()

            bot.send_message(chat_id=message.chat.id, text="✅ Промокод успешно активирован!")

def promo_add_sum_reg(message):
    global promo_sum 
    promo_sum = message.text 
    db = sql3.connect('base.db')
    sql = db.cursor()

    if promo_sum.isdigit() and int(promo_sum) > 101:
        bot.send_message(chat_id=message.chat.id, text="❌ Сумма не может быть больше 100 рублей!")
    elif promo_sum.isdigit():  
        sql.execute("INSERT INTO promo_codes VALUES (?, ?, ?)", (promo_name, promo_amount, promo_sum))
        db.commit()
        bot.send_message(chat_id=message.chat.id, text=f"✅ Промокод {promo_name} успешно добавлен!")
    else:
        bot.send_message(chat_id=message.chat.id, text="❌ Непавильное значения")  
           
def promo_add_amount_reg(message):
    global promo_amount 
    promo_amount = message.text
    
    if promo_amount.isdigit() and int(promo_amount) > 10:
        bot.send_message(chat_id=message.chat.id, text="❌ Колличество активаций не может быть больше 10!")
    else:
        bot.send_message(chat_id=message.chat.id, text="Введите сумму промокода: ")
        bot.register_next_step_handler(message, promo_add_sum_reg)
        
def promo_add_name_reg(message):
    db = sql3.connect('base.db')
    sql = db.cursor()

    global promo_name 
    promo_name = message.text
    sql.execute("SELECT name FROM promo_codes WHERE name = ?", (promo_name,))
    
    if sql.fetchone() is None:
        if len(promo_name) > 50:
            bot.send_message(chat_id=message.chat.id, text="❌ Максимальная длина 50 символов!")
        elif len(promo_name) <= 4: 
            bot.send_message(chat_id=message.chat.id, text="❌ Минимальная длина 5 символов!")
        else:    
            bot.send_message(chat_id=message.chat.id, text="Введите кол-во активаций промокода: ")
            bot.register_next_step_handler(message, promo_add_amount_reg)
    else:
        bot.send_message(chat_id=message.chat.id, text="❌ Такой промокод уже есть!")

def steam_ru(message):
    global sym_to_ref
    global sym_to_pay_steam
    sym_to_ref = message.text

    if sym_to_ref.isdigit() and int(sym_to_ref) > 100 and int(sym_to_ref) < 15001:
        sym_to_ref = int(sym_to_ref)
        sym_to_pay_steam = int(sym_to_ref+sym_to_ref/100*15)

        print(sym_to_pay_steam)
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_ru_next')
        button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
        markup.row(button1)
        markup.row(button2)
        bot.send_message(chat_id=message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Пополнения Steam Россия\n💸 К пополнению: {sym_to_ref}₽ \n💸 К оплате: {sym_to_pay_steam}₽", reply_markup=markup)
    if int(sym_to_ref) <= 99:
        bot.send_message(chat_id=message.chat.id, text="❌ Сумма меньше 100 рублей")
    if int(sym_to_ref) >= 15001:
        bot.send_message(chat_id=message.chat.id, text="❌ Сумма больше 15000 рублей")     
    if sym_to_ref.isdigit() == False:
        bot.send_message(chat_id=message.chat.id, text="❌ Неправильно значения")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_id = call.message.chat.id 
    sql.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
    user_status = sql.fetchone()

    if user_status[0] != 'blocked':
        
        if call.data == 'buy_steam_ru_next':
            print(sym_to_ref)
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay_steam:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_ru', sym_to_ref,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay_steam)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay_steam} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Пополнения Steam Россия\n💸 Сумма для пополнения: {sym_to_ref}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'balance_user_add':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, balance_add)
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')    
            
        if call.data == 'balance_user_unadd':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, balance_unadd)
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')   

        if call.data == 'promo_add':
            if user_status[0] == 'admin':
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="Отменить ",callback_data='cancel')
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите названия промокода: ", message_id=call.message.message_id, reply_markup=markup)
                bot.register_next_step_handler(call.message, promo_add_name_reg)
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')    

        if call.data == 'promo_edit':
            if user_status[0] == 'admin':
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text="Изменить названия",callback_data='promo_name_edit')
                button2 = types.InlineKeyboardButton(text="Изменить кол-во активаций",callback_data='promo_amount_edit')
                button3 = types.InlineKeyboardButton(text="Изменить сумму",callback_data='promo_sum_edit')
                button4 = types.InlineKeyboardButton(text="Удалить промкод",callback_data='promo_delete')
                markup.add(button1, button2, button3)
                markup.add(button4)
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите действия ", message_id=call.message.message_id, reply_markup=markup)
                
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')    

        if call.data == 'ban':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, user_ban)  
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')   

        if call.data == 'bot_stop':
            print("session the close")
            sql.execute()

        if call.data == 'unban':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, user_unban)    
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')   

        if call.data == 'admin_set':
            sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            user_idd = sql.fetchone()
            print(user_idd)
            if user_idd[0] != "1643087866":
                bot.send_message(chat_id=call.message.chat.id, text=f"У вас нету доступа!")
            
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, admin_set)

        if call.data == 'steam':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🇷🇺 Steam Россия', callback_data='ru')
            button2 = types.InlineKeyboardButton('🇪🇺 Steam Европа', callback_data='eu')
            button3 = types.InlineKeyboardButton('🇺🇸 Steam Америка', callback_data='us')
            button4 = types.InlineKeyboardButton("↩️ Назад",callback_data='backk')
            markup.row(button1, button2, button3)
            markup.row(button4)
            bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите под-категорию: ", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'backk': 
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton(text="⬛ Steam",callback_data='steam')
            button2 = types.InlineKeyboardButton(text="🟩 Xbox",callback_data='xbox')
            button3 = types.InlineKeyboardButton(text="🟦 PS Store",callback_data='ps')
            button4 = types.InlineKeyboardButton(text="⬜ Apple Card",callback_data='apple')
            markup.add(button1)
            markup.add(button2)
            markup.add(button3)
            # markup.add(button4)
            bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите категорию:", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'xbox':
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('Xbox 10 USD | 1200р', callback_data='buy_xbox_10usd')
                button2 = types.InlineKeyboardButton('Xbox 25 USD | 3000р', callback_data='buy_xbox_25usd')
                button3 = types.InlineKeyboardButton('Xbox 50 USD | 6000р', callback_data='buy_xbox_50usd')
                button4 = types.InlineKeyboardButton("↩️ Назад",callback_data='backk')
                markup.row(button1)
                markup.row(button2)
                markup.row(button3)
                markup.row(button4)
                bot.edit_message_text(chat_id=call.message.chat.id, text="💚Xbox (Америка)\n \n🔐Гарантия: до момента активации\n🤔Как активировать?: Справка>Как активировать Xbox\n \n ❗После покупки вы получаете ПРОМОКОД для активации и действует он только для АМЕРИКАНСКИХ аккаунтов", reply_markup=markup, message_id=call.message.message_id) 

        if call.data == 'ps':
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('PS Network 10 USD | 1100р', callback_data='ps_usa_10usd')
                button2 = types.InlineKeyboardButton('PS Network 25 USD | 2800р', callback_data='ps_usa_25usd')
                button3 = types.InlineKeyboardButton('PS Network 50 USD | 5570р', callback_data='ps_usa_50usd')
                button4 = types.InlineKeyboardButton('PS Network 100 USD | 11000р', callback_data='ps_usa_100usd')
                button5 = types.InlineKeyboardButton("↩️ Назад",callback_data='backk')
                markup.row(button1)
                markup.row(button2)
                markup.row(button3)
                markup.row(button4)
                markup.row(button5)
                bot.edit_message_text(chat_id=call.message.chat.id, text="💙PlayStation Store (Америка)\n \n🔐Гарантия: до момента активации\n🤔Как активировать?: Справка>Как активировать PS\n \n❗После покупки вы получаете ПРОМОКОД для активации и он действует только для АМЕРИКАНСКИХ аккаунтов", reply_markup=markup, message_id=call.message.message_id) 

        if call.data == 'apple':
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('Apple Card 3 US | 350р', callback_data='apple_usa_3usd')
                button2 = types.InlineKeyboardButton('Apple Card 5 US | 575р', callback_data='apple_usa_5usd')
                button3 = types.InlineKeyboardButton('Apple Card 10 US | 1120р', callback_data='apple_usa_10usd')
                button4 = types.InlineKeyboardButton('Apple Card 20 US | 2200р', callback_data='apple_usa_20usd')
                button5 = types.InlineKeyboardButton('Apple Card 30 US | 3250р', callback_data='apple_usa_30usd')
                button6 = types.InlineKeyboardButton('Apple Card 50 US | 5300р', callback_data='apple_usa_50usd')
                button7 = types.InlineKeyboardButton('Apple Card 100 US | 10600р', callback_data='apple_usa_100usd')
                button8 = types.InlineKeyboardButton('Apple Card 200 US | 21500р', callback_data='apple_usa_200usd')
                button9 = types.InlineKeyboardButton("↩️ Назад",callback_data='backk')
                markup.row(button1)
                markup.row(button2)
                markup.row(button3)
                markup.row(button4)
                markup.row(button5)
                markup.row(button6)
                markup.row(button7)
                markup.row(button8)
                markup.row(button9)
                bot.edit_message_text(chat_id=call.message.chat.id, text="🤍 Apple (Доллары)\n \n🔐Гарантия: до момента активации\n🤔Как активировать?: Справка>Как активировать Apple\n \n❗После покупки вы получаете ПРОМОКОД для активации и он действует только для АМЕРИКАНСКИХ аккаунтов"    , reply_markup=markup, message_id=call.message.message_id) 

        if call.data == 'ru':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_ru')
            button2 = types.InlineKeyboardButton("↩️ Назад",callback_data='backkk')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text="🖤Steam (Россия)\n \n🔐Гарантия: До момента пополнения\n🤔Как происходит поплнения?:\n1. Вы покупаете товар и пишите свой логин стим\n2. Мы поплняем ваш баланс👍 \n  \n❗ Этот товар работает для аккаунтов с регионами Россия и к вашей сумме будет прибовлятся комиссия 15%!", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'eu':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Steam EUR 20 | 2550р', callback_data='buy_steam_eu_20')
            button2 = types.InlineKeyboardButton('Steam EUR 50 | 6050р', callback_data='buy_steam_eu_50')
            button3 = types.InlineKeyboardButton("↩️ Назад",callback_data='backkk')
            markup.row(button1)
            markup.row(button2)
            markup.row(button3)
            bot.edit_message_text(chat_id=call.message.chat.id, text="🖤Steam (Турция)\n \n🔐Гарантия: До момента пополнения\n🤔Как активировать?: Справка>Как активировать Steam\n  \n❗После покупки вы получаете ПРОМОКОД для активации и он действует только для ТУРЕЦКИХ аккаунтов", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'cancel':
            bot.delete_message(call.message.chat.id, call.message.message_id)

        if call.data == 'backkk':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('🇷🇺 Steam Россия', callback_data='ru')
            button2 = types.InlineKeyboardButton('🇪🇺 Steam Европа', callback_data='eu')
            button3 = types.InlineKeyboardButton('🇺🇸 Steam Америка', callback_data='us')
            button4 = types.InlineKeyboardButton("↩️ Назад",callback_data='backk')
            markup.row(button1, button2, button3)
            markup.row(button4)
            bot.edit_message_text(chat_id=call.message.chat.id, text="Выберите под-категорию: ", reply_markup=markup, message_id=call.message.message_id)  

        if call.data == 'us':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('Steam US 5 USD | 585р', callback_data='buy_steam_usa_5usd')
            button2 = types.InlineKeyboardButton('Steam US 10 USD | 1150р', callback_data='buy_steam_usa_10usd')
            button3 = types.InlineKeyboardButton('Steam US 20 USD | 2280р', callback_data='buy_steam_usa_20usd')
            button4 = types.InlineKeyboardButton('Steam US 25 USD | 2800р', callback_data='buy_steam_usa_25usd')
            button5 = types.InlineKeyboardButton("↩️ Назад",callback_data='backkk')
            markup.row(button1)
            markup.row(button2)
            markup.row(button3)
            markup.row(button4)
            markup.row(button5)
            bot.edit_message_text(chat_id=call.message.chat.id, text="🖤Steam (Америка)\n \n🔐Гарантия: До момента пополнения\n🤔Как активировать?: Справка>Как активировать Steam\n  \n❗После покупки вы получаете ПРОМОКОД для активации и он действует только для АМЕРИКАНСКИХ аккаунтов", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy':
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', url='t.me/itzkeeni')
            button7 = types.InlineKeyboardButton("↩️ Назад",callback_data='backkk')
            markup.row(button1)
            markup.row(button7)
            bot.edit_message_text(chat_id=call.message.chat.id, text="👨‍💻 Пока, что автоматическая оплата находится в разработке \n \nПоэтому, за покупкой писать ➡ @itzkeeni", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'balance_add':
            bot.edit_message_text(chat_id=call.message.chat.id, text="Введите сумму пополнения:", message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, process_data)

        if call.data == 'set_admin':
            sql.execute(f"UPDATE users SET status = ? WHERE user_id = ?", ('admin', user_id_for_admin_set)) 
            db.commit() 
            bot.send_message(chat_id=call.message.chat.id, text=f"Пользователю <b>{user_id_for_admin_set}</b> был установлен статус Администратора!", parse_mode='html') 

        if call.data == 'remove_admin':
            sql.execute(f"UPDATE users SET status = ? WHERE user_id = ?", ('user', user_id_for_admin_set)) 
            db.commit() 
            bot.send_message(chat_id=call.message.chat.id, text=f"Пользователю <b>{user_id_for_admin_set}</b> был убран статус Администратора!", parse_mode='html') 

        if call.data == 'check':
            if payment.status == PaymentStatus.PAID:
                user_id = call.message.chat.id
                sql.execute(f"SELECT balance FROM users WHERE user_id = {user_id}")
                balance = sql.fetchone()[0]
                sql.execute(f"UPDATE users SET balance = {int(sum_to_pay) + balance} WHERE user_id = {user_id}")
                db.commit()
                sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
                balance = sql.fetchone()[0]
                bot.edit_message_text(chat_id=call.message.chat.id, text=f"👌Баланс успешно пополнен!\nТекущий баланс: {balance}", message_id=call.message.message_id)

            if payment.status == PaymentStatus.WAITING:
                bot.send_message(chat_id=call.message.chat.id, text="Платеж создан, но еще не оплачен")
                
            if PaymentStatus == PaymentStatus.REJECTED:
                bot.edit_message_text(chat_id=call.message.chat.id, text="Платеж был откланен", message_id=call.message.message_id)
                
            if PaymentStatus == PaymentStatus.EXPIRED:
                bot.edit_message_text(chat_id=call.message.chat.id, text="Срок действия платежа истек", message_id=call.message.message_id) 

        if call.data == 'buy_steam_ru':
            bot.edit_message_text(chat_id=call.message.chat.id, text="Введите сколько рублей хотите пополнить: ", message_id=call.message.message_id)
            bot.register_next_step_handler(call.message, steam_ru)  

        if call.data == 'check_check':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите номер заказа:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, check_check)
            else:
                bot.send_message(chat_id=call.message.chat.id, text=f"У вас нету доступа!")

        if call.data == 'promo':
            bot.send_message(chat_id=call.message.chat.id, text="Введите промокод:")
            bot.register_next_step_handler(call.message, promo)  

#region buy 

        #region steam

        if call.data == 'buy_steam_usa_5usd':
            sym_to_pay = 585
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_usa_5usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Америка 5 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_usa_5usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 585
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_usa_5usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Америка 5 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_steam_usa_10usd':
            sym_to_pay = 1150
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_usa_10usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Америка 10 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_usa_10usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 1150
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_usa_10usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Америка 10 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_steam_usa_20usd':
            sym_to_pay = 2280
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_usa_20usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Америка 20 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_usa_20usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 2280
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_usa_20usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Америка 20 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_steam_usa_25usd':
            sym_to_pay = 2800
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_usa_25usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Америка 25 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_usa_25usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 2800
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_usa_25usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Америка 25 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_steam_eu_20':
            sym_to_pay = 2550
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_eu_20_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Европа 20 Евро\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_eu_20_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 2550
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_eu_20eur', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Европа 20 Евро\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_steam_eu_50':
            sym_to_pay = 6050
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_steam_eu_50_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Steam Европа 50 Евро\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_steam_eu_50_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 6050
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Steam_eu_50eur', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Steam Европа 50 Евро\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        #endregion steam

        #region xbox

        if call.data == 'buy_xbox_10usd':
            sym_to_pay = 1200
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_xbox_10usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Xbox Америка 10 долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_xbox_10usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 1200
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Xbox_usa_10usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Xbox Америка 10 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'buy_xbox_25usd':
            sym_to_pay = 3000
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_xbox_25usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Xbox Америка 25 долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_xbox_25usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 3000
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Xbox_usa_25usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Xbox Америка 25 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберте наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")
        
        if call.data == 'buy_xbox_50usd':
            sym_to_pay = 6000
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='buy_xbox_50usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: Xbox Америка 50 долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'buy_xbox_50usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 6000
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'Xbox_usa_50usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: Xbox Америка 50 долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберите наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        #endregion xbox

        #region ps

        if call.data == 'ps_usa_10usd':
            sym_to_pay = 1100
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='ps_usa_10usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: PS Store Америка 10 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'ps_usa_10usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 1100
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'ps_usa_10usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: PS Store Америка 10 Долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберите наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'ps_usa_25usd':
            sym_to_pay = 2800
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='ps_usa_25usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: PS Store Америка 25 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'ps_usa_25usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 2800
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'ps_usa_25usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: PS Store Америка 25 Долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберите наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'ps_usa_50usd':
            sym_to_pay = 5570
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='ps_usa_50usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: PS Store Америка 50 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'ps_usa_50usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 5570
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'ps_usa_50usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: PS Store Америка 50 Долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберите наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        if call.data == 'ps_usa_100usd':
            sym_to_pay = 11000
            markup = types.InlineKeyboardMarkup()
            button1 = types.InlineKeyboardButton('💳 Купить', callback_data='ps_usa_100usd_next')
            button2 = types.InlineKeyboardButton("↩️ Отменить",callback_data='cancel')
            markup.row(button1)
            markup.row(button2)
            bot.edit_message_text(chat_id=call.message.chat.id, text=f"✅ Подтверждения покупки\n \n🛒 Товар: PS Store Америка 100 Долларов\n💸 К оплате: {sym_to_pay}₽", reply_markup=markup, message_id=call.message.message_id)

        if call.data == 'ps_usa_100usd_next':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            sym_to_pay = 11000
            sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_id}'")
            balance = sql.fetchone()[0]

            sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_id,))
            total_buy = sql.fetchone()[0]

            sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_id,))
            spent_money = sql.fetchone()[0]

            if balance < sym_to_pay:
                 bot.send_message(chat_id=call.message.chat.id, text="❌ На балансе недосточно средств!")
            else:
                product_code = int(randint(1000, 500000))
                sql.execute("INSERT INTO product VALUES (?, ?, ?, ?)", (product_code, user_id, 'ps_usa_100usd', sym_to_pay,))
                db.commit()

                time = date.today()
                hour = datetime.now().hour
                minute = datetime.now().minute

                sql.execute(f"UPDATE users SET balance = {balance - int(sym_to_pay)} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET total_buy = {total_buy+1} WHERE user_id = {user_id}")
                sql.execute(f"UPDATE users SET spent_money = {spent_money+sym_to_pay} WHERE user_id = {user_id}")

                db.commit()

                bot.send_message(chat_id=call.message.chat.id, text=f"📰 Номер заказа: {product_code}\n \n🛒 Названия товара: PS Store Америка 100 Долларов\n💸 Сумма покупки: {sym_to_pay}\n⌛ Время покупки: {time} {hour}:{minute}\n \n👾 Покупатель: {user_id}")
                bot.send_message(chat_id=call.message.chat.id, text=f"Для выдачи товара перешлите данное сообщения @ItzKeeni\n \nЧтобы переслать сообщению, зажмите на нем палец или нажмите по нему ПКМ, выберите наверху стрелочку в право, в поиске найдите ItzKeeni и нажмите отправить)")

        #endregion ps

        #region apple
            
        #endregion apple 

#endregion buy

        if call.data == 'user_info':
            if user_status[0] == 'admin':
                bot.edit_message_text(chat_id=call.message.chat.id, text="Введите id:", message_id=call.message.message_id)
                bot.register_next_step_handler(call.message, user_info)  
            else:
                bot.send_message(call.message.chat.id, text='У вас нету доступа!')   
            
    else:
        bot.send_message(chat_id=call.message.chat.id, text=f"⛔Ваш аккаунт заблокирован!\nВам закрыт доступ к магазину с аккаунта <b>{user_id}</b>\n \n📞Если ваш аккаунт не является аккаунтом <b>1683841862</b> вы можете написать в тех. поддержку для разблокировки", parse_mode="html")    


def balance_add(message):
    db = sql3.connect('base.db')
    sql = db.cursor()
    global user_idd
    user_idd = message.text
    print(user_idd)

    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_idd,))

    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='balance_user_add')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else:
       bot.send_message(chat_id=message.chat.id, text="Введите сумму поплнения:")
       bot.register_next_step_handler(message, balance_add_next) 

def balance_add_next(message):
    sym = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_idd}'")
    balance = sql.fetchone()[0]
    sql.execute(f"UPDATE users SET balance = {int(sym) + balance} WHERE user_id = {user_idd}")
    db.commit()
    sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_idd}'")
    balance = sql.fetchone()[0]
    bot.send_message(chat_id=message.chat.id, text=f"Баланс {user_idd} пополнен на {sym}\nТекущий баланс: {balance}")

def balance_unadd(message):
    db = sql3.connect('base.db')
    sql = db.cursor()
    global user_idd
    user_idd = message.text

    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_idd,))

    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='balance_user_unadd')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else:
       bot.send_message(chat_id=message.chat.id, text="Введите сколько вычисть:")
       bot.register_next_step_handler(message, balance_unadd_next)

def balance_unadd_next(message):
    sym = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_idd}'")
    balance = sql.fetchone()[0]
    sql.execute(f"UPDATE users SET balance = {balance - int(sym)} WHERE user_id = {user_idd}")
    db.commit()
    sql.execute(f"SELECT balance FROM users WHERE user_id = '{user_idd}'")
    balance = sql.fetchone()[0]
    bot.send_message(chat_id=message.chat.id, text=f"С баланса {user_idd} вычьтено {sym}\nТекущий баланс: {balance}")

def user_ban(message):
    user_idd = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_idd,))

    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='ban')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else:    
        sql.execute(f"UPDATE users SET status = ? WHERE user_id = ?", ('blocked', user_idd)) 
        db.commit() 
        bot.send_message(chat_id=message.chat.id, text=f"Пользователь {user_idd} был заблокирован!")    

def user_unban(message):
    user_idd = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_idd,)) 
    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='ban')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else: 
        sql.execute(f"UPDATE users SET status = ? WHERE user_id = ?", ('user', user_idd)) 
        db.commit() 
        bot.send_message(chat_id=message.chat.id, text=f"Пользователь {user_idd} был разблокирован!")  

def check_check(message):
    product_code = message.text
    db = sql3.connect('base.db')
    sql = db.cursor()
    sql.execute(f"SELECT check_id FROM product WHERE check_id = {product_code}")
    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='check_check')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого заказа нету!", reply_markup=markup)
    else:
        sql.execute(f"SELECT user_id FROM product WHERE check_id = {product_code}")
        user_id = sql.fetchone()[0]

        sql.execute(f"SELECT product FROM product WHERE check_id = {product_code}")
        product = sql.fetchone()[0]

        sql.execute(f"SELECT sum FROM product WHERE check_id = {product_code}")
        sym = sql.fetchone()[0]
        bot.send_message(chat_id=message.chat.id, text=f"Номер заказа: {product_code}\n \nПокупатель: {user_id}\n \nТовар: {product}\n \nСумма заказа: {sym}")  

def user_info(message):
    db = sql3.connect('base.db')
    sql = db.cursor()
    user_idd = message.text
    print(user_idd)

    sql.execute("SELECT user_id FROM users WHERE user_id = ?", (user_idd,))

    if sql.fetchone() is None:
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('Назад', callback_data='balance_user_add')
        markup.row(button1)
        bot.send_message(chat_id=message.chat.id, text=f"Такого id нету!")
    else:
        sql.execute(f"SELECT balance FROM users WHERE user_id = ?", (user_idd,))
        balance = sql.fetchone()[0]

        sql.execute(f"SELECT total_buy FROM users WHERE user_id = ?", (user_idd,))
        total_buy = sql.fetchone()[0]

        sql.execute(f"SELECT spent_money FROM users WHERE user_id = ?", (user_idd,))
        spent_money = sql.fetchone()[0]

        sql.execute(f"SELECT status FROM users WHERE user_id = ?", (user_idd,))
        status = sql.fetchone()[0]

        bot.send_message(message.chat.id, f"⚙ Профиль\n👾 ID: {user_idd}\n \n🔑 Баланс: {balance}\n💳 Куплено товаров: {total_buy}\n😥 Всего потрачено: {spent_money}\n \n👑 Статус: {status}")


bot.polling(non_stop=True)    

# \n
