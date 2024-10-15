import logging
import os
import re
import paramiko
import psycopg2
import subprocess

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

load_dotenv()

TOKEN = os.getenv('TOKEN')
RM_HOST = os.getenv('RM_HOST')
RM_USER = os.getenv('RM_USER')
RM_PASSWORD = os.getenv('RM_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_DATABASE')

import logging
logging.basicConfig(filename='logfile.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s', encoding="utf-8")
logger = logging.getLogger(__name__)
logging.debug('Отладочная информация.')
logging.info('Работает модуль logging.')
logging.warning('Риск получения сообщения об ошибке.')
logging.error('Произошла ошибка.')
logging.critical('Программа не может выполняться.')


def connect():
    host = RM_HOST
    username = RM_USER 
    password = RM_PASSWORD
    port = '22'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    return client

def connect_db():

    host = DB_HOST
    username = DB_USER 
    password = DB_PASSWORD
    port = '65535'

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)

    return client

def start(update: Update, context):
    user = update.effective_user
    update.message.reply_text(f'Привет {user.full_name}!')


def get_emails(update: Update, context):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM emails")

    emails = cursor.fetchall()
    emailList = ''
    
    for i in range(len(emails)):
        emailList += f'{i+1}. {emails[i][0]}\n'

    update.message.reply_text(emailList)
    cursor.close()
    conn.close()

    return ConversationHandler.END

def get_phone_numbers(update: Update, context):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute("SELECT phone_number FROM phones")

    phones = cursor.fetchall()
    phoneList = ''
    
    for i in range(len(phones)):
        phoneList += f'{i+1}. {phones[i][0]}\n'

    update.message.reply_text(phoneList)
    cursor.close()
    conn.close()

    return ConversationHandler.END

def find_phone_number_command(update: Update, context):
    update.message.reply_text('Введите текст для поиска телефонных номеров: ')

    return 'find_phone_number'

def helpCommand(update: Update, context):
    update.message.reply_text('Help!')

def find_email_command(update: Update, context):
    update.message.reply_text('Введите текст для поиска email адресов: ')

    return 'find_email'

def verify_password_command(update: Update, context):
    update.message.reply_text('Введите пароль на проверку: ')

    return 'verify_password'

def get_release(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("lsb_release -a")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_uname(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("uname -a")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_uptime(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("uptime")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_df(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("df")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_free(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("free -h")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_mpstat(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("mpstat")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_w(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("w")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_auths(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("last -n 10")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_critical(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("journalctl -p crit -n 5")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_ps(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("ps")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_ss(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("ss -l | tail")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_services(update: Update, context):
    client = connect()

    stdin, stdout, stderr = client.exec_command("service --status-all")
    
    update.message.reply_text(stdout.read().decode().strip())
    client.close()

    return ConversationHandler.END

def get_apt_list_command(update: Update, context):
    update.message.reply_text('Введите 1 что бы увидеть список всех пакетов, либо название пакета что бы получить информацию о конкретном пакете')

    return 'get_apt_list'


def get_apt_list(update: Update, context):
    client = connect()

    user_input = update.message.text

    if user_input == "1":
        stdin, stdout, stderr = client.exec_command("dpkg --get-selections | tail -n 20")
        update.message.reply_text(stdout.read().decode().strip())
    else:
        stdin, stdout, stderr = client.exec_command(f"apt show {user_input}")
        update.message.reply_text(stdout.read().decode().strip() + stderr.read().decode().strip())
    client.close()
    return ConversationHandler.END

# def getReplLogs(update: Update, context):
#     client = connect_db()

#     stdin, stdout, stderr = client.exec_command("tail -n 20 /var/log/postgresql/postgresql-15-main.log")
    
#     update.message.reply_text(stdout.read().decode().strip() + stderr.read().decode().strip())
#     client.close()

#     return ConversationHandler.END

def get_repl_logs(update: Update, context):
    try:
        result = subprocess.run(
            ["bash", "-c", f"cat /var/log/postgresql/postgresql.log | grep 'repl' | tail -n 15"],
            capture_output=True,
            text=True
        )
        logs = result.stdout
        if logs:
            update.message.reply_text(f"Последние логи:\n{logs}")
        else:
            update.message.reply_text("Логи репликации не найдены.")
    except Exception as e:
        update.message.reply_text(f"Ошибка при получении логов: {str(e)}")


def verify_password(update: Update, context):
    user_input = update.message.text

    passwordRegex = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()]).{8,}')
    
    passlist = passwordRegex.findall(user_input)
    if not passlist:
        update.message.reply_text('Пароль простой')
        return
    update.message.reply_text('Пароль сложный')
    return ConversationHandler.END

def find_email (update: Update, context):
    user_input = update.message.text
    emailRegex = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
    emailList = emailRegex.findall(user_input)

    if not emailList:
        update.message.reply_text('Email адреса не найдены')
        return ConversationHandler.END

    email = ''
    for i in range(len(emailList)):
        email += f'{i+1}. {emailList[i]}\n'

    context.user_data['found_emails'] = emailList
    update.message.reply_text(email)
    update.message.reply_text('Хотите записать новые адреса')
    return 'saveEmail'

def saveEmail(update: Update, context):
    user_ans = update.message.text.lower()
    emailList = context.user_data.get('found_emails', [])

    if user_ans == "Да" or user_ans == "да":
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()
            
            for email in emailList:
                print(email)
                cursor.execute("INSERT INTO emails (email) VALUES (%s)", (email,))
            conn.commit()
            cursor.close()
            conn.close()
            update.message.reply_text('Успешная запись!')
        except Exception as e:
            logger.error(f"Ошибка в сохранении новых записей: {e}")
    else:
        update.message.reply_text('Новые адреса не будут записаны')  
    return ConversationHandler.END
        

def find_phone_number (update: Update, context):
    user_input = update.message.text 

    # регулярное выражение для всех вариантов номеров
    phoneNumRegex = re.compile(r'8 \(\d{3}\) \d{3}-\d{2}-\d{2}|8\d{10}|8\(\d{3}\)\d{7}|8 \d{3} \d{3} \d{2} \d{2}|8 \(\d{3}\) \d{3} \d{2} \d{2}|8-\d{3}-\d{3}-\d{2}-\d{2}|\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}|\+7\d{10}|\+7\(\d{3}\)\d{7}|\+7 \d{3} \d{3} \d{2} \d{2}|\+7 \(\d{3}\) \d{3} \d{2} \d{2}|\+7-\d{3}-\d{3}-\d{2}-\d{2}') 
    phoneNumberList = phoneNumRegex.findall(user_input) 
    if not phoneNumberList: 
        update.message.reply_text('Телефонные номера не найдены')
        return ConversationHandler.END 
    
    phoneNumbers = '' 
    for i in range(len(phoneNumberList)):
        phoneNumbers += f'{i+1}. {phoneNumberList[i]}\n' 

    context.user_data['found_phones'] = phoneNumberList
    update.message.reply_text(phoneNumbers)
    update.message.reply_text('Хотите записать новые номера?')
    return 'savePhone'

def savePhone(update: Update, context):
    user_ans = update.message.text.lower()
    phoneNumberList = context.user_data.get('found_phones', [])
    
    if user_ans == "Да" or user_ans == "да":
        try:
            conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
            cursor = conn.cursor()
            for phone in phoneNumberList:
                cursor.execute("INSERT INTO phones (phone_number) VALUES (%s)", (phone,))
            conn.commit()
            cursor.close()
            conn.close()
            update.message.reply_text('Успешная запись!')
        except Exception as e:
            logger.error(f"Ошибка в сохранении новых записей: {e}")
    else:
        update.message.reply_text('Новые номера не будут записаны')
        
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    
    dp = updater.dispatcher

    convHandlerFindPhoneNumbers = ConversationHandler(
        entry_points=[CommandHandler('find_phone_number', find_phone_number_command)],
        states={
            'find_phone_number': [MessageHandler(Filters.text & ~Filters.command, find_phone_number)],
            'savePhone': [MessageHandler(Filters.text & ~Filters.command, savePhone)]
        },
        fallbacks=[]
    )
    convHandlerFindEmail = ConversationHandler(
        entry_points=[CommandHandler('find_email', find_email_command)],
        states={
            'find_email': [MessageHandler(Filters.text & ~Filters.command, find_email)],
            'saveEmail': [MessageHandler(Filters.text & ~Filters.command, saveEmail)]
        },
        fallbacks=[]
    )

    convHandlerVerifyPassword = ConversationHandler(
        entry_points=[CommandHandler('verify_password', verify_password_command)],
        states={
            'verify_password': [MessageHandler(Filters.text & ~Filters.command, verify_password)],
        },
        fallbacks=[]
    )
	
    convHandlerGetRelease = ConversationHandler(
        entry_points=[CommandHandler('get_release', get_release)],
        states={
            'get_release': [MessageHandler(Filters.text & ~Filters.command, get_release)],
        },
        fallbacks=[]
    )

    convHandlerGetUname = ConversationHandler(
        entry_points=[CommandHandler('get_uname', get_uname)],
        states={
            'get_uname': [MessageHandler(Filters.text & ~Filters.command, get_uname)],
        },
        fallbacks=[]
    )

    convHandlerGetUptime = ConversationHandler(
        entry_points=[CommandHandler('get_uptime', get_uptime)],
        states={
            'get_uptime': [MessageHandler(Filters.text & ~Filters.command, get_uptime)],
        },
        fallbacks=[]
    )

    convHandlerGetDf = ConversationHandler(
        entry_points=[CommandHandler('get_df', get_df)],
        states={
            'get_df': [MessageHandler(Filters.text & ~Filters.command, get_df)],
        },
        fallbacks=[]
    )

    convHandlerGetFree = ConversationHandler(
        entry_points=[CommandHandler('get_free', get_free)],
        states={
            'get_free': [MessageHandler(Filters.text & ~Filters.command, get_free)],
        },
        fallbacks=[]
    )

    convHandlerGetMpstat = ConversationHandler(
        entry_points=[CommandHandler('get_mpstat', get_mpstat)],
        states={
            'get_mpstat': [MessageHandler(Filters.text & ~Filters.command, get_mpstat)],
        },
        fallbacks=[]
    )

    convHandlerGetW = ConversationHandler(
        entry_points=[CommandHandler('get_w', get_w)],
        states={
            'get_w': [MessageHandler(Filters.text & ~Filters.command, get_w)],
        },
        fallbacks=[]
    )

    convHandlerGetAuth = ConversationHandler(
        entry_points=[CommandHandler('get_auths', get_auths)],
        states={
            'get_auths': [MessageHandler(Filters.text & ~Filters.command, get_auths)],
        },
        fallbacks=[]
    )

    convHandlerGetCrit = ConversationHandler(
        entry_points=[CommandHandler('get_critical', get_critical)],
        states={
            'get_critical': [MessageHandler(Filters.text & ~Filters.command, get_critical)],
        },
        fallbacks=[]
    )

    convHandlerGetPs = ConversationHandler(
        entry_points=[CommandHandler('get_ps', get_ps)],
        states={
            'get_ps': [MessageHandler(Filters.text & ~Filters.command, get_ps)],
        },
        fallbacks=[]
    )

    convHandlerGetSs = ConversationHandler(
        entry_points=[CommandHandler('get_ss', get_ss)],
        states={
            'get_ss': [MessageHandler(Filters.text & ~Filters.command, get_ss)],
        },
        fallbacks=[]
    )

    convHandlerGetServices = ConversationHandler(
        entry_points=[CommandHandler('get_services', get_services)],
        states={
            'get_services': [MessageHandler(Filters.text & ~Filters.command, get_services)],
        },
        fallbacks=[]
    )

    convHandlerGetAptList = ConversationHandler(
        entry_points=[CommandHandler('get_apt_list', get_apt_list_command)],
        states={
            'get_apt_list': [MessageHandler(Filters.text & ~Filters.command, get_apt_list)],
        },
        fallbacks=[]
    )

    convHandlerGetReplLogs = ConversationHandler(
        entry_points=[CommandHandler('get_repl_logs', get_repl_logs)],
        states={
            'get_repl_logs': [MessageHandler(Filters.text & ~Filters.command, get_repl_logs)],
        },
        fallbacks=[]
    )

    convHandlerGetEmails = ConversationHandler(
        entry_points=[CommandHandler('get_emails', get_emails)],
        states={
            'get_emails': [MessageHandler(Filters.text & ~Filters.command, get_emails)],
        },
        fallbacks=[]
    )

    convHandlerGetPhones = ConversationHandler(
        entry_points=[CommandHandler('get_phone_numbers', get_phone_numbers)],
        states={
            'get_phone_numbers': [MessageHandler(Filters.text & ~Filters.command, get_phone_numbers)],
        },
        fallbacks=[]
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helpCommand))
    dp.add_handler(convHandlerFindPhoneNumbers)
    dp.add_handler(convHandlerFindEmail)
    dp.add_handler(convHandlerVerifyPassword)
    dp.add_handler(convHandlerGetRelease)
    dp.add_handler(convHandlerGetUname)
    dp.add_handler(convHandlerGetUptime)

    dp.add_handler(convHandlerGetDf)
    dp.add_handler(convHandlerGetFree)
    dp.add_handler(convHandlerGetMpstat)

    dp.add_handler(convHandlerGetW)
    dp.add_handler(convHandlerGetAuth)
    dp.add_handler(convHandlerGetCrit)

    dp.add_handler(convHandlerGetPs)
    dp.add_handler(convHandlerGetSs)
    dp.add_handler(convHandlerGetServices)

    dp.add_handler(convHandlerGetAptList)

    dp.add_handler(convHandlerGetReplLogs)
    dp.add_handler(convHandlerGetEmails)
    dp.add_handler(convHandlerGetPhones)

    updater.start_polling()

    updater.idle()



if __name__ == '__main__':
    main()

