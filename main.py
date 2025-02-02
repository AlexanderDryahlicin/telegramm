from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
import configparser
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Чтение конфигурации
config = configparser.ConfigParser()
config.read('settings.ini')
tgramm_token = config['TOKEN']['token']

# Определяем состояния для ConversationHandler
DAY, ROUTE = range(2)

# Данные маршрутов
routes_data = {
    "Понедельник": {
        "Октябрьский": ["тратата", "Адрес 2", "Адрес 3"],
        "Ломоносовский": ["Урицкого 50 маг", "Обводный 22 маг", "Шабалина 20 маг", "Урицкий 45 макси", "Урицкий 47 пят", "Тимме 1/3 маг", "ТИмме 4/3 полюс", "Тимме 4/4 пят", "Тимме 6 маг", "Дзержинского 7/4 маг", "Воскресенская 105 пят", "Воскресенская 114 чипок :)", "Воскресенская 112 пят", "Воскресенская 112 маг", "Шабалина 29 маг", "Воскресенская 89 маг", " Воскресенская 92 маг", "Обводный 29 пят", "Обводный 36 маг", "Воскресенская 20 титан-арена", "Воскресенская 20 Ирис (до10) :(", "Воскресенская 20 Д.М.(с10)", "Воскресенская 14 маг", "Карла Либнехта 22 пят", "Ломоносова 98 пят", "Поморская 24 маг", "Троицкий 52 маг", "Набережная 71 Анрофф", "Поморская 2 хочу лето", "Троицкий 17 макси", "Троицкий 17 Д.М.", "Троицкий 17 тортомастер", "Троицкий 17 Ирис", "Троицкий 3 пят", "Набережная 62 В/П", "Троицкий 20 петр", "Троицкий 20 кафе Ринкан (с 11)", "Ломоносова 117 албатрос", "Ломоносова 98 маг", "Ломоносова 90 петр", "Ломоносова 88 макси", "Выучейского 28 пят", "Выучейского 28/1 петр", "Северодвинская 31 маг", "Новгородский 32 иванов", "Розы Люксембург 7 маг", "Набережная 32 петр", "Ломоносова 44 пят", "Ломоносова 15/2 маг", "Урицкий 1 петр", "Урицкий 1 пят"],
        "Варавино-Фактория": ["Калинина 19 пят", "Почтовая 21 петр", "Ленинградский 167 маг (с9)", "Ленинградский 255 петромост", "Дачная 44 пят", "дачная 51", "Никитова 10", "Никитова 9", "Никитова 11", "Воронина 43 маг", "Воронина 21", "Русанова 8 петр", "Ленинградский 311", "Русанова 4", "Ленинградский 327", "Ленинградский 335", "Октябрьская 20", "Ленинградский 352", "Ленинградский 390", "Большесельская 48", "Устьянская 187", "Силикатчиков 5 маг", "Ленинградский 323", "Ленинградский 275"],
        "Маршрут 4": ["Адрес 10", "Адрес 11", "Адрес 12"],
        "Маршрут 5": ["Адрес 13", "Адрес 14", "Адрес 15"],
        "Маршрут 6": ["Адрес 16", "Адрес 17", "Адрес 18"],
    },
    "Вторник": {
        "Новодвинск": ["Мира 7 петр", "Мира 9 союз", "Димитрова 12 пят", "3 пятилеток 27", "Первомайская 6", "Космонавтов 7", "50 лет октября 50", "50 лет октября 43", "Пролетарская 61", "3 пятилеток 8", "Советов 25", "Советов 27", "Добровольского 2/20", "Советов 7", "Фр.Бригад 3", "Уборевича 16", "Пролетарская 47", "Южная 17", "Двинская 45/2", "--Катунино 2а", "--Маркина 3", "---Счастливая 12", "---Васьково зд.74а"],
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
    }
}

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> int:
    try:
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
        reply_keyboard = [days[i:i + 2] for i in range(0, len(days), 2)]
        await update.message.reply_text(
            "Выберите день недели:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        )
        return DAY
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")
        return ConversationHandler.END

# Обработчик выбора дня недели
async def choose_day(update: Update, context: CallbackContext) -> int:
    try:
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
    except Exception as e:
        logger.error(f"Ошибка в choose_day: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")
        return ConversationHandler.END

# Обработчик выбора маршрута
async def choose_route(update: Update, context: CallbackContext) -> int:
    try:
        user_choice = update.message.text
        day = context.user_data.get('day')

        if not day:
            await update.message.reply_text("Сначала выберите день.")
            return await start(update, context)

        if user_choice == "Назад":
            return await start(update, context)
        elif user_choice == "Отмена":
            return await cancel(update, context)

        if user_choice not in routes_data[day]:
            await update.message.reply_text("Пожалуйста, выберите маршрут из списка.")
            return ROUTE

        context.user_data['route'] = user_choice
        addresses = routes_data[day][user_choice]
        # Разделяем адреса на группы для удобства чтения
        address_groups = [addresses[i:i + 5] for i in range(0, len(addresses), 5)]
        response = f"Адреса для маршрута '{user_choice}':\n\n"
        for group in address_groups:
            response += "\n".join(group) + "\n\n"
        await update.message.reply_text(
            response,
            reply_markup=ReplyKeyboardMarkup([["Назад", "Отмена"]], resize_keyboard=True)
        )
        return ROUTE
    except Exception as e:
        logger.error(f"Ошибка в choose_route: {e}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте снова.")
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
    application = Application.builder().token(tgramm_token).build()

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