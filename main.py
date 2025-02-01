from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import configparser
#
token = "7852145634:AAGbrQ_FQ4VxZrOqo7OFwqbiIsZkgFZjgdk"
# Определяем состояния для ConversationHandler
DAY, ROUTE, ADDRESS = range(3)

# Данные маршрутов
routes_data = {
    "Понедельник": {
        "Маршрут 1": ["Адрес 1", "Адрес 2", "Адрес 3"],
        "Маршрут 2": ["Адрес 4", "Адрес 5", "Адрес 6"],
        "Маршрут 3": ["Адрес 7", "Адрес 8", "Адрес 9"],
        "Маршрут 4": ["Адрес 10", "Адрес 11", "Адрес 12"],
        "Маршрут 5": ["Адрес 13", "Адрес 14", "Адрес 15"],
        "Маршрут 6": ["Адрес 16", "Адрес 17", "Адрес 18"],
    },
    "Вторник": {
        "Маршрут 1": ["Адрес 19", "Адрес 20", "Адрес 21"],
        "Маршрут 2": ["Адрес 22", "Адрес 23", "Адрес 24"],
        "Маршрут 3": ["Адрес 25", "Адрес 26", "Адрес 27"],
        "Маршрут 4": ["Адрес 28", "Адрес 29", "Адрес 30"],
        "Маршрут 5": ["Адрес 31", "Адрес 32", "Адрес 33"],
        "Маршрут 6": ["Адрес 34", "Адрес 35", "Адрес 36"],
    },
    "Среда": {
        "Маршрут 1": ["Адрес 19", "Адрес 20", "Адрес 21"],
        "Маршрут 2": ["Адрес 22", "Адрес 23", "Адрес 24"],
        "Маршрут 3": ["Адрес 25", "Адрес 26", "Адрес 27"],
        "Маршрут 4": ["Адрес 28", "Адрес 29", "Адрес 30"],
        "Маршрут 5": ["Адрес 31", "Адрес 32", "Адрес 33"],
        "Маршрут 6": ["Адрес 34", "Адрес 35", "Адрес 36"],
    },
    "Четверг": {
        "Маршрут 1": ["Адрес 19", "Адрес 20", "Адрес 21"],
        "Маршрут 2": ["Адрес 22", "Адрес 23", "Адрес 24"],
        "Маршрут 3": ["Адрес 25", "Адрес 26", "Адрес 27"],
        "Маршрут 4": ["Адрес 28", "Адрес 29", "Адрес 30"],
        "Маршрут 5": ["Адрес 31", "Адрес 32", "Адрес 33"],
        "Маршрут 6": ["Адрес 34", "Адрес 35", "Адрес 36"],
    },
    "Пятница": {
        "Маршрут 1": ["Адрес 19", "Адрес 20", "Адрес 21"],
        "Маршрут 2": ["Адрес 22", "Адрес 23", "Адрес 24"],
        "Маршрут 3": ["Адрес 25", "Адрес 26", "Адрес 27"],
        "Маршрут 4": ["Адрес 28", "Адрес 29", "Адрес 30"],
        "Маршрут 5": ["Адрес 31", "Адрес 32", "Адрес 33"],
        "Маршрут 6": ["Адрес 34", "Адрес 35", "Адрес 36"],
        "Маршрут 7": ["Адрес 19", "Адрес 20", "Адрес 21"],
        "Маршрут 8": ["Адрес 22", "Адрес 23", "Адрес 24"],
        "Маршрут 9": ["Адрес 25", "Адрес 26", "Адрес 27"],
        "Маршрут 10": ["Адрес 28", "Адрес 29", "Адрес 30"],
        "Маршрут 11": ["Адрес 31", "Адрес 32", "Адрес 33"],
        "Маршрут 12": ["Адрес 34", "Адрес 35", "Адрес 36"],
    }

}

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> int:
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    reply_keyboard = [days[i:i + 2] for i in range(0, len(days), 2)]
    await update.message.reply_text(
        "Выберите день недели:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return DAY

# Обработчик выбора дня недели
async def choose_day(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    if user_choice not in routes_data:
        await update.message.reply_text("Пожалуйста, выберите день из списка.")
        return DAY

    context.user_data['day'] = user_choice
    routes = list(routes_data[user_choice].keys())
    reply_keyboard = [routes[i:i + 2] for i in range(0, len(routes), 2)]
    reply_keyboard.append(["Назад", "Отмена"])
    await update.message.reply_text(
        "Выберите маршрут:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return ROUTE

# Обработчик выбора маршрута
async def choose_route(update: Update, context: CallbackContext) -> int:
    user_choice = update.message.text
    day = context.user_data.get('day')
    if user_choice == "Назад":
        return await start(update, context)
    elif user_choice == "Отмена":
        return await cancel(update, context)

    if user_choice not in routes_data[day]:
        await update.message.reply_text("Пожалуйста, выберите маршрут из списка.")
        return ROUTE

    context.user_data['route'] = user_choice
    addresses = routes_data[day][user_choice]
    await update.message.reply_text(
        f"Адреса для маршрута '{user_choice}':\n" + "\n".join(addresses),
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Обработчик команды /cancel
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "Действие отменено.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# Основная функция
def main() -> None:
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_day)],
            ROUTE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_route)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == '__main__':
    main()