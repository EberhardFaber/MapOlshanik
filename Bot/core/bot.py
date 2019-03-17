from telebot import types, apihelper, TeleBot
import re
from core.static import botText
from core import database

class BotTelegram(object):

    def __init__(self, token, proxy):
        apihelper.proxy = {
            'https': 'socks5://' + proxy['LOGIN'] + ':' + proxy['PSW'] + '@' + proxy['IP'] + ':' + proxy['PORT']
        }
        self.bot = TeleBot(token)

    def start_and_work(self):

        # Actions after /start command
        @self.bot.message_handler(commands=['start'])
        def send_welcom(message):
            self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            self.markup.row(botText.NEW_TEAM, botText.SIGNIN_TEAM)
            answer = self.bot.send_message(message.from_user.id, botText.START, reply_markup=self.markup)
            self.bot.register_next_step_handler(answer, process_choose_sigin_step)
            database.register_user(message.chat)

        # Actions after choice: new team OR choose team
        def process_choose_sigin_step(message):
            markup = types.ReplyKeyboardRemove(selective=False)
            if message.text == botText.NEW_TEAM:
                answer = self.bot.send_message(message.from_user.id, botText.NAME_TEAM, reply_markup=markup)
                self.bot.register_next_step_handler(answer, process_name_command_step)
            elif message.text == botText.SIGNIN_TEAM:
                self.bot.send_message(message.from_user.id, botText.CHOOSE_TEAM, reply_markup=markup)
                team_list = database.take_teams()
                title_team_buttons = types.InlineKeyboardMarkup()
                for title in team_list:
                    butt = types.InlineKeyboardButton(text=title, callback_data=title)
                    title_team_buttons.add(butt)
                answer = self.bot.send_message(message.chat.id, "Список команд:", reply_markup=title_team_buttons)
                self.bot.register_next_step_handler(answer, callback_inline)
            else:
                self.bot.reply_to(message, botText.ERROR)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_inline(call):
            try:
                print(call.message.chat.id, call.data)
                database.choose_team(call.message.chat.id, call.data)
                answer = self.bot.send_message(chat_id=call.message.chat.id, text="Введи пароль:")
                self.bot.register_next_step_handler(answer, process_login_step)
            except:
                self.bot.send_message(call.chat.id, botText.ERROR_PSW)

        # Enter team name
        def process_name_command_step(message):
            database.register_team(message.from_user.id, message.text)
            answer = self.bot.send_message(message.from_user.id, 'Придумай простой пароль:')
            self.bot.register_next_step_handler(answer, process_password_command_step)

        # Enter team password
        def process_password_command_step(message):
            database.inputPSW_team(message.from_user.id, message.text)
            self.bot.send_message(message.from_user.id, botText.REG_TEAM)

        # Team authorization
        def process_login_step(message):
            if database.login_team(message.chat.id, message.text):
                self.bot.send_message(message.from_user.id, botText.LOGIN_TEAM)
            else:
                database.clear_team_for_user(message.chat.id)
                self.bot.send_message(message.from_user.id, botText.ERROR_PSW)


        # Actions after /coords command
        @self.bot.message_handler(commands=['coords'])
        def send_message(message):
            answer = self.bot.send_message(message.from_user.id, botText.POINT)
            self.bot.register_next_step_handler(answer, process_adding_coords)

        # Enter coordinates. If form doesn't correct, enter again
        def process_adding_coords(message):
            result = database.check_register(message.chat.id)
            if result == None:
                self.bot.send_message(message.from_user.id, botText.ERROR_REG)
                print('reg_error from:'+' '+message.chat.id)
            else:
                result = database.coordinates_verify(message.chat.id)
                key_tuple = (float(message.text.split(', ')[0]), float(message.text.split(', ')[1]))
                if key_tuple in result:
                    self.bot.send_message(message.from_user.id, botText.WRONG_POINT)
                else:
                    if re.match(r'\d*.\d*, \d*.\d*', message.text):
                        database.input_point(message.from_user.id, message.text.split(', '))
                        answer = self.bot.send_message(message.from_user.id, botText.HEIGHT)
                        self.bot.register_next_step_handler(answer, process_adding_height)
                    elif message.entities:
                        # Приостанавливаем ввод координат, если введена любая команда
                        self.bot.send_message(message.from_user.id, botText.WHATSUP)
                    else:
                        answer = self.bot.send_message(message.from_user.id, botText.TRY_AGAIN)
                        self.bot.register_next_step_handler(answer, process_adding_coords)

        # Enter point height
        def process_adding_height(message):
                database.input_height(message.from_user.id, message.text)
                self.bot.send_message(message.from_user.id, botText.SAVE_POINT)

        @self.bot.message_handler(commands=['showpoints'])
        def show_points(message):
            coords_list = database.show_points(message.chat.id)
            coords_buttons = types.InlineKeyboardMarkup()
            for array in coords_list:
                string = str(array[0]) + ', ' + str(array[1]) + ', ' + str(array[2])
                butt = types.InlineKeyboardButton(text=string, callback_data=str(array[3]))
                coords_buttons.add(butt)
            self.bot.send_message(message.chat.id, "Список точек:", reply_markup=coords_buttons)





        self.bot.polling(none_stop=True)