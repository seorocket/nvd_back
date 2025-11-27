from telegram.ext import Application, CommandHandler



import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


BOT_TOKEN = '8382027985:AAFaUlclLrv1BQ9MLRhiDT3x-FCFej2rRKI'
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

# # telegram_bot/bot.py
# import os
# import logging
# import requests
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import (
#     Application, 
#     CommandHandler, 
#     CallbackQueryHandler, 
#     ContextTypes,
#     MessageHandler,
#     filters
# )
# import asyncio
# # Настройки
# BOT_TOKEN = '8382027985:AAFaUlclLrv1BQ9MLRhiDT3x-FCFej2rRKI'

# # Настройка логирования
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )
# logger = logging.getLogger(__name__)

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик команды /start"""
#     user = update.effective_user
    
#     keyboard = [
#         [InlineKeyboardButton("🚀 Зарегистрироваться", callback_data="register")],
#         [InlineKeyboardButton("🔐 Войти", callback_data="login")],
#         [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     welcome_text = f"""
# 👋 Привет, {user.first_name}!

# Я бот для регистрации на нашем портале.

# Выберите действие:
# • **Регистрация** - создать новый аккаунт
# • **Вход** - войти в существующий аккаунт

# Нажмите кнопку ниже для начала:
# """
#     await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик нажатий на кнопки"""
#     query = update.callback_query
#     await query.answer()
    
#     if query.data == "register":
#         await start_registration(query, context)
#     elif query.data == "login":
#         await show_login_info(query, context)
#     elif query.data == "help":
#         await show_help(query, context)
#     elif query.data == "back_to_main":
#         await back_to_main(query, context)

# async def start_registration(query, context):
#     """Начать процесс регистрации"""
#     user = query.from_user
#     context.user_data['registration_step'] = 'waiting_email'
#     context.user_data['telegram_user'] = {
#         'id': user.id,
#         'first_name': user.first_name,
#         'last_name': user.last_name or '',
#         'username': user.username or ''
#     }
    
#     text = f"""
# 📝 **Регистрация**

# Привет, {user.first_name}!

# Для регистрации на портале нам нужен ваш email.

# Пожалуйста, введите ваш email адрес:
# """
    
#     keyboard = [[InlineKeyboardButton("⬅️ Отмена", callback_data="back_to_main")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# async def show_login_info(query, context):
#     """Показать информацию о входе"""
#     text = """
# 🔐 **Вход в систему**

# Для входа в систему используйте следующие данные:

# 📧 **Email**: ваш email, указанный при регистрации
# 🔑 **Пароль**: используйте кнопку "Забыли пароль" на сайте

# Или зарегистрируйтесь, если у вас еще нет аккаунта.
# """
    
#     keyboard = [
#         [InlineKeyboardButton("🚀 Зарегистрироваться", callback_data="register")],
#         [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик текстовых сообщений"""
#     user_data = context.user_data
#     current_step = user_data.get('registration_step')
    
#     if current_step == 'waiting_email':
#         await process_email(update, context, update.message.text.strip())
    
#     elif current_step == 'waiting_username':
#         await process_username(update, context, update.message.text.strip())

# async def process_email(update: Update, context: ContextTypes.DEFAULT_TYPE, email: str):
#     """Обработка введенного email"""
#     # Простая валидация email
#     if '@' not in email or '.' not in email:
#         await update.message.reply_text("❌ Неверный формат email. Пожалуйста, введите корректный email адрес:")
#         return
    
#     context.user_data['email'] = email
#     context.user_data['registration_step'] = 'waiting_username'
    
#     await update.message.reply_text("✅ Email принят!\n\n📝 Теперь введите желаемое имя пользователя (только латинские буквы, цифры и _):")

# async def process_username(update: Update, context: ContextTypes.DEFAULT_TYPE, username: str):
#     """Обработка введенного username"""
#     # Валидация username
#     if not username.replace('_', '').isalnum():
#         await update.message.reply_text("❌ Имя пользователя может содержать только латинские буквы, цифры и символ _. Попробуйте еще раз:")
#         return
    
#     if len(username) < 3:
#         await update.message.reply_text("❌ Имя пользователя должно быть не менее 3 символов. Попробуйте еще раз:")
#         return
    
#     context.user_data['username'] = username
    
#     # Регистрируем пользователя
#     success, message = await register_user_on_django(update, context)
    
#     if success:
#         context.user_data.clear()
#         keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await update.message.reply_text(
#             f"✅ {message}",
#             reply_markup=reply_markup
#         )
#     else:
#         keyboard = [
#             [InlineKeyboardButton("🔄 Попробовать снова", callback_data="register")],
#             [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
#         ]
#         reply_markup = InlineKeyboardMarkup(keyboard)
#         await update.message.reply_text(
#             f"❌ {message}",
#             reply_markup=reply_markup
#         )

# async def register_user_on_django(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Отправка данных регистрации на Django сервер"""
#     try:
#         user_data = context.user_data
#         telegram_user = user_data['telegram_user']
        
#         # Данные для регистрации
#         registration_data = {
#             'telegram_id': telegram_user['id'],
#             'username': user_data['username'],
#             'email': user_data['email'],
#             'first_name': telegram_user['first_name'],
#             'last_name': telegram_user['last_name'],
#             'tg_username': telegram_user['username'],
#             'auth_date': update.effective_message.date.timestamp()
#         }
        
#         logger.info(f"Sending registration data: {registration_data}")
        
#         # Отправляем запрос на регистрацию
#         response = requests.post(
#             f'{DJANGO_BASE_URL}/api/auth/telegram/register/',
#             json=registration_data,
#             timeout=10
#         )
        
#         logger.info(f"Response status: {response.status_code}")
#         logger.info(f"Response content: {response.text}")
        
#         if response.status_code in [200, 201]:
#             return True, "Регистрация завершена успешно! Теперь вы можете войти в систему через сайт."
#         else:
#             error_data = response.json()
#             error_msg = error_data.get('error', 'Неизвестная ошибка')
#             return False, f"Ошибка регистрации: {error_msg}"
        
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Network error during registration: {e}")
#         return False, "Ошибка соединения с сервером. Попробуйте позже."
#     except Exception as e:
#         logger.error(f"Registration error: {e}")
#         return False, "Внутренняя ошибка сервера. Попробуйте позже."

# async def show_help(query, context):
#     """Показать справку"""
#     text = """
# 🤖 **Помощь по боту**

# **Как зарегистрироваться:**
# 1. Нажмите кнопку "Зарегистрироваться"
# 2. Введите ваш email адрес
# 3. Введите желаемое имя пользователя
# 4. Бот создаст аккаунт автоматически

# **После регистрации:**
# • Вы получите email для подтверждения (если настроено)
# • Можете войти на сайт используя ваш email
# • Для сброса пароля используйте функцию "Забыли пароль" на сайте

# **Проблемы с регистрацией?**
# • Проверьте правильность ввода email
# • Убедитесь что имя пользователя содержит только латинские буквы, цифры и _
# • Если проблемы сохраняются - обратитесь в поддержку
# """
    
#     keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# async def back_to_main(query, context):
#     """Вернуться в главное меню"""
#     user = query.from_user
    
#     keyboard = [
#         [InlineKeyboardButton("🚀 Зарегистрироваться", callback_data="register")],
#         [InlineKeyboardButton("🔐 Войти", callback_data="login")],
#         [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
    
#     await query.edit_message_text(
#         f"Главное меню. Выберите действие, {user.first_name}:",
#         reply_markup=reply_markup
#     )

# async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     """Обработчик ошибок"""
#     logger.error(f"Exception while handling an update: {context.error}")

# async def main():
#     """Запуск бота"""
    
#     # Создаем приложение
#     application = Application.builder().token(BOT_TOKEN).build()
#     await application.initialize()
    
#     # Добавляем обработчики
#     application.add_handler(CommandHandler("start", start))
#     # application.add_handler(CallbackQueryHandler(button_handler))
#     # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     # application.add_error_handler(error_handler)
    
#     # Запускаем бота
#     logger.info("🤖 Бот запущен...")
#     print("=" * 50)
#     print("🤖 Telegram Bot запущен!")
#     print("⏹️  Для остановки нажмите Ctrl+C")
#     print("=" * 50)
    
#     # await application.run_polling()
#     await application.shutdown()

# if __name__ == '__main__':

#     asyncio.run(main())