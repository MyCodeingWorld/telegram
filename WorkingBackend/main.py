import os
import mysql.connector as SQL
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)

updater = Updater("5027808497:AAHo8-FtHIeOCcP_hv72MdZbTHOgxZPg9D0", use_context=True)
database = SQL.connect(host = 'sql6.freesqldatabase.com',
                       database = "sql6469897",
                       user = 'sql6469897',
                       password = 'KTHyfaFGf6')

choice, typing_choice, new, new_main = range(4)
markup0 = ReplyKeyboardMarkup([ ["USN", "Name"], ["Year", "Semester"], ["Register"], ["Main Menu", "Stop"] ], one_time_keyboard=True, resize_keyboard = True)
markup1 = ReplyKeyboardMarkup([['1', '2'], ['3', '4']], one_time_keyboard=True, resize_keyboard = True)
markup2 = ReplyKeyboardMarkup([['1', '2', '3', '4'], ['5', '6', '7', '8']], one_time_keyboard=True, resize_keyboard = True)

def HELP(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select name, usn from Stud_Record where chat_id = \'{update.message.chat_id}\'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Hello {result[0][0]}, {result[0][1]};
I am HKBK AB Bot,
I can do following work:
/help      = Help for what Bot Can Do
/register  = Register yourself
/main_menu = Go to Main Menu
/ia_mark   = Fetch all IA marks of Current Semester
/ea_mark   = Fetch all last year Semester Marks
/circular  = Latest Circular and Time Table
""", reply_markup = ReplyKeyboardMarkup([['register','/ia_mark'],['circular', '/ea_mark'],['Main Menu'], ['Stop']], one_time_keyboard=True, resize_keyboard = True))
    else:
        update.message.reply_text(f"Hello, I am HKBK AB Bot\nYou are not registered;\nRegister yourself using /register to use my features")
    return ConversationHandler.END

def MAIN_MENU(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select name, usn, year, semester from Stud_Record where chat_id = '{update.message.chat_id}'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Dear {result[0][0]},
Choose One Option from below""", reply_markup=ReplyKeyboardMarkup([['Internal', 'External'], ['Question Bank', 'Notes'], ['Circular'], ['Website', 'Games'], ['Stop']], one_time_keyboard=True, resize_keyboard=True))
        return new_main
    else:
        update.message.reply_text("Please Register yourself using /register to access this bot complete", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

def CIRCULAR(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select chat_id, year, semester from Stud_Record where chat_id = '{update.message.chat_id}'")
    result = cursor.fetchall()
    update.message.reply_text(f"Dear Sir/Mam,\nHere are your important circular and notification")
    if len(result) >= 1:
        path = f"{os.getcwd()}\\Student_DataBase\\Year{result[0][1]}\\{result[0][2]}\\Circular"
        for i in os.listdir(path):
            context.bot.send_document(result[0][0], document = open(f"{path}\\{i}", 'rb'))
            return ConversationHandler.END
    path = f"{os.getcwd()}\\Common_DataBase\\Circular"
    for i in os.listdir(path):
        context.bot.send_document(update.message.chat_id, document = open(f"{path}\\{i}", 'rb'))
        return ConversationHandler.END

def WEBSITE(update: Update, context: CallbackContext):
    update.message.reply_html(f"Please visit out Website:-\n👇👇👇👇👇👇👇👇👇\n\nsites.google.com/view/hkbk-cse-elib", reply_markup=ReplyKeyboardRemove())
    return new_main
    
def DETAILS(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select name, usn, year, semester, status from Stud_Record where chat_id = '{update.message.chat_id}'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Dear Sir/Mam,
According to my Resources,
Your Name is '{result[0][0]}',
Your USN is '{result[0][1]}',
You are currently in '{result[0][2]}' year & '{result[0][3]}' semester,
Your current Status in College is '{result[0][4]}'
""")
        result = cursor = None
    else:
        update.message.reply_text(f"""Hello Sir/Mam,\nI am HKBK AB Bot\nPlease register yourself using /register to use my features""")
        result = cursor = None
        return new

def START(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select name, usn from Stud_Record where chat_id = '{update.message.chat_id}'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Welcome back {result[0][0]} ({result[0][1]})
I HKBK AB Bot is eager to help you in every need...
Use /help to know, How can I help you""", reply_markup = ReplyKeyboardMarkup([['Register', 'User Details'], ['Game', 'Help'], ['Circular'], ['Main Menu'], ['Stop']]))
    else:
        update.message.reply_text(f"""Hello Sir/Mam,\nI am HKBK AB Bot\nPlease register yourself using /register to use my features""",
                                  reply_markup = ReplyKeyboardMarkup([['Register', 'User Details'], ['Game', 'Help'], ['Circular'], ['Main Menu'], ['Stop']]))
    result = cursor = None
    return new

def REGISTER(update: Update, context: CallbackContext):
    cursor = database.cursor()
    cursor.execute(f"select name, usn from Stud_Record where chat_id = \'{update.message.chat_id}\'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Dear {result[0][0]} {result[0][1]},
You are already registered with the bot you can't register again""")
        cursor = result = None
        return ConversationHandler.END
    else:
        update.message.reply_text(f"""Hello, I am HKBK AB Bot
Let's Start Registering
Choose the option one by one for registering""", reply_markup=markup0)
        cursor = result = None
        return choice

def VALUE_INPUT(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data['choice'] = text
    if (text == "USN" or text == "Name"):
        update.message.reply_text(f"Enter your {text}: ")
    elif (text == "Year"):
        update.message.reply_text(f"Choose your current year: ", reply_markup=markup1)
    elif (text == "Semester"):
        update.message.reply_text(f"Choose your current semester: ", reply_markup=markup2)
    
    return typing_choice

def STORE_DATA(update: Update, context: CallbackContext):
    user_data = context.user_data
    text = update.message.text
    category = user_data['choice']
    if category == 'USN':
        user_data[category] = text.upper()[0:10]
    else:
        user_data[category] = text
    del user_data['choice']
    user_data['chat_id'] = update.message.chat_id
    update.message.reply_text(
        f"Thanks for Giving Information!\nContinuing to Registration",
        reply_markup = markup0
    )
    return choice

def SQL_QUERY(update:Update, context: CallbackContext):
    cursor = database.cursor()
    user_data = context.user_data
    cursor.execute(f"select name, usn from Stud_Record where chat_id = '{update.message.chat_id}' or usn = \'{user_data['USN']}\'")
    result = cursor.fetchall()
    if len(result) == 1:
        update.message.reply_text(f"""Dear {result[0][0]} {result[0][1]},
You are already registered with the bot you can't register again""")
    else:
        cursor.execute(f"""
                    insert into Stud_Record Values ({user_data['chat_id']}, \'{user_data['USN']}\', \'{user_data['Name']}\', 'Active', {int(user_data['Year'])}, \'{int(user_data['Semester'])}\');
                    """)
        database.commit()
        update.message.reply_text(f"""You are Registered with following details:-
USN = {user_data['USN']}
Name = {user_data['Name']}
Year = {user_data['Year']}
Semester = {user_data['Semester']}""", reply_markup=ReplyKeyboardRemove())  
    cursor = result = None
    return ConversationHandler.END 

def STOP(update:Update, context: CallbackContext):
    update.message.reply_text("Bye Bye!, Meet You Soon...", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def ERROR(update:Update, context: CallbackContext):
    update.message.reply_text("Invalid Option...\nSorry for Inconvenience\nPlease Choose Correct Option")

handle1 = ConversationHandler(
    entry_points = [MessageHandler(Filters.regex('[Rr][Ee][Gg][Ii][Ss][Tt][Ee][Rr]'), REGISTER), CommandHandler('register', REGISTER)],
    states = {
        choice : [
            MessageHandler(Filters.regex('^(USN|Name|Semester|Year)$'), VALUE_INPUT), 
            MessageHandler(Filters.regex('^Register$'), SQL_QUERY),
            MessageHandler(Filters.regex('^!(USN|Name|Semester|Year)$'), ERROR)
        ],
        typing_choice : [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Register$')), STORE_DATA
                )
            ]
    },
    fallbacks=[MessageHandler(Filters.regex('^Register$'), SQL_QUERY), 
               MessageHandler(Filters.regex('[Mm][Aa][Ii][Nn] [Mm][Ee][Nn][Uu]'), MAIN_MENU), 
               MessageHandler(Filters.regex('[Ss][Tt][Oo][Pp]'), STOP)]
)

handle2 = ConversationHandler(
    entry_points = [CommandHandler('main_menu', MAIN_MENU), MessageHandler(Filters.regex('[Mm][Aa][Ii][Nn] [Mm][Ee][Nn][Uu]'), MAIN_MENU)],
    states = {
        new_main : [
            MessageHandler(Filters.regex('[Cc][Ii][Rr][Cc][Uu][Ll][Aa][Rr]'), CIRCULAR),
            MessageHandler(Filters.regex('[Ss][Tt][Oo][Pp]'), STOP),
            MessageHandler(Filters.regex('[Ww][Ee][Bb][Ss][Ii][Tt][Ee]'), WEBSITE)
        ]
        },
    fallbacks = [MessageHandler(Filters.regex('[Ss][Tt][Oo][Pp]'), STOP)]
)

handle3 = ConversationHandler(
    entry_points = [CommandHandler('start', START), MessageHandler(Filters.regex('[Ss][Tt][Aa][Rr][Tt]'), START)],
    states = {
        new : [ handle1, handle2, MessageHandler(Filters.regex('[Ss][Tt][Oo][Pp]'), STOP),
                 MessageHandler(Filters.regex('[Uu][Ss][Ee][Rr] [Dd][Ee][Tt][Aa][Ii][Ll]'), DETAILS),
                 MessageHandler(Filters.regex('[Cc][Ii][Rr][Cc][Uu][Ll][Aa][Rr]'), CIRCULAR),
                 MessageHandler(Filters.regex('[Hh][Ee][Ll][Pp]'), HELP)],
        },
    fallbacks = [MessageHandler(Filters.regex('[Ss][Tt][Oo][Pp]'), STOP)]
)

updater.dispatcher.add_handler(handle1)
updater.dispatcher.add_handler(handle2)
updater.dispatcher.add_handler(handle3)
updater.dispatcher.add_handler(CommandHandler('help', HELP))
updater.dispatcher.add_handler(CommandHandler('stop', STOP))
updater.dispatcher.add_handler(CommandHandler('main_menu', MAIN_MENU))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('[Mm][Aa][Ii][Nn] [Mm][Ee][Nn][Uu]'), MAIN_MENU))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('[Cc][Ii][Rr][Cc][Uu][Ll][Aa][Rr]'), CIRCULAR))

updater.start_polling()
updater.idle()
